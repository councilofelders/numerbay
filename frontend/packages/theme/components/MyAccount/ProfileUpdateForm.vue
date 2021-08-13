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
        <MetamaskButton @publicAddressChange="onPublicAddressChange"></MetamaskButton>
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
      <SfButton class="form__button">{{ $t('Update profile data') }}</SfButton>
    </form>
  </ValidationObserver>
</template>

<script>
import { ref } from '@vue/composition-api';
import { ValidationProvider, ValidationObserver } from 'vee-validate';
import { useUser, userGetters } from '@vue-storefront/numerbay';
import { SfInput, SfButton } from '@storefront-ui/vue';
import MetamaskButton from '../Molecules/MetamaskButton';
import Web3 from 'web3';
import {Logger, useVSFContext} from '@vue-storefront/core';

export default {
  name: 'ProfileUpdateForm',

  components: {
    SfInput,
    SfButton,
    ValidationProvider,
    ValidationObserver,
    MetamaskButton
  },

  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  setup(_, { emit }) {
    const { user } = useUser();
    const vsfContext = useVSFContext();
    const onPublicAddressChange = async (publicAddress, providerEthers, callback) => {
      if (publicAddress) {
        // get nonce from backend
        const { nonce } = await vsfContext.$numerbay.api.logInGetNonce({
          publicAddress: publicAddress
        });
        try {
          // web3 lib instance
          const web3 = new Web3(providerEthers.provider);
          const signaturePromise = web3.eth.personal.sign(
            `I am signing my one-time nonce: ${nonce}`,
            publicAddress,
            // MetaMask will ignore the password argument here
            '',
            callback
          );

          // Update publicAddress to backend
          signaturePromise.then(async (signature)=>{
            const response = await vsfContext.$numerbay.api.logInGetTokenWeb3({
              publicAddress: publicAddress,
              signature: signature
            });

            Logger.debug(`login web3 response: ${JSON.stringify(response)}`);
            return response;
          });
        } catch (err) {
          Logger.error(err);
          throw new Error(
            'You need to sign the message to be able to log in.'
          );

        }
      }
    };

    const resetForm = () => ({
      username: userGetters.getUsername(user.value),
      email: userGetters.getEmailAddress(user.value),
      publicAddress: userGetters.getPublicAddress(user.value),
      nonce: userGetters.getNonce(user.value)
    });

    const form = ref(resetForm());

    const submitForm = (resetValidationFn) => {
      return () => {
        const onComplete = () => {
          form.value = resetForm();
          resetValidationFn();
        };

        const onError = () => {
          // TODO: Handle error
        };

        emit('submit', { form, onComplete, onError });
      };
    };

    return {
      form,
      submitForm,
      onPublicAddressChange
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
