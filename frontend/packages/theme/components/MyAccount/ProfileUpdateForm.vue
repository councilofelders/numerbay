<template>
  <ValidationObserver v-slot="{ handleSubmit, reset }">
    <form class="form" @submit.prevent="handleSubmit(submitForm(reset))">
      <ValidationProvider rules="required|min:2" v-slot="{ errors }" class="form__element">
        <SfInput
          v-model="form.username"
          name="username"
          label="Username"
          required
          :valid="!errors[0]"
          :errorMessage="errors[0]"
        />
      </ValidationProvider>
      <ValidationProvider rules="email" v-slot="{ errors }" class="form__element">
        <SfInput
          v-model="form.email"
          type="email"
          name="email"
          label="Your e-mail"
          :valid="!errors[0]"
          :errorMessage="errors[0]"
        />
      </ValidationProvider>
      <ValidationProvider rules="min:6" v-slot="{ errors }" class="form__element">
        <SfInput
          v-model="form.password"
          name="password"
          type="password"
          label="New password (Leave empty for no change)"
          :valid="!errors[0]"
          :errorMessage="errors[0]"
        />
      </ValidationProvider>
      <div class="form__horizontal">
        <MetamaskButton @click:connect="handleWeb3Connect" @click:disconnect="handleWeb3Disconnect" :is-connected="!!form.publicAddress" :disabled="loading"/>
        <ValidationProvider rules="" v-slot="{ errors }" class="form__element">
          <SfInput
            v-model="form.publicAddress"
            name="publicAddress"
            label="Your wallet public address"
            disabled
            :valid="!errors[0]"
            :errorMessage="errors[0]"
          />
        </ValidationProvider>
      </div>
      <div v-if="error.web3">
        {{ error.web3 }}
      </div>
      <SfButton class="form__button">{{ $t('Update profile data') }}</SfButton>
    </form>
  </ValidationObserver>
</template>

<script>
import {reactive, ref} from '@vue/composition-api';
import { ValidationProvider, ValidationObserver } from 'vee-validate';
import { useUser, userGetters } from '@vue-storefront/numerbay';
import { useUiNotification } from '~/composables';
import { SfInput, SfButton } from '@storefront-ui/vue';
import MetamaskButton from '../Molecules/MetamaskButton';
import Web3 from 'web3';
import {Logger} from '@vue-storefront/core';

export default {
  name: 'ProfileUpdateForm',

  components: {
    SfInput,
    SfButton,
    ValidationProvider,
    ValidationObserver,
    MetamaskButton
  },
  computed: {
    activeAccount() {
      return this.web3User.activeAccount;
    }
  },
  methods: {
    async handleWeb3Connect() {
      await this.initWeb3Modal();
      await this.ethereumListener();
      await this.connectWeb3Modal();
      await this.publicAddressHandler(this.web3User.activeAccount);
      console.log('web3User.activeAccount, ', this.web3User.activeAccount);
    },
    async handleWeb3Disconnect() {
      await this.disconnectWeb3Modal();
      await this.publicAddressHandler('');
      console.log('web3User.activeAccount, ', this.web3User.activeAccount);
    },
    async publicAddressHandler(publicAddress) {
      Logger.debug('profile on publicAddressChange: ', publicAddress);
      if (publicAddress) {
        try {
          // get nonce from backend
          await this.getNonceAuthenticated();
          console.log('this.web3User', this.web3User);
          const { nonce } = this.web3User.nonce;

          // web3 lib instance
          const web3 = new Web3(this.web3User.providerEthers.provider);
          const signaturePromise = web3.eth.personal.sign(
            `I am signing my one-time nonce: ${nonce}`,
            publicAddress,
            // MetaMask will ignore the password argument here
            '',
            (err, signature)=>{
              if (err) {
                this.error.web3 = 'You need to sign the message.';
                this.disconnectWeb3Modal();
              } else {
                // this.resetErrorValues();
                Logger.debug('Web3 signature: ', signature);
              }
            }
          );

          // login with the signature
          signaturePromise.then(async (signature)=>{
            await this.updateUser({
              user: {
                publicAddress: publicAddress,
                signature: signature
              }
            });
            this.form = this.resetForm();
          });

        } catch (err) {
          Logger.error(err);
          throw new Error(
            'You need to sign the message to be able to log in.'
          );
        }
      } else {
        await this.updateUser({ user: { publicAddress: ''}});
        this.form = this.resetForm();
        await this.send({
          message: 'Please connect a wallet or set a password before logging out, or you might lose access to this account',
          type: 'warning',
          persist: true
        });
      }
    }
  },
  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  setup(_, { emit }) {
    const { user, load, loading, setUser, updateUser, web3User, initWeb3Modal, ethereumListener, connectWeb3Modal,
      disconnectWeb3Modal, getNonceAuthenticated, error: userError } = useUser();
    const { send } = useUiNotification();

    const error = reactive({
      web3: null
    });

    const resetErrorValues = () => {
      error.web3 = null;
    };

    const resetForm = () => ({
      username: userGetters.getUsername(user.value),
      email: userGetters.getEmailAddress(user.value),
      publicAddress: userGetters.getPublicAddress(user.value),
      nonce: userGetters.getNonce(user.value)
    });

    const form = ref(resetForm());

    const submitForm = (resetValidationFn) => {
      resetErrorValues();
      return () => {
        const onComplete = () => {
          form.value = resetForm();
          resetValidationFn();
          if (userError.value.updateUser) {
            send({
              message: userError.value.updateUser.message,
              type: 'danger'
            });
          } else {
            send({
              message: 'Successfully updated profile',
              type: 'success',
              icon: 'check'
            });
          }
        };

        const onError = () => {
          // TODO: Handle error
        };

        emit('submit', { form, onComplete, onError });
      };
    };

    return {
      form,
      error,
      user,
      load,
      loading,
      setUser,
      web3User,
      initWeb3Modal,
      ethereumListener,
      connectWeb3Modal,
      disconnectWeb3Modal,
      getNonceAuthenticated,
      updateUser,
      resetForm,
      submitForm,
      send
    };
  }
};
</script>

<style lang='scss' scoped>
.form {
  &__element {
    display: block;
    margin: 0 0 var(--spacer-lg) 0;
  }
  &__button {
    display: block;
    width: 100%;
    @include for-desktop {
      width: 17.5rem;
    }
  }
  &__horizontal {
    @include for-desktop {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
    }
    .form__element {
      @include for-desktop {
        flex: 1;
        margin-right: var(--spacer-2xl);
      }

      &:last-child {
        margin-right: 0;
      }
    }
  }
}
</style>
