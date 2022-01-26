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
      <div class="highlighted">
        <div class="form__horizontal">
          <MetamaskButton @click:connect="handleWeb3Connect" @click:disconnect="handleWeb3Disconnect" :is-connected="!!form.publicAddress" :disabled="loading"/>
          <ValidationProvider rules="" v-slot="{ errors }" class="form__element" v-if="!!form.publicAddress">
            <SfInput
              v-model="form.publicAddress"
              name="publicAddress"
              label="Your wallet public address"
              disabled
              :valid="!errors[0]"
              :errorMessage="errors[0]"
              style="display: none;"
            />
          </ValidationProvider>
          <SfButton
            v-if="!!form.publicAddress"
            class="sf-button--text"
            @click="copyToClipboard(form.publicAddress)"
            type="button"
          >
            {{form.publicAddress}}
          </SfButton>
          <div v-else>
            No wallet connected
          </div>
        </div>
        <div v-if="error.web3">
          {{ error.web3 }}
        </div>
        <br/>
        <div class="form__horizontal">
          <SfButton class="form__button color-secondary" @click="generateKeyPair" type="button">{{ $t('Generate key Pair') }}</SfButton>
          <div v-if="!!form.publicKey">
            <SfButton
              class="sf-button--text"
              @click="exportKeyPair"
              type="button"
            >
              Export key file
            </SfButton>
          </div>
          <div v-else>
            No key available
          </div>
        </div>
      </div>
      <br/>
      <SfButton class="form__button">{{ $t('Update profile data') }}</SfButton>
    </form>
  </ValidationObserver>
</template>

<script>
import { SfButton, SfInput } from '@storefront-ui/vue';
import { ValidationObserver, ValidationProvider, extend } from 'vee-validate';
import { email, min, required } from 'vee-validate/dist/rules';
import { reactive, ref } from '@vue/composition-api';
import { useUser, userGetters } from '@vue-storefront/numerbay';
import { Logger } from '@vue-storefront/core';
import MetamaskButton from '../Molecules/MetamaskButton';
import Web3 from 'web3';
import { encodeBase64 } from 'tweetnacl-util';
import { encrypt } from 'eth-sig-util';
import nacl from 'tweetnacl';
import { useUiNotification } from '~/composables';

extend('email', {
  ...email,
  message: 'Invalid email'
});

extend('required', {
  ...required,
  message: 'This field is required'
});

extend('min', {
  ...min,
  message: 'The field should have at least {length} characters'
});

// extend('password', {
//   validate: value => String(value).length >= 8 && String(value).match(/[A-Za-z]/gi) && String(value).match(/[0-9]/gi),
//   message: 'Password must have at least 8 characters including one letter and a number'
// });

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
    async copyToClipboard(text) {
      try {
        await this.$copyText(text);
        await this.send({
          message: 'Value copied',
          type: 'success',
          icon: 'check'
        });
      } catch (e) {
        console.error('Copy failed: ', e);
      }
    },
    downloadFile(file, name) {
      const a = document.createElement('a');
      document.body.appendChild(a);
      a.style = 'display: none';

      const url = window.URL.createObjectURL(file);
      a.href = url;
      a.download = name;
      a.click();
      window.URL.revokeObjectURL(url);
    },
    async exportKeyPair() {
      const privateKeyStr = await window.ethereum.request({
        method: 'eth_decrypt',
        params: [this.form.encryptedPrivateKey, window.ethereum.selectedAddress]
      });

      const privateKey = encodeBase64(new Uint8Array(privateKeyStr.split(',').map((item) => parseInt(item))));
      // eslint-disable-next-line camelcase
      const keyJson = JSON.stringify({public_key: this.form.publicKey, private_key: privateKey});
      this.downloadFile(new Blob([keyJson], {type: 'application/json'}), 'numerbay.json');
    },
    async generateKeyPair() {
      if (!this.form.publicAddress) {
        await this.send({
          message: 'Please connect a MetaMask wallet first',
          type: 'warning'
        });
        return;
      }

      const keyPair = nacl.box.keyPair();
      const privateKeyBytes = keyPair.secretKey;
      const publicKeyBytes = keyPair.publicKey;

      let encryptedPrivateKey = null;
      try {
        const accounts = await window.ethereum.request({
          method: 'eth_requestAccounts'
        });

        const key = await window.ethereum.request({
          method: 'eth_getEncryptionPublicKey',
          params: [accounts[0]]
        });

        encryptedPrivateKey = JSON.stringify(encrypt(
          key,
          {data: privateKeyBytes.toString('hex')},
          'x25519-xsalsa20-poly1305'
        ));
      } catch {
        return;
      }

      await this.updateUser({
        user: {
          publicKey: encodeBase64(publicKeyBytes),
          encryptedPrivateKey: encryptedPrivateKey
        }
      });
      this.form = this.resetForm();
    },
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
      nonce: userGetters.getNonce(user.value),
      publicKey: user.value.public_key,
      encryptedPrivateKey: user.value.encrypted_private_key
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
.highlighted {
  box-sizing: border-box;
  width: 100%;
  background-color: var(--c-light);
  padding: var(--spacer-sm);
  --property-value-font-size: var(--font-size--base);
  --property-name-font-size: var(--font-size--base);
  &:last-child {
    margin-bottom: 0;
  }
  ::v-deep .sf-property__name {
    white-space: nowrap;
  }
  ::v-deep .sf-property__value {
    text-align: right;
  }
  &--total {
    margin-bottom: var(--spacer-sm);
  }
  @include for-desktop {
    padding: var(--spacer-xl);
    --property-name-font-size: var(--font-size--lg);
    --property-name-font-weight: var(--font-weight--medium);
    --property-value-font-size: var(--font-size--lg);
    --property-value-font-weight: var(--font-weight--semibold);
  }
}
</style>
