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
                    <SfSelectOption v-for="model in numerai.models" :key="model.name" :value="model.name">{{model.name}}</SfSelectOption>
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
                <ValidationProvider rules="required|decimal|min_value:0" v-slot="{ errors }">
                  <SfInput
                    v-e2e="'listing-modal-price'"
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
                  />
                </ValidationProvider>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="ListingPlatform"
                      value="onPlatform"
                      label="On-Platform"
                      details="Sell natively on NumerBay for cryptocurrency"
                      description="[Coming Soon]"
                      disabled=""
                      selected=""
                      class="form__radio"
                    />
                    <SfRadio
                      name="ListingPlatform"
                      value="offPlatform"
                      label="Off-Platform"
                      details="Link to 3rd-party platforms"
                      description=""
                      disabled=""
                      selected="offPlatform"
                      class="form__radio"
                    />
                  </ValidationProvider>
                </div>
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
                  :disabled="loading"
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
                    :disabled="loading"
                  >
                    <SfLoader :class="{ loader: loading }" :loading="loading">
                      <div>{{ $t('Save') }}</div>
                    </SfLoader>
                  </SfButton>
                  <SfButton v-e2e="'listing-modal-submit'"
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
import { SfModal, SfTabs, SfInput, SfTextarea, SfSelect, SfButton, SfCheckbox, SfLoader, SfAlert, SfBar, SfRadio } from '@storefront-ui/vue';
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
// eslint-disable-next-line camelcase
import { required, email, min_value } from 'vee-validate/dist/rules';
import { userGetters, useUser, productGetters, useCategory, useProduct, useNumerai } from '@vue-storefront/numerbay';
import { onSSR } from '@vue-storefront/core';
import { useUiState } from '~/composables';

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
  setup() {
    const { isListingModalOpen, currentListing, toggleListingModal } = useUiState();
    const { categories, search: categorySearch } = useCategory();
    const { search: productSearch, createProduct, updateProduct, deleteProduct, loading, error: productError } = useProduct('products');
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
      productError,
      loading,
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
</style>
