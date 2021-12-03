<template>
  <SfModal
    v-e2e="'login-modal'"
    :visible="isLoginModalOpen"
    class="modal"
    @close="toggleLoginModal"
  >
    <template #modal-bar>
      <SfBar
        class="sf-modal__bar smartphone-only"
        :close="true"
        :title="isLogin ? 'Log in' : 'Sign in'"
        @click:close="toggleLoginModal"
      />
    </template>
    <transition name="sf-fade" mode="out-in">
      <SfTabs :open-tab="1" v-e2e="'login-options-tab'">
        <SfTab title="One-Click Login">
          <MetamaskButton @click:connect="handleWeb3Connect" class="action" :disabled="loading"/>
          <div v-if="error.web3">
            {{ error.web3 }}
          </div>
        </SfTab>
        <SfTab title="Username Login">
          <div v-if="isLogin">
            <ValidationObserver v-slot="{ handleSubmit }" key="log-in">
              <form class="form" @submit.prevent="handleSubmit(handleLogin)">
                <ValidationProvider rules="required|min:2" v-slot="{ errors }">
                  <SfInput
                    v-e2e="'login-modal-username'"
                    v-model="form.username"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="username"
                    label="Username"
                    class="form__element"
                  />
                </ValidationProvider>
                <ValidationProvider rules="required|min:6" v-slot="{ errors }">
                  <SfInput
                    v-e2e="'login-modal-password'"
                    v-model="form.password"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="password"
                    label="Password"
                    type="password"
                    class="form__element"
                  />
                </ValidationProvider>
                <!--<SfCheckbox
                  v-e2e="'login-modal-remember-me'"
                  v-model="rememberMe"
                  name="remember-me"
                  label="Remember me"
                  class="form__element checkbox"
                />-->
                <div v-if="error.login">
                  {{ error.login }}
                </div>
                <SfButton
                  name="login-modal-submit"
                  v-e2e="'login-modal-submit'"
                  type="submit"
                  class="sf-button--full-width form__button"
                  :disabled="loading"
                >
                  <SfLoader :class="{ loader: loading }" :loading="loading">
                    <div>{{ $t('Login') }}</div>
                  </SfLoader>
                </SfButton>
              </form>
            </ValidationObserver>
            <!--<div class="action">
              <SfButton class="sf-button&#45;&#45;text">
                {{ $t('Forgotten password?') }}
              </SfButton>
            </div>-->
            <div class="bottom">
              <p class="bottom__paragraph">{{ $t('No account') }}</p>
              <SfButton class="sf-button--text" @click="setIsLoginValue(false)"
                        v-e2e="'register-option-button'"
                        name="register-option-button"
              >
                {{ $t('Register today') }}
              </SfButton>
            </div>
          </div>
          <div v-else class="form">
            <ValidationObserver v-slot="{ handleSubmit }" key="sign-up">
              <form class="form" @submit.prevent="handleSubmit(handleRegister)" autocomplete="off">
                <ValidationProvider rules="required|min:2" v-slot="{ errors }">
                  <SfInput
                    v-e2e="'login-modal-username'"
                    v-model="form.username"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="username"
                    label="Username"
                    class="form__element"
                  />
                </ValidationProvider>
                <ValidationProvider rules="required|min:6" v-slot="{ errors }">
                  <SfInput
                    v-e2e="'login-modal-password'"
                    v-model="form.password"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="password"
                    label="Password"
                    type="password"
                    class="form__element"
                  />
                </ValidationProvider>
                <div v-if="error.register">
                  {{ error.register }}
                </div>
                <SfButton
                  name="login-modal-submit"
                  v-e2e="'login-modal-submit'"
                  type="submit"
                  class="sf-button--full-width form__button"
                  :disabled="loading"
                >
                  <SfLoader :class="{ loader: loading }" :loading="loading">
                    <div>{{ $t('Create an account') }}</div>
                  </SfLoader>
                </SfButton>
              </form>
            </ValidationObserver>
            <div class="action">
              {{ $t('or') }}
              <SfButton v-e2e="'login-modal-login-to-your-account'" class="sf-button--text" @click="setIsLoginValue(true)">
                {{ $t('login in to your account') }}
              </SfButton>
            </div>
          </div>
        </SfTab>
      </SfTabs>
    </transition>
  </SfModal>
</template>
<script>
import { ref, watch, reactive } from '@vue/composition-api';
import { SfModal, SfTabs, SfInput, SfButton, SfCheckbox, SfLoader, SfBar } from '@storefront-ui/vue';
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
import { required, min } from 'vee-validate/dist/rules';
import { useUser} from '@vue-storefront/numerbay';
import { Logger } from '@vue-storefront/core';
import { useUiState } from '~/composables';
import MetamaskButton from './Molecules/MetamaskButton';
import Web3 from 'web3';

extend('required', {
  ...required,
  message: 'This field is required'
});

extend('min', {
  ...min,
  message: 'The field should have at least {length} characters'
});

export default {
  name: 'LoginModal',
  components: {
    SfModal,
    SfTabs,
    SfInput,
    SfButton,
    SfCheckbox,
    SfLoader,
    SfBar,
    MetamaskButton,
    ValidationProvider,
    ValidationObserver
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
    async publicAddressHandler(publicAddress) {
      Logger.debug('login on publicAddressChange: ', publicAddress);
      if (publicAddress) {
        try {
          // get nonce from backend
          await this.getNonce({ publicAddress: this.web3User.activeAccount });
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
                // this.disconnectWeb3Modal();
              } else {
                // this.resetErrorValues();
                Logger.debug('Web3 signature: ', signature);
              }
            }
          );

          // login with the signature
          signaturePromise.then(async (signature)=>{
            await this.loginWeb3({
              user: {
                publicAddress: publicAddress,
                signature: signature
              }
            }).then(() => this.toggleLoginModal());
          });

        } catch (err) {
          Logger.error(err);
          throw new Error(
            'You need to sign the message to be able to log in.'
          );
        }
      }
    }
  },
  setup() {
    const { isLoginModalOpen, toggleLoginModal } = useUiState();
    const form = ref({});
    const isLogin = ref(true);
    // const createAccount = ref(false);
    // const rememberMe = ref(false);
    const { register, login, loading, setUser, error: userError,
      web3User, initWeb3Modal, ethereumListener, connectWeb3Modal, getNonce, loginWeb3 } = useUser();

    const error = reactive({
      login: null,
      web3: null,
      register: null
    });

    const resetErrorValues = () => {
      error.login = null;
      error.web3 = null;
      error.register = null;
    };

    watch(isLoginModalOpen, () => {
      if (isLoginModalOpen) {
        form.value = {};
        resetErrorValues();
      }
    });

    const setIsLoginValue = (value) => {
      resetErrorValues();
      isLogin.value = value;
    };

    const handleForm = (fn) => async () => {
      resetErrorValues();
      await fn({ user: form.value });

      const hasUserErrors = userError.value.register || userError.value.login || userError.value.web3;
      if (hasUserErrors) {
        error.login = userError.value.login?.message;
        error.web3 = userError.value.web3?.message;
        error.register = userError.value.register?.message;
        return;
      }
      toggleLoginModal();
    };

    const handleRegister = async () => handleForm(register)();

    const handleLogin = async () => handleForm(login)();

    return {
      form,
      error,
      userError,
      setUser,
      loading,
      isLogin,
      isLoginModalOpen,
      toggleLoginModal,
      web3User,
      initWeb3Modal,
      ethereumListener,
      connectWeb3Modal,
      getNonce,
      loginWeb3,
      handleLogin,
      handleRegister,
      setIsLoginValue,
      resetErrorValues
    };
  }
};
</script>

<style lang="scss" scoped>

.modal {
  --modal-index: 3;
  --overlay-z-index: 3;
}
.form {
  margin-top: var(--spacer-sm);
  &__element {
    margin: 0 0 var(--spacer-xl) 0;
  }
}
.action {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: var(--spacer-xl) 0 var(--spacer-xl) 0;
  font: var(--font-weight--light) var(--font-size--base) / 1.6 var(--font-family--secondary);
  & > * {
    margin: 0 0 0 var(--spacer-xs);
  }
}
.action {
  margin: var(--spacer-xl) 0 var(--spacer-xl) 0;
}
.checkbox {
  margin-bottom: var(--spacer-2xl);
}
.bottom {
  text-align: center;
  margin-bottom: var(--spacer-lg);
  font-size: var(--h3-font-size);
  font-weight: var(--font-weight--semibold);
  font-family: var(--font-family--secondary);
  &__paragraph {
    color: var(--c-primary);
    margin: 0 0 var(--spacer-base) 0;
    @include for-desktop {
      margin: 0;
    }
  }
}
</style>
