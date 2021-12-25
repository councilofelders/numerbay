<template>
  <SfModal
    v-e2e="'listing-modal'"
    :persistent="true"
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
              <div class="form">
                <ValidationProvider rules="required" v-slot="{ errors }">
                  <SfSelect label="Category" v-model="form.category" v-e2e="'listing-modal-category'"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]" :disabled="!!currentListing" required @input="onCategoryChange">
                    <SfSelectOption value=""></SfSelectOption>
                    <SfSelectOption v-for="category in leafCategories" :key="category.id" :value="category.id">{{category.slug}}</SfSelectOption>
                  </SfSelect>
                </ValidationProvider>
                <ValidationProvider rules="required" v-slot="{ errors }" v-if="isTournamentCategory(form.category)">
                  <SfSelect label="Model Name" v-model="form.name" v-e2e="'listing-modal-name'"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]" required :disabled="!!currentListing || !form.category" @input="populateModelInfo">
                    <SfSelectOption value=""></SfSelectOption>
                    <SfSelectOption v-for="model in getFilteredModels(form.category)" :key="`${model.tournament}-${model.name}`" :value="`${model.name}`">{{model.name}}</SfSelectOption>
                  </SfSelect>
                </ValidationProvider>
                <ValidationProvider rules="required|min:2|alpha_dash" v-slot="{ errors }" v-else>
                  <SfInput
                    v-model="form.name"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="name"
                    label="Product Name"
                    class="form__element"
                    :disabled="!!currentListing"
                  />
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
<!--                <SfCheckbox v-model="form.hasFeaturedProducts" name="coupon">
                  <template #label>
                    <div class="sf-checkbox__label">
                      Feature my other products
                    </div>
                  </template>
                </SfCheckbox>-->
<!--                <div v-if="form.hasFeaturedProducts">-->
                <multiselect ref="featuredProductsMultiSelect" placeholder="(Optional) Featured Products" v-model="form.featuredProducts" class="multiselect"
                                 :options="groupedProducts" :multiple="true" :close-on-select="false" group-values="products" group-label="category" :group-select="true" track-by="id" label="sku"
                >
                  <template slot="option" slot-scope="props">
                    <span>{{ props.option.$isLabel ? props.option.$groupLabel : props.option.name }}</span>
                  </template>
                </multiselect>
<!--                </div>-->
                <ProductOptionsForm
                  ref="optionsForm"
                  optionsTabTitle="Pricing options"
                  changeOptionTabTitle="Update option"
                  :options="form.options"
                  transition="sf-fade"
                  changeOptionDescription="Update pricing option."
                  changeButtonText="Change"
                  deleteButtonText="Delete"
                  addNewOptionButtonText="Add new option"
                  updateOptionButtonText="Update option"
                  optionsTabDescription="Manage all the pricing options, the first one will be the default for buyers. Please save the overall form after modifying options."
                  :user="user"
                  :category="form.category"
                  :isTournamentCategory="isTournamentCategory(form.category)"
                  :isSubmissionCategory="isSubmissionCategory(form.category)"
                  :isPerRoundCategory="isPerRoundCategory(form.category)"
                  :groupedProducts="groupedProducts"
                ></ProductOptionsForm>
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
                  :disabled="loading || !!numeraiError.getModels || !(form.options && form.options.length > 0)"
                  v-if="!currentListing"
                  @click="handleSubmit(handleProductForm)"
                >
                  <SfLoader :class="{ loader: loading }" :loading="loading">
                    <div>{{ $t('Save') }}</div>
                  </SfLoader>
                </SfButton>
                <div class="form__horizontal" v-if="!!currentListing">
                  <SfButton v-e2e="'listing-modal-submit'"
                    type="submit"
                    class="sf-button form__button"
                    :disabled="loading || !!numeraiError.getModels || !(form.options && form.options.length > 0)"
                    @click="handleSubmit(handleProductForm)"
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
              </div>
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
import { ref, watch, reactive, computed } from '@vue/composition-api';
import { SfModal, SfTabs, SfInput, SfSelect, SfButton, SfLoader, SfBar, SfRadio, SfBadge, SfCheckbox } from '@storefront-ui/vue';
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
// eslint-disable-next-line camelcase
import { required, min_value, integer, min, alpha_dash } from 'vee-validate/dist/rules';
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
import ProductOptionsForm from '~/components/ProductOptionsForm';

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

extend('min', {
  ...min,
  message: 'The field should have at least {length} characters'
});

extend('alpha_dash', {
  // eslint-disable-next-line camelcase
  ...alpha_dash,
  message: 'The field should only contain alphabetic characters, numbers, dashes or underscores'
});

export default {
  name: 'ListingModal',
  components: {
    SfModal,
    SfTabs,
    SfInput,
    SfSelect,
    SfButton,
    SfLoader,
    SfBar,
    SfRadio,
    SfBadge,
    SfCheckbox,
    ProductOptionsForm,
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
        placeholder: 'Product Description'
      }
    };
  },
  methods: {
    isSubmissionCategory(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c=>c.id === Number(categoryId))[0];
        return category?.is_submission;
      }
      return false;
    },
    isPerRoundCategory(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c=>c.id === Number(categoryId))[0];
        return category?.is_per_round;
      }
      return false;
    },
    isTournamentCategory(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c=>c.id === Number(categoryId))[0];
        if (Boolean(category) && Boolean(category.tournament)) {
          return true;
        }
      }
      return false;
    },
    onCategoryChange(categoryId) {
      const category = this.leafCategories.filter(c=>c.id === Number(categoryId))[0];

      if (category) {
        this.form.options = (this.currentListing?.options ? this.currentListing?.options : (this.form?.options || [])).filter((option) => {
          if (!category.tournament) {
            this.$refs.optionsForm.isOnPlatform = 'false';
            return !option.is_on_platform;
          }
          if (option.is_on_platform && !category.is_submission) {
            this.$refs.optionsForm.mode = 'file';
            return option.mode === 'file';
          }
          return true;
        });
      }
    },
    getFilteredModels(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c=>c.id === Number(categoryId))[0];
        let tournament = 8;
        if (category.slug.startsWith('signals-')) {
          tournament = 11;
        }
        const models = userGetters.getModels(this.numerai, tournament, false);
        return models;
      }
      return [];
    },
    onPlatformChange(isOnPlatform) {
      if (isOnPlatform === 'true') {
        this.form.currency = 'NMR';
        this.form.wallet = this.currentListing ? this.currentListing.wallet : null;
        this.form.mode = this.currentListing?.mode || 'file';
        this.form.stakeLimit = this.currentListing?.stake_limit;
      } else {
        this.form.currency = 'USD';
        this.form.wallet = null;
        this.form.mode = null;
        this.form.stakeLimit = null;
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
        this.form.avatar = encodeURI(decodeURI(this.form.avatar));
      }
      if (this.form.thirdPartyUrl) {
        this.form.thirdPartyUrl = encodeURI(decodeURI(this.form.thirdPartyUrl));
      }
    }
  },
  beforeDestroy() {
    if (this.$refs.featuredProductsMultiSelect) {
      this.$refs.featuredProductsMultiSelect.deactivate();
    }
  },
  setup() {
    const { isListingModalOpen, currentListing, toggleListingModal } = useUiState();
    const { categories, search: categorySearch } = useCategory();
    const { products, search: productSearch, createProduct, updateProduct, deleteProduct, loading, error: productError } = useProduct('products');
    const { numerai, error: numeraiError } = useNumerai('my-listings');
    const { user } = useUser();
    const { globals } = useGlobals();
    onSSR(async () => {
      await categorySearch();
    });

    const groupProducts = (products) => {
      const groupedProducts = products.reduce((rv, x) => {
        (rv[x.category.slug] = rv[x.category.slug] || []).push(x);
        return rv;
      }, {});
      return Object.keys(groupedProducts).map((key) => ({category: key, products: groupedProducts[key]}));
    };

    const productsData = computed(() => products?.value?.data ? products?.value?.data : []);

    const groupedProducts = computed(() => groupProducts(productsData.value));

    const resetForm = (product) => ({
      name: product ? productGetters.getName(product) : null,
      category: product ? productGetters.getCategoryIds(product)[0] : null,
      description: product ? productGetters.getDescription(product) : null,
      avatar: product ? productGetters.getCoverImage(product) : null,
      isActive: product ? String(productGetters.getIsActive(product)) : 'true',
      isPerpetual: String(productGetters.getExpirationRound(product) === null),
      expirationRound: productGetters.getExpirationRound(product),
      options: product ? product.options : [],
      // hasFeaturedProducts: product?.featured_products?.length > 0,
      featuredProducts: product?.featured_products ? product?.featured_products.map(id => groupedProducts.value.map(gp=>gp.products).flat().find((p)=>parseInt(p.id) === parseInt(String(id)))) : null
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

      await productSearch({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
    };

    const populateModelInfo = async (name) => {
      if (name) {
        const models = numerai.value.models.filter((m)=>m.name === name);
        if (models) {
          const model = models[0];
          if (model.profileUrl) {
            form.value.avatar = encodeURI(decodeURI(model.profileUrl));
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
      }).sort((a, b) => -a.slug.localeCompare(b.slug)) : []),
      products: productsData,
      groupedProducts,
      resetForm,
      populateModelInfo,
      handleProductForm,
      deleteProduct,
      handleDeleteProduct
    };
  }
};
</script>

<style lang="scss" scoped>
.modal {
  --modal-index: 3;
  --overlay-z-index: 3;
  --modal-width: 70%;
  @include for-mobile {
    --modal-width: 100%;
  }
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
    @include for-mobile {
      width: 100%
    }
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
