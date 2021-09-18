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
        :title="currentListing?`Editing ${currentListing.name.toUpperCase()}`:'New Listing'"
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
                  <SfSelect label="Model Name" v-model="form.name" v-e2e="'listing-modal-name'"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]" required :disabled="!!currentListing" @input="populateModelInfo">
                    <SfSelectOption value=""></SfSelectOption>
                    <SfSelectOption value="">========== Numerai Models ==========</SfSelectOption>
                    <SfSelectOption v-for="model in userGetters.getModels(numerai, tournament=8, sortDate=false)" :key="model.name" :value="model.name">{{model.name}}</SfSelectOption>
                    <SfSelectOption value="">========== Signals Models ==========</SfSelectOption>
                    <SfSelectOption v-for="model in userGetters.getModels(numerai, tournament=11, sortDate=false)" :key="model.name" :value="model.name">{{model.name}}</SfSelectOption>
                  </SfSelect>
                </ValidationProvider>
                <!--<ValidationProvider rules="required" v-slot="{ errors }">
                  <SfInput
                    v-e2e="'listing-modal-name'"
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
                  <SfSelect label="Category" v-model="form.category" v-e2e="'listing-modal-category'"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]" :disabled="!!currentListing || !form.name" required>
                    <SfSelectOption value=""></SfSelectOption>
                    <SfSelectOption v-for="category in getFilteredCategories(leafCategories, numerai.models, form.name)" :key="category.id" :value="category.id">{{category.slug}}</SfSelectOption>
                  </SfSelect>
                </ValidationProvider>
                <ValidationProvider rules="secureUrl" v-slot="{ errors }">
                  <SfInput
                    v-e2e="'listing-modal-avatar'"
                    v-model="form.avatar"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="avatar"
                    label="Avatar Image URL (e.g. Numerai avatar img link)"
                    type="url"
                    class="form__element"
                    @change="encodeURL"
                  />
                </ValidationProvider>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isActive"
                      value="true"
                      label="Active"
                      details="People will be able to buy this product"
                      v-model="form.isActive"
                      class="form__radio"
                    />
                    <SfRadio
                      name="isActive"
                      value="false"
                      label="Inactive"
                      details="Buy button will be disabled without deleting the product"
                      v-model="form.isActive"
                      class="form__radio"
                    />
                  </ValidationProvider>
                </div>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isPerpetual"
                      value="true"
                      label="Perpetual Listing"
                      details="Available for all rounds until delisted or deleted"
                      v-model="form.isPerpetual"
                      @change="onIsPerpetualChange(form.isPerpetual)"
                      class="form__radio"
                    />
                    <SfRadio
                      name="isPerpetual"
                      value="false"
                      label="Temporary Listing"
                      details="Available until specified round"
                      v-model="form.isPerpetual"
                      @change="onIsPerpetualChange(form.isPerpetual)"
                      class="form__radio"
                    />
                  </ValidationProvider>
                </div>
                <div v-if="form.isPerpetual === 'false'">
                  <ValidationProvider rules="integer|min_value:0"  v-slot="{ errors }">
                    <SfInput
                      v-e2e="'listing-modal-avatar'"
                      v-model="form.expirationRound"
                      :valid="!errors[0]"
                      :errorMessage="errors[0]"
                      name="expirationRound"
                      label="Round after which this product is delisted"
                      type="number"
                      step=1.0
                      class="form__element"
                    />
                  </ValidationProvider>
                </div>
                <div class="form__radio-group">
                  <!--todo turnkey rollout-->
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isOnPlatform"
                      value="true"
                      label="On-Platform"
                      details="Sell natively on NumerBay for cryptocurrency"
                      description="Payments are directly sent to you from buyers. You can manage buyers and automate file distribution."
                      v-model="form.isOnPlatform"
                      @change="onPlatformChange(form.isOnPlatform)"
                      class="form__radio"
                    />
                    <SfRadio
                      name="isOnPlatform"
                      value="false"
                      label="Off-Platform"
                      details="Link to 3rd-party platforms"
                      description="Off-Platform reference only. Self-managed."
                      v-model="form.isOnPlatform"
                      @change="onPlatformChange(form.isOnPlatform)"
                      class="form__radio"
                    />
                  </ValidationProvider>
                </div>
                <div v-if="form.isOnPlatform === 'true'">
                  <div class="form__radio-group">
                    <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                      <SfRadio
                        name="currency"
                        value="NMR"
                        label="NMR"
                        :details="`Payments go to your Numerai wallet ${user.numerai_wallet_address} by default`"
                        description="Alternatively, specify a compatible wallet below"
                        v-model="form.currency"
                        class="form__radio"
                      >
                        <template #label>
                          NMR  <SfBadge class="color-primary sf-badge flag">Gas-Free</SfBadge>
                        </template>
                      </SfRadio>
                      <SfRadio
                        name="currency"
                        value="DAI"
                        label="DAI"
                        details="On Polygon"
                        description="[Coming Soon]"
                        disabled
                        class="form__radio"
                      />
                      <!--<SfRadio
                        name="isOnPlatform"
                        value="USDC"
                        label="USDC"
                        v-model="form.currency"
                        class="form__radio"
                      />
                      <SfRadio
                        name="isOnPlatform"
                        value="ETH"
                        label="ETH"
                        v-model="form.currency"
                        class="form__radio"
                      />-->
                    </ValidationProvider>
                  </div>
                  <ValidationProvider v-slot="{ errors }">
                    <SfInput
                      v-e2e="'listing-modal-price'"
                      v-model="form.wallet"
                      :valid="!errors[0]"
                      :errorMessage="errors[0]"
                      name="price"
                      :label="`(Optional) Alternative Wallet for Receiving Payments`"
                      class="form__element"
                    />
                  </ValidationProvider>
                  <ValidationProvider rules="required|decimal|min_value:0" v-slot="{ errors }">
                    <SfInput
                      v-e2e="'listing-modal-price'"
                      v-model="form.price"
                      :valid="!errors[0]"
                      :errorMessage="errors[0]"
                      name="price"
                      :label="`Price (per round equivalent, in ${form.currency})`"
                      type="number"
                      step=0.0001
                      min=0
                      class="form__element"
                    />
                  </ValidationProvider>
                </div>
                <div v-else>
                  <ValidationProvider rules="required|decimal|min_value:0" v-slot="{ errors }">
                    <SfInput
                      v-e2e="'listing-modal-price'"
                      v-model="form.price"
                      :valid="!errors[0]"
                      :errorMessage="errors[0]"
                      name="price"
                      label="Price (per round equivalent, in $USD)"
                      type="number"
                      step=0.01
                      min=0
                      class="form__element"
                    />
                  </ValidationProvider>
                  <ValidationProvider rules="url" v-slot="{ errors }">
                    <SfInput
                      v-e2e="'listing-modal-thirdPartyUrl'"
                      v-model="form.thirdPartyUrl"
                      :valid="!errors[0]"
                      :errorMessage="errors[0]"
                      name="thirdPartyUrl"
                      label="Third Party Listing URL (e.g. Gumroad product link)"
                      type="url"
                      class="form__element"
                      @change="encodeURL"
                    />
                  </ValidationProvider>
                </div>
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
                    v-e2e="'listing-modal-description'"
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
                <div v-if="error.listingModal">
                  {{ error.listingModal }}
                </div>
                <SfButton v-e2e="'listing-modal-submit'"
                  type="submit"
                  class="sf-button--full-width"
                  :disabled="loading || !!numeraiError.getModels"
                  v-if="!currentListing"
                >
                  <SfLoader :class="{ loader: loading }" :loading="loading">
                    <div>{{ $t('Save') }}</div>
                  </SfLoader>
                </SfButton>
                <div class="form__horizontal" v-if="!!currentListing">
                  <SfButton v-e2e="'listing-modal-submit'"
                    type="submit"
                    class="sf-button form__button"
                    :disabled="loading || !!numeraiError.getModels"
                  >
                    <SfLoader :class="{ loader: loading }" :loading="loading">
                      <div>{{ $t('Save') }}</div>
                    </SfLoader>
                  </SfButton>
                  <SfButton v-e2e="'listing-modal-submit'"
                    type="button"
                    class="sf-button color-danger"
                    :disabled="loading || !!numeraiError.getModels"
                    @click="handleDeleteProduct"
                  >
                    <SfLoader :class="{ loader: loading }" :loading="loading">
                      <div>{{ $t('Deactivate') }}</div>
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
import { SfModal, SfTabs, SfInput, SfTextarea, SfSelect, SfButton, SfCheckbox, SfLoader, SfAlert, SfBar, SfRadio, SfBadge } from '@storefront-ui/vue';
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
// eslint-disable-next-line camelcase
import { required, min_value, integer } from 'vee-validate/dist/rules';
import {
  userGetters,
  useUser,
  productGetters,
  useCategory,
  useProduct,
  useNumerai,
  useGlobals
} from '@vue-storefront/numerbay';
import { onSSR } from '@vue-storefront/core';
import { useUiState } from '~/composables';

extend('required', {
  ...required,
  message: 'This field is required'
});

extend('min_value', {
  // eslint-disable-next-line camelcase
  ...min_value,
  message: 'This must be positive'
});

extend('integer', {
  ...integer,
  message: 'This field must be an integer'
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

extend('secureUrl', {
  validate: (value) => {
    if (value) {
      // eslint-disable-next-line
      return /^(https:\/\/www\.|https:\/\/)[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(value);
    }

    return false;
  },
  message: 'This must be a valid HTTPS URL'
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
    SfBar,
    SfRadio,
    SfBadge,
    ValidationProvider,
    ValidationObserver
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
  methods: {
    onPlatformChange(isOnPlatform) {
      if (isOnPlatform === 'true') {
        this.form.currency = 'NMR';
        this.form.wallet = this.currentListing ? this.currentListing.wallet : null;
      } else {
        this.form.currency = 'USD';
        this.form.wallet = null;
      }
    },
    onIsPerpetualChange(isPerpetual) {
      if (isPerpetual === 'true') {
        this.form.expirationRound = null;
      } else {
        this.form.expirationRound = productGetters.getExpirationRound(this.currentListing) || this.globals.selling_round;
      }
    },
    encodeURL() {
      if (this.form.avatar) {
        this.form.avatar = encodeURI(this.form.avatar);
      }
      if (this.form.thirdPartyUrl) {
        this.form.thirdPartyUrl = encodeURI(this.form.thirdPartyUrl);
      }
    }
  },
  setup() {
    const { isListingModalOpen, currentListing, toggleListingModal } = useUiState();
    const { categories, search: categorySearch } = useCategory();
    const { search: productSearch, createProduct, updateProduct, deleteProduct, loading, error: productError } = useProduct('products');
    const { numerai, error: numeraiError } = useNumerai('my-listings');
    const { user } = useUser();
    const { globals } = useGlobals();
    onSSR(async () => {
      await categorySearch();
    });

    const resetForm = (product) => ({
      name: product ? productGetters.getName(product) : null,
      price: product ? productGetters.getPrice(product).regular : null,
      category: product ? productGetters.getCategoryIds(product)[0] : null,
      description: product ? productGetters.getDescription(product) : null,
      avatar: product ? productGetters.getCoverImage(product) : null,
      isActive: product ? String(productGetters.getIsActive(product)) : 'true',
      isPerpetual: String(productGetters.getExpirationRound(product) === null),
      expirationRound: productGetters.getExpirationRound(product),
      isOnPlatform: product ? String(product.is_on_platform) : 'true', // todo turnkey rollout
      currency: product ? product.currency : 'NMR',
      wallet: product ? product.wallet : null,
      thirdPartyUrl: product ? product.third_party_url : null
    });
    const form = ref(resetForm(currentListing));

    const error = reactive({
      listingModal: null
    });

    const resetErrorValues = () => {
      error.listingModal = null;
    };

    watch(currentListing, (product) => {
      if (currentListing) {
        form.value = resetForm(product);
        resetErrorValues();
      }
    });

    const handleForm = (fn) => async () => {
      resetErrorValues();
      await fn({ id: currentListing.value ? currentListing.value.id : null, product: form.value });

      const hasProductErrors = productError.value.listingModal;
      if (hasProductErrors) {
        error.listingModal = productError.value.listingModal?.message;
        return;
      }

      toggleListingModal();

      await productSearch({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}});
    };

    const populateModelInfo = async (name) => {
      if (name) {
        const models = numerai.value.models.filter((m)=>m.name === name);
        if (models) {
          const model = models[0];
          if (model.profileUrl) {
            form.value.avatar = model.profileUrl;
          }
        }
      }
    };

    const handleProductForm = async () => {
      if (!currentListing.value) {
        return handleForm(createProduct)();
      } else {
        return handleForm(updateProduct)();
      }
    };

    const handleDeleteProduct = async () => handleForm(deleteProduct)();

    const getFilteredCategories = (categories, numeraiModels, selectedModelName) => {
      if (selectedModelName) {
        const selectedModel = numeraiModels.filter(m=>m.name === selectedModelName)[0];
        const tournament = selectedModel.tournament;
        if (tournament === 8) {
          return categories.filter(c=>c.slug.startsWith('numerai-'));
        } else {
          return categories.filter(c=>c.slug.startsWith('signals-'));
        }
      }
      return categories;
    };

    return {
      form,
      error,
      user,
      productError,
      loading,
      isListingModalOpen,
      currentListing,
      toggleListingModal,
      userGetters,
      globals,
      numerai: computed(() => numerai ? numerai.value : null),
      numeraiError,
      leafCategories: computed(() => categories ? categories.value.filter((category) => {
        return category.items.length === 0;
      }) : []),
      resetForm,
      populateModelInfo,
      handleProductForm,
      deleteProduct,
      handleDeleteProduct,
      getFilteredCategories
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
  &__radio {
    width: 50%;
  }
  &__radio-group {
    flex: 0 0 100%;
    margin: 0 0 var(--spacer-xl) 0;
    @include for-desktop {
      margin: 0 0 var(--spacer-xl) 0;
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
.flag {
  margin-left: 0.4em;
  padding: 0.15em;
}
</style>
