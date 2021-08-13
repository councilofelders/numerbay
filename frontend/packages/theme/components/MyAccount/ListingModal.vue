<template>
  <SfModal
    v-e2e="'listing-modal'"
    :visible="isListingModalOpen"
    class="modal"
    @close="toggleListingModal"
  >
    <template #modal-bar>
      <SfBar
        class="sf-modal__bar smartphone-only"
        :close="true"
        :title="isLogin ? 'Log in' : 'Sign in'"
        @click:close="toggleListingModal"
      />
    </template>
    <transition name="sf-fade" mode="out-in">
      <SfTabs :open-tab="1">
        <SfTab :title="currentListing?`Editing ${currentListing.name.toUpperCase()}`:'New Listing'">
          <div>
            <ValidationObserver v-slot="{ handleSubmit }" key="log-in">
              <form class="form" @submit.prevent="handleSubmit(handleProductForm)">
                <ValidationProvider rules="required" v-slot="{ errors }">
                  <SfSelect label="Name" v-model="form.name"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]" required :disabled="!!currentListing" @input="populateModelInfo">
                    <SfSelectOption value=""></SfSelectOption>
                    <SfSelectOption v-for="model in numerai.models" :key="model.name" :value="model.name">{{model.name}}</SfSelectOption>
                  </SfSelect>
                </ValidationProvider>
                <!--<ValidationProvider rules="required" v-slot="{ errors }">
                  <SfInput
                    v-e2e="'login-modal-username'"
                    v-model="form.name"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="name"
                    label="Name"
                    class="form__element"
                    :disabled="!!currentListing"
                  />
                </ValidationProvider>-->
                <ValidationProvider rules="required" v-slot="{ errors }">
                  <SfSelect label="Category" v-model="form.category"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]" :disabled="!!currentListing" required>
                    <SfSelectOption value=""></SfSelectOption>
                    <SfSelectOption v-for="category in leafCategories" :key="category.id" :value="category.id">{{category.slug}}</SfSelectOption>
                  </SfSelect>
                </ValidationProvider>
                <ValidationProvider rules="required|decimal|min_value:0" v-slot="{ errors }">
                  <SfInput
                    v-e2e="'login-modal-username'"
                    v-model="form.price"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="price"
                    label="Price (in $USD)"
                    type="number"
                    step=any
                    min=0
                    class="form__element"
                  />
                </ValidationProvider>
                <ValidationProvider rules="url" v-slot="{ errors }">
                  <SfInput
                    v-e2e="'login-modal-username'"
                    v-model="form.avatar"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="avatar"
                    label="Avatar Image URL (e.g. Numerai avatar img link)"
                    type="url"
                    class="form__element"
                  />
                </ValidationProvider>
                <ValidationProvider rules="url" v-slot="{ errors }">
                  <SfInput
                    v-e2e="'login-modal-username'"
                    v-model="form.thirdPartyUrl"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="thirdPartyUrl"
                    label="Third Party Listing URL (e.g. Gumroad product link)"
                    type="url"
                    class="form__element"
                  />
                </ValidationProvider>
                <client-only>
                  <div class="editor">
                    <quill-editor
                      ref="descriptionEditor"
                      name="description"
                      v-model="form.description"
                      :options="editorOption"
                    />
                  </div>
                </client-only>
                <!--<ValidationProvider v-slot="{ errors }">
                  <SfTextarea
                    v-e2e="'login-modal-username'"
                    v-model="form.description"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="description"
                    label="Description"
                    class="form__element"
                    :cols="60"
                    :rows="10"
                  />
                </ValidationProvider>-->
                <div v-if="error.login">
                  {{ error.login }}
                </div>
                <SfButton v-e2e="'login-modal-submit'"
                  type="submit"
                  class="sf-button--full-width"
                  :disabled="loading"
                  v-if="!currentListing"
                >
                  <SfLoader :class="{ loader: loading }" :loading="loading">
                    <div>{{ $t('Save') }}</div>
                  </SfLoader>
                </SfButton>
                <div class="form__horizontal" v-if="!!currentListing">
                  <SfButton v-e2e="'login-modal-submit'"
                    type="submit"
                    class="sf-button form__button"
                    :disabled="loading"
                  >
                    <SfLoader :class="{ loader: loading }" :loading="loading">
                      <div>{{ $t('Save') }}</div>
                    </SfLoader>
                  </SfButton>
                  <SfButton v-e2e="'login-modal-submit'"
                    type="button"
                    class="sf-button color-danger"
                    :disabled="loading"
                    @click="handleDeleteProduct"
                  >
                    <SfLoader :class="{ loader: loading }" :loading="loading">
                      <div>{{ $t('Delete') }}</div>
                    </SfLoader>
                  </SfButton>
                </div>
              </form>
            </ValidationObserver>
            <div class="bottom">
            </div>
          </div>
        </SfTab>
      </SfTabs>
    </transition>
  </SfModal>
</template>
<script>
import {ref, watch, reactive, computed} from '@vue/composition-api';
import { SfModal, SfTabs, SfInput, SfTextarea, SfSelect, SfButton, SfCheckbox, SfLoader, SfAlert, SfBar } from '@storefront-ui/vue';
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
// eslint-disable-next-line camelcase
import { required, email, min_value } from 'vee-validate/dist/rules';
import {userGetters, useUser, productGetters, useCategory, useProduct, useNumerai} from '@vue-storefront/numerbay';
import {onSSR, useVSFContext} from '@vue-storefront/core';
import { useUiState } from '~/composables';
import MetamaskButton from '../Molecules/MetamaskButton';
import Web3 from 'web3';

extend('email', {
  ...email,
  message: 'Invalid email'
});

extend('required', {
  ...required,
  message: 'This field is required'
});

extend('min_value', {
  // eslint-disable-next-line camelcase
  ...min_value,
  message: 'This must be positive'
});

extend('decimal', {
  validate: (value, { decimals = '*', separator = '.' } = {}) => {
    if (value === null || value === undefined || value === '') {
      return {
        valid: false
      };
    }
    if (Number(decimals) === 0) {
      return {
        valid: /^-?\d*$/.test(value)
      };
    }
    const regexPart = decimals === '*' ? '+' : `{1,${decimals}}`;
    const regex = new RegExp(`^[-+]?\\d*(\\${separator}\\d${regexPart})?([eE]{1}[-]?\\d+)?$`);

    return {
      valid: regex.test(value)
    };
  },
  message: 'The {_field_} field must contain only decimal values'
});

extend('url', {
  validate: (value) => {
    if (value) {
      // eslint-disable-next-line
      return /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(value);
    }

    return false;
  },
  message: 'This must be a valid URL'
});

export default {
  name: 'ListingModal',
  components: {
    SfModal,
    SfTabs,
    SfInput,
    SfTextarea,
    SfSelect,
    SfButton,
    SfCheckbox,
    SfLoader,
    SfAlert,
    ValidationProvider,
    ValidationObserver,
    SfBar,
    MetamaskButton
  },
  data () {
    return {
      editorOption: {
        theme: 'snow',
        modules: {
          toolbar: {
            container: [
              ['bold', 'italic', 'underline', 'strike'],
              ['blockquote', 'code-block'],
              [{ list: 'ordered' }, { list: 'bullet' }],
              [{ indent: '-1' }, { indent: '+1' }],
              [{ header: [1, 2, 3, 4, 5, 6, false] }],
              [{ color: [] }, { background: [] }],
              [{ font: [] }],
              ['link']
            ]
          }
        },
        placeholder: 'Description'
      }
    };
  },
  setup() {
    const { isListingModalOpen, currentListing, toggleListingModal } = useUiState();
    const { categories, search: categorySearch } = useCategory();
    const { search: productSearch } = useProduct('products');
    const { numerai } = useNumerai();
    const { user } = useUser();
    onSSR(async () => {
      await categorySearch();
    });

    const resetForm = (product) => ({
      name: product ? productGetters.getName(product) : null,
      price: product ? productGetters.getPrice(product).regular : null,
      category: product ? productGetters.getCategoryIds(product)[0] : null,
      description: product ? productGetters.getDescription(product) : null,
      avatar: product ? productGetters.getCoverImage(product) : null,
      thirdPartyUrl: product ? product.third_party_url : null
      // email: productGetters.getEmailAddress(currentListing),
      // publicAddress: productGetters.getPublicAddress(currentListing),
      // nonce: productGetters.getNonce(currentListing)
    });
    const form = ref(resetForm(currentListing));

    const isLogin = ref(true);
    // const createAccount = ref(false);
    // const rememberMe = ref(false);
    const { load, loading, setUser, error: userError } = useUser();

    const error = reactive({
      login: null,
      register: null
    });

    const resetErrorValues = () => {
      error.login = null;
      error.register = null;
    };

    watch(currentListing, (product) => {
      if (currentListing) {
        form.value = resetForm(product);
        resetErrorValues();
      }
    });

    const setIsLoginValue = (value) => {
      resetErrorValues();
      isLogin.value = value;
    };

    const handleForm = (fn) => async () => {
      resetErrorValues();
      await fn({ product: form.value });

      // const hasUserErrors = userError.value.register || userError.value.login;
      // if (hasUserErrors) {
      //   error.login = userError.value.login?.message;
      //   error.register = userError.value.register?.message;
      //   return;
      // }
      toggleListingModal();
      // await setUser(load());
      await productSearch({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}});
    };

    const populateModelInfo = async (name) => {
      if (name) {
        const models = numerai.value.models.filter((m)=>m.name === name);
        if (models) {
          const model = models[0];
          if (model.profileUrl) {
            console.log('setavatar: ', model.profileUrl);
            form.value.avatar = model.profileUrl;
          }
        }
      }
    };

    const vsfContext = useVSFContext();

    const createProduct = async ({product}) => {
      console.log('createProduct:', product);
      const response = await vsfContext.$numerbay.api.createProduct(product);
      console.log('createProduct response:', JSON.stringify(response));
    };

    const updateProduct = async ({product}) => {
      product.id = currentListing.value.id;
      console.log('updateProduct:', product);
      const response = await vsfContext.$numerbay.api.updateProduct(product);
      console.log('updateProduct response:', JSON.stringify(response));
    };

    const deleteProduct = async () => {
      const response = await vsfContext.$numerbay.api.deleteProduct({id: currentListing.value.id});
      console.log('deleteProduct response:', JSON.stringify(response));
    };

    const handleProductForm = async () => {
      if (!currentListing.value) {
        return handleForm(createProduct)();
      } else {
        return handleForm(updateProduct)();
      }
    };

    const handleDeleteProduct = async () => handleForm(deleteProduct)();

    const onPublicAddressChange = async (publicAddress, providerEthers, callback) => {
      // console.log('onPublicAddressChange: ', publicAddress, providerEthers);
      if (publicAddress) {
        try {
          // get nonce from backend
          console.log('get nonce...');
          const { nonce } = await vsfContext.$numerbay.api.logInGetNonce({
            publicAddress: publicAddress
          });
          console.log('nonce: ', nonce);

          // web3 lib instance
          const web3 = new Web3(providerEthers.provider);
          const signaturePromise = web3.eth.personal.sign(
            `I am signing my one-time nonce: ${nonce}`,
            publicAddress,
            // MetaMask will ignore the password argument here
            '',
            callback
          );

          // login with the signature
          signaturePromise.then(async (signature)=>{
            const response = await vsfContext.$numerbay.api.logInGetTokenWeb3({
              publicAddress: publicAddress,
              signature: signature
            });
            toggleListingModal();
            await setUser(load());
            console.log('login web3 response:', JSON.stringify(response));
            return response;
          });

        } catch (err) {
          console.log(err);
          throw new Error(
            'You need to sign the message to be able to log in.'
          );

        }
      }
    };

    return {
      form,
      error,
      userError,
      loading,
      isLogin,
      isListingModalOpen,
      currentListing,
      toggleListingModal,
      numerai: computed(() => numerai ? numerai.value : null),
      leafCategories: computed(() => categories ? categories.value.filter((category) => {
        return category.items.length === 0;
      }) : []),
      resetForm,
      populateModelInfo,
      handleProductForm,
      deleteProduct,
      handleDeleteProduct,
      setIsLoginValue,
      onPublicAddressChange
    };
  }
};
</script>

<style lang="scss" scoped>

.modal {
  --modal-index: 3;
  --overlay-z-index: 3;
  --modal-width: 50%;
}
.form {
  margin-top: var(--spacer-sm);
  &__button {
    display: block;
    width: 100%;
    @include for-desktop {
      width: 17.5rem;
    }
  }
  &__element {
    margin: 0 0 var(--spacer-xl) 0;
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
.editor {
  margin: 0 0 var(--spacer-xl) 0;
  height: 300px;
  .quill-editor {
    height: 250px;
  }
}
</style>
