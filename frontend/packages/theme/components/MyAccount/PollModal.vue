<template>
  <SfModal
    v-e2e="'poll-modal'"
    :visible="isPollModalOpen"
    class="modal"
    @close="togglePollModal"
  >
    <template #modal-bar>
      <SfBar
        class="sf-modal__bar smartphone-only"
        :close="true"
        :title="currentPoll?`Editing ${currentPoll.name.toUpperCase()}`:'New Poll'"
        @click:close="togglePollModal"
      />
    </template>
    <transition name="sf-fade" mode="out-in">
      <SfTabs :open-tab="1">
        <SfTab :title="currentPoll?`Editing ${currentPoll.name.toUpperCase()}`:'New Poll'">
          <div>
            <ValidationObserver v-slot="{ handleSubmit }" key="log-in">
              <div class="form">
<!--                <ValidationProvider rules="required" v-slot="{ errors }">
                  <SfSelect label="Category" v-model="form.category" v-e2e="'listing-modal-category'"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]" :disabled="!!currentPoll" required @input="onCategoryChange">
                    <SfSelectOption value=""></SfSelectOption>
                    <SfSelectOption v-for="category in leafCategories" :key="category.id" :value="category.id">{{category.slug}}</SfSelectOption>
                  </SfSelect>
                </ValidationProvider>-->
                <ValidationProvider rules="required|min:2|alpha_dash" v-slot="{ errors }">
                  <SfInput
                    v-model="form.topic"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="name"
                    label="Poll Topic, Cannot be Changed Later"
                    class="form__element"
                    :disabled="!!currentPoll"
                  />
                </ValidationProvider>
                <ValidationProvider rules="min:2|alpha_dash" v-slot="{ errors }">
                  <SfInput
                    v-model="form.id"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="id"
                    label="(Optional) Custom Poll ID for Shorthand URL, Cannot be Changed Later"
                    class="form__element"
                    :disabled="!!currentPoll"
                  />
                </ValidationProvider>
                <ValidationProvider rules="min:2|alpha_dash" v-slot="{ errors }">
                  <SfInput
                    v-model="form.description"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="description"
                    label="(Optional) Description"
                    class="form__element"
                  />
                </ValidationProvider>
                <ValidationProvider rules="required" v-slot="{ errors }">
                  <SfInput
                    v-model="form.dateFinish"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="name"
                    type="date"
                    label="End Date"
                    class="form__element"
                    :disabled="!!currentPoll"
                  />
                </ValidationProvider>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isMultiple"
                      value="false"
                      label="Single Choice"
                      details="Voter can only choose one option, this cannot be changed later"
                      v-model="form.isMultiple"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                    <SfRadio
                      name="isMultiple"
                      value="true"
                      label="Multiple Choice"
                      details="Voter can choose options up to the limit below, this cannot be changed later"
                      v-model="form.isMultiple"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                  </ValidationProvider>
                </div>
                <div v-if="form.isMultiple === 'true'">
                  <ValidationProvider rules="integer|min_value:0"  v-slot="{ errors }">
                    <SfInput
                      v-model="form.maxOptions"
                      :valid="!errors[0]"
                      :errorMessage="errors[0]"
                      name="maxOptions"
                      label="Maximum Options for a Vote, Cannot be Changed Later"
                      type="number"
                      step=1.0
                      class="form__element"
                      :disabled="!!currentPoll"
                    />
                  </ValidationProvider>
                </div>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isAnonymous"
                      value="true"
                      label="Anonymous Votes"
                      details="Voter IDs will be anonymized"
                      v-model="form.isAnonymous"
                      @change="onIsPerpetualChange(form.isAnonymous)"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                    <SfRadio
                      name="isAnonymous"
                      value="false"
                      label="Named Votes"
                      details="Voter IDs will be plain Numerai usernames"
                      v-model="form.isAnonymous"
                      @change="onIsPerpetualChange(form.isAnonymous)"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                  </ValidationProvider>
                </div>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isBlind"
                      value="true"
                      label="Blind Results"
                      details="Results will be kept blind until poll ends"
                      v-model="form.isBlind"
                      class="form__radio"
                    />
                    <SfRadio
                      name="isBlind"
                      value="false"
                      label="Observable Results"
                      details="Results will be visible to voters anytime"
                      v-model="form.isBlind"
                      class="form__radio"
                    />
                  </ValidationProvider>
                </div>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="weightMode"
                      value="equal"
                      label="Equal Weights"
                      details="Equal weights for all voters"
                      v-model="form.weightMode"
                      class="form__radio"
                    />
                    <SfRadio
                      name="weightMode"
                      value="log"
                      label="Log Weighted"
                      details="Log-transformed weights by NMR stake or balance"
                      v-model="form.weightMode"
                      class="form__radio"
                    />
                    <SfRadio
                      name="weightMode"
                      value="log_clip"
                      label="Log Weighted with Clipping"
                      details="Log-transformed weights by NMR stake or balance, clipped by min or max weight"
                      v-model="form.weightMode"
                      class="form__radio"
                    />
                  </ValidationProvider>
                </div>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isNumeraiOnly"
                      value="stake"
                      label="Numerai Staked Only"
                      details="Weighting based only on staked NMR amount in Numerai accounts"
                      v-model="form.isNumeraiOnly"
                      class="form__radio"
                    />
                    <SfRadio
                      name="isNumeraiOnly"
                      value="numerai_total"
                      label="Numerai Total Balance"
                      details="Weighting based on all available NMR amount in Numerai accounts"
                      v-model="form.isNumeraiOnly"
                      class="form__radio"
                    />
                    <SfRadio
                      name="isNumeraiOnly"
                      value="total"
                      label="Total Balance"
                      details="Weighting based on available NMR amount in any wallet (Coming soon)"
                      v-model="form.isNumeraiOnly"
                      class="form__radio"
                      disabled
                    />
                  </ValidationProvider>
                </div>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isStakePredetermined"
                      value="true"
                      label="Pre-determine Stake"
                      details="NMR stake and balance will be snapshotted before poll creation, this cannot be changed later"
                      v-model="form.isStakePredetermined"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                    <SfRadio
                      name="isStakePredetermined"
                      value="false"
                      label="Post-determine Stake"
                      details="NMR stake and balance will be snapshotted after poll ends, this cannot be changed later"
                      v-model="form.isStakePredetermined"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                  </ValidationProvider>
                </div>
                <ValidationProvider rules="integer|min_value:0"  v-slot="{ errors }">
                  <SfInput
                    v-model="form.maxOptions"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="maxOptions"
                    label="Minimum Staked & Resolved Rounds Required for Voter"
                    type="number"
                    step=1.0
                    class="form__element"
                    :disabled="!!currentPoll"
                  />
                </ValidationProvider>
                <ProductOptionsForm
                  ref="optionsForm"
                  optionsTabTitle="Poll options"
                  changeOptionTabTitle="Update option"
                  :options="form.options"
                  transition="sf-fade"
                  changeOptionDescription="Update pricing option."
                  changeButtonText="Change"
                  deleteButtonText="Delete"
                  addNewOptionButtonText="Add new option"
                  updateOptionButtonText="Update option"
                  selectLabel="Country"
                  optionsTabDescription="Manage all the pricing options, the first one will be the default for buyers. Please save the overall form after modifying options."
                  :user="user"
                  :category="form.category"
                  :isTournamentCategory="isTournamentCategory(form.category)"
                  :isSubmissionCategory="isSubmissionCategory(form.category)"
                  :isPerRoundCategory="isPerRoundCategory(form.category)"
                ></ProductOptionsForm>
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
                  v-if="!currentPoll"
                  @click="handleSubmit(handleProductForm)"
                >
                  <SfLoader :class="{ loader: loading }" :loading="loading">
                    <div>{{ $t('Save') }}</div>
                  </SfLoader>
                </SfButton>
                <div class="form__horizontal" v-if="!!currentPoll">
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
import { SfModal, SfTabs, SfInput, SfTextarea, SfSelect, SfButton, SfCheckbox, SfLoader, SfAlert, SfBar, SfRadio, SfBadge } from '@storefront-ui/vue';
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
  message: 'This must be greater than 1'
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
  name: 'PollModal',
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
        this.form.options = (this.currentPoll?.options ? this.currentPoll?.options : (this.form?.options || [])).filter((option) => {
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
        this.form.wallet = this.currentPoll ? this.currentPoll.wallet : null;
        this.form.mode = this.currentPoll?.mode || 'file';
        this.form.stakeLimit = this.currentPoll?.stake_limit;
      } else {
        this.form.currency = 'USD';
        this.form.wallet = null;
        this.form.mode = null;
        this.form.stakeLimit = null;
      }
    },
    onIsPerpetualChange(isAnonymous) {
      if (isAnonymous === 'true') {
        this.form.expirationRound = null;
      } else {
        this.form.expirationRound = productGetters.getExpirationRound(this.currentPoll) || this.globals.selling_round;
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
  setup() {
    const { isPollModalOpen, currentPoll, togglePollModal } = useUiState();
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
      // price: product ? productGetters.getPrice(product).regular : null,
      category: product ? productGetters.getCategoryIds(product)[0] : null,
      description: product ? productGetters.getDescription(product) : null,
      avatar: product ? productGetters.getCoverImage(product) : null,
      isMultiple: product ? String(productGetters.getIsActive(product)) : 'true',
      isAnonymous: String(productGetters.getExpirationRound(product) === null),
      expirationRound: productGetters.getExpirationRound(product),
      // isOnPlatform: product ? String(product.is_on_platform) : 'true',
      // currency: product ? product.currency : 'NMR',
      // wallet: product ? product.wallet : null,
      // mode: product ? product.mode : 'file',
      // stakeLimit: product ? product.stake_limit : null,
      // thirdPartyUrl: product ? product.third_party_url : null,
      options: product ? product.options : []
    });
    const form = ref(resetForm(currentPoll));

    const error = reactive({
      listingModal: null
    });

    const resetErrorValues = () => {
      error.listingModal = null;
    };

    watch(currentPoll, (product) => {
      if (currentPoll) {
        form.value = resetForm(product);
        resetErrorValues();
      }
    });

    const handleForm = (fn) => async () => {
      resetErrorValues();
      await fn({ id: currentPoll.value ? currentPoll.value.id : null, product: form.value });

      const hasProductErrors = productError.value.listingModal;
      if (hasProductErrors) {
        error.listingModal = productError.value.listingModal?.message;
        return;
      }

      togglePollModal();

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
      if (!currentPoll.value) {
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
      isPollModalOpen,
      currentPoll,
      togglePollModal,
      userGetters,
      globals,
      numerai: computed(() => numerai ? numerai.value : null),
      numeraiError,
      leafCategories: computed(() => categories ? categories.value.filter((category) => {
        return category.items.length === 0;
      }).sort((a, b) => -a.slug.localeCompare(b.slug)) : []),
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
