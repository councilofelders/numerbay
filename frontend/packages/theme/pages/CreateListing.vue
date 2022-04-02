<template>
<div class="page-wrap">
    <!-- create -->
    <section class="create-section section-space-b pt-4 pt-md-5 mt-md-4">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="section-head-sm">
                        <router-link :to="`/listings`" class="btn-link fw-semibold"><em class="ni ni-arrow-left"></em> My listings</router-link>
                        <h1 class="mt-2">{{ !id ? `Create new listing` : `Edit listing`}}</h1>
                    </div>
                </div><!-- end col -->
                <div class="col-lg-8">
                    <ValidationObserver v-slot="{ handleSubmit }">
                    <form action="#" class="form-create mb-5 mb-lg-0">
                        <ValidationProvider rules="required" v-slot="{ errors }" slim>
                        <div class="form-item mb-4">
                            <h5 class="mb-1" :class="{ 'text-danger': Boolean(errors[0]) }">Choose category</h5>
                            <p class="form-text mb-3" :class="{ 'text-danger': Boolean(errors[0]) }">Select the category of listing. This cannot be changed later.</p>
                            <v-select class="generic-select" :class="!errors[0] ? '' : 'is-invalid'" placeholder="Select Category" label="slug" v-model="form.category" :options="leafCategories" :reduce="option => option.id" :disabled="Boolean(currentListing)" :clearable=false @input="onCategoryChange"></v-select>
                            <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                        </div><!-- end form-item -->
                        </ValidationProvider>
                        <ValidationProvider rules="required" v-slot="{ errors }" v-if="isTournamentCategory(form.category)" slim>
                        <div class="form-item mb-4">
                            <h5 class="mb-1" :class="{ 'text-danger': Boolean(errors[0]) }">Select model</h5>
                            <p class="form-text mb-3" :class="{ 'text-danger': Boolean(errors[0]) }">Select the tournament model for listing. This cannot be changed later.</p>
                            <v-select class="generic-select" :class="!errors[0] ? '' : 'is-invalid'" placeholder="Select Model" label="name" v-model="form.name" :options="getFilteredModels(form.category)" :reduce="option => option.name"  :disabled="Boolean(currentListing)" :clearable=false @input="populateModelInfo"></v-select>
                            <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                        </div><!-- end form-item -->
                        </ValidationProvider>
                        <ValidationProvider rules="required|min:2|alpha_dash" v-slot="{ errors }" v-else slim>
                        <div class="form-item mb-4">
                            <div class="mb-4">
                                <label class="mb-2 form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Product name</label>
                                <p class="form-text mb-3" :class="{ 'text-danger': Boolean(errors[0]) }">Set the product name. This cannot be changed later.</p>
                                <input type="text" class="form-control form-control-s1"  :class="!errors[0] ? '' : 'is-invalid'" placeholder="Product Name" v-model="form.name" :disabled="Boolean(currentListing)">
                                <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                            </div>
                        </div><!-- end form-item -->
                        </ValidationProvider>
                        <ValidationProvider rules="secureUrl" v-slot="{ errors }" slim>
                        <div class="form-item mb-4">
                            <div class="mb-4">
                                <label class="mb-2 form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Avatar</label>
                                <input type="text" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="Https URL to an image (optional)" v-model="form.avatar" @change="encodeURL">
                                <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                            </div>
                          <object v-if="Boolean(form.avatar)" :data="form.avatar" type="image/png" class="col-xs-12 col-md-3 rounded-3" style="max-width: 100%">
                            <img src="https://numer.ai/img/profile_picture_light.jpg" alt="" class="col-xs-12 col-md-3 rounded-3" style="max-width: 100%">
                          </object>
                        </div><!-- end form-item -->
                        </ValidationProvider>
                        <div class="form-item mb-4">
                            <div class="mb-4">
                                <div class="d-flex align-items-center justify-content-between">
                                    <div class="me-2">
                                        <h5 class="mb-1">Show advanced settings</h5>
                                    </div>
                                    <div class="form-check form-switch form-switch-s1">
                                        <input class="form-check-input" type="checkbox" v-model="showAdvanced">
                                    </div><!-- end form-check -->
                                </div><!-- end d-flex -->
                            </div>
                        </div><!-- end form-item -->
                        <div v-show="showAdvanced">
                          <div class="form-item mb-4">
                              <div class="mb-4">
                                  <div class="d-flex align-items-center justify-content-between">
                                      <div class="me-2">
                                          <h5 class="mb-1">Active for sale</h5>
                                          <p class="form-text">People will be able to buy this product</p>
                                      </div>
                                      <div class="form-check form-switch form-switch-s1">
                                          <input class="form-check-input" type="checkbox" v-model="form.isActive">
                                      </div><!-- end form-check -->
                                  </div><!-- end d-flex -->
                              </div>
                          </div><!-- end form-item -->
                          <div class="form-item mb-4">
                              <div class="mb-4">
                                  <div class="d-flex align-items-center justify-content-between">
                                      <div class="me-2">
                                          <h5 class="mb-1">Auto expiration</h5>
                                          <p class="form-text">Whether to auto delist after a certain tournament round</p>
                                      </div>
                                      <div class="form-check form-switch form-switch-s1">
                                          <input class="form-check-input" data-target="switch-content-expiration" type="checkbox" v-model="form.autoExpiration" @change="onIsPerpetualChange(form.autoExpiration)">
                                      </div><!-- end form-check -->
                                  </div><!-- end d-flex -->
                                  <ValidationProvider rules="required|integer|min_value:0" v-slot="{ errors }" v-if="form.autoExpiration" slim>
                                  <div class="mt-4">
                                      <input type="number" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="Round after which this product will be delisted" min="0" v-model="form.expirationRound">
                                      <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                                  </div>
                                  </ValidationProvider>
                              </div>
                          </div><!-- end form-item -->
                          <div class="form-item mb-4">
                              <div class="mb-4">
                                  <div class="d-flex align-items-center justify-content-between">
                                      <div class="me-2">
                                          <h5 class="mb-1">Use client-side encryption</h5>
                                          <p class="form-text">Upload artifacts for each order and encrypt them in your browser</p>
                                          <a class="link-secondary" href="https://docs.numerbay.ai/updates/encryption" target="_blank">Learn more about encryption</a>
                                      </div>
                                      <div class="form-check form-switch form-switch-s1">
                                          <input class="form-check-input" type="checkbox" v-model="form.useEncryption">
                                      </div><!-- end form-check -->
                                  </div><!-- end d-flex -->
                              </div>
                          </div><!-- end form-item -->
                          <ValidationProvider rules="url" v-slot="{ errors }" slim>
                          <div class="form-item mb-4">
                              <div class="mb-4">
                                  <h5 class="mb-1" :class="{ 'text-danger': Boolean(errors[0]) }">Webhook url</h5>
                                  <p class="form-text mb-3" :class="{ 'text-danger': Boolean(errors[0]) }">Url to call on new sale order. Useful for products using client-side encryption</p>
                                  <input type="text" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="Webhook URL (optional)" v-model="form.webhook" @change="encodeURL">
                                  <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                              </div>
                          </div><!-- end form-item -->
                          </ValidationProvider>
                          <div class="form-item mb-4">
                              <h5 class="mb-1">Featured products</h5>
                              <p class="form-text mb-3">Other products to display in the product page (optional)</p>
                              <client-only>
                                <multiselect ref="featuredProductsMultiSelect" placeholder="" v-model="form.featuredProducts" class="featured-products-multiselect"
                                     :options="groupedProducts" :multiple="true" :close-on-select="false" group-values="products" group-label="category" :group-select="true" track-by="id" label="sku"
                                >
                                  <template slot="option" slot-scope="props">
                                    <span>{{ props.option.$isLabel ? props.option.$groupLabel : props.option.name }}</span>
                                  </template>
                                </multiselect>
                              </client-only>
                          </div><!-- end form-item -->
                        </div>
                        <div class="form-item mb-4">
                          <h5 class="mb-3">Pricing options</h5>
<!--                          {{form.options}}-->
                          <a class="btn" :class="form.options.length > 0 ? 'btn-outline-dark' : 'btn-dark'" @click="changeOption(-1)"><em class="ni ni-plus"></em> New Option</a>
                          <div class="row g-gs mt-1">
                            <div class="col-xl-6" v-for="option in orderedOptions" :key="option.id">
                                <div class="card card-full">
                                    <div class="card-body card-body-s1">
                                        <p class="mb-3 fs-13 mb-4">{{ option.is_on_platform ? `On-platform` : `Off-platform` }}</p>
                                        <div class="card-media mb-3">
                                            <div class="card-media-body">
                                                <h4>{{ productGetters.getOptionFormattedPrice(option, withCurrency=true) }}</h4>
                                                <p class="fw-medium fs-14">{{ option.mode }}{{ option.mode === 'stake_with_limit' ? ` [${productGetters.getStakeLimit(option)}]`: `` }} x {{ option.quantity }}</p>
                                                <p class="fs-15">{{ option.description }}</p>
                                            </div><!-- end card-media-body -->
                                        </div><!-- end card-media -->
                                        <div class="card-media mb-3">
                                            <div class="card-media-body text-truncate">
                                                <span class="fw-medium fs-13">{{ option.is_on_platform ? (option.wallet || 'Numerai wallet') : option.third_party_url }}</span>
                                            </div>
                                        </div><!-- end d-flex -->
                                        <ul class="btns-group">
                                            <li><a href="javascript:void(0);" class="btn-link flex-grow-1 fw-medium fs-13 text-success" @click="changeOption(option.key)">Change</a></li>
                                            <li><a href="javascript:void(0);" class="btn-link flex-grow-1 fw-medium fs-13 text-danger" @click="deleteOption(option.key)">Delete</a></li>
                                        </ul>
                                    </div><!-- end card-body -->
                                </div><!-- end card -->
                            </div><!-- end col -->
                          </div><!-- end row -->
                        </div><!-- end form-item -->
                        <div class="form-item mb-4">
                            <label class="mb-2 form-label">Description</label>
                            <client-only>
                              <div class="mb-4 editor">
                                <quill-editor
                                  ref="descriptionEditor"
                                  name="description"
                                  v-model="form.description"
                                  :options="editorOption"
                                />
                                <input ref="imageInput" class="d-none" type="file" accept="image/*" @change="_doImageUpload" style="display: none">
                              </div>
                            </client-only>
                        </div><!-- end form-item -->
                        <button class="btn btn-dark" type="button" @click="handleSubmit(saveListing)" :disabled="productLoading">
                          <span v-if="productLoading"><span class="spinner-border spinner-border-sm me-2" role="status" ></span>Saving...</span>
                          <span v-else>Save</span>
                        </button>
                    </form>
                    </ValidationObserver>
                </div><!-- endn col -->
            </div><!-- row-->
            <PricingOptionModal
              modalId="pricingOptionModal"
              ref="pricingOptionModal"
              :is-modal-open="isModalOpen"
              :options="form.options"
              :groupedProducts="groupedProducts"
              :isTournamentCategory="isTournamentCategory(form.category)"
              :isSubmissionCategory="isSubmissionCategory(form.category)"
              :isPerRoundCategory="isPerRoundCategory(form.category)"
              :user="user"
              @update:pricing="refresh"
            ></PricingOptionModal>
        </div><!-- container -->
    </section><!-- create-section -->
</div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

// Composables
import { computed, ref } from '@vue/composition-api';
import { onSSR } from '@vue-storefront/core';
import {
  productGetters,
  useCategory,
  useGlobals,
  useNumerai,
  useProduct,
  useUser,
  userGetters
} from '@vue-storefront/numerbay';
import { useUiNotification } from '~/composables';
import axios from 'axios';
import _ from 'lodash';
import {extend} from 'vee-validate';

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
  name: 'CreateListing',
  middleware: [
    'is-authenticated'
  ],
  data () {
    return {
      SectionData,
      selected: 'Select Collection',
      options: [
        'Select Collection',
        'Abstraction',
        'Patternlicious',
        'Skecthify',
        'Cartoonism',
        'Virtuland',
        'Papercut'
      ],
      optionForm: {},
      isModalOpen: false,
      modal: null,
      showAdvanced: false,
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
              ['link', 'image']
            ],
            handlers: {
              image: this.insertImage
            }
          }
        },
        placeholder: 'Product description'
      }
    };
  },
  computed: {
    orderedOptions() {
      if (this.form.options && this.form.options.length > 0) {
        for (let i = 0; i < this.form.options.length; i++) {
          this.form.options[i].key = i;
        }
      }
      return _.orderBy(this.form.options, 'id');
    },
    quillInstance () {
      return this.$refs.descriptionEditor.quill;
    }
  },
  methods: {
    insertImage () {
      // manipulate the DOM to do a click on hidden input
      this.$refs.imageInput.click();
    },
    async _doImageUpload (event) {
      // for simplicity I only upload the first image
      const file = event.target.files[0];
      // create form data
      const fd = new FormData();
      // just add file instance to form data normally
      fd.append('upload_preset', 'numerbay');
      fd.append('file', file);
      // I use axios here, should be obvious enough
      const response = await axios.post(this.imageUpload.url, fd);
      // clear input value to make selecting the same image work
      event.target.value = '';
      // get current index of the cursor
      const currentIndex = this.quillInstance.selection.lastRange.index;
      // insert uploaded image url to 'image' embed (quill does this for you)
      // the embed looks like this: <img src="{url}" />
      this.quillInstance.insertEmbed(currentIndex, 'image', response.data.url);
      // set cursor position to after the image
      this.quillInstance.setSelection(currentIndex + 1, 0);
    },
    encodeURL() {
      if (this.form.avatar) {
        this.form.avatar = encodeURI(decodeURI(this.form.avatar));
      }
    },
    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    onCategoryChange(categoryId) {
      this.form.name = null;
      // const category = this.leafCategories.filter(c=>c.id === Number(categoryId))[0];
      //
      // if (category) {
      //   this.form.options = (this.currentListing?.options ? this.currentListing?.options : (this.form?.options || [])).filter((option) => {
      //     if (!category.tournament) {
      //       this.$refs.optionsForm.isOnPlatform = 'false';
      //       return !option.is_on_platform;
      //     }
      //     if (option.is_on_platform && !category.is_submission) {
      //       this.$refs.optionsForm.mode = 'file';
      //       return option.mode === 'file';
      //     }
      //     return true;
      //   });
      // }
    },
    refresh() {
      this._computedWatchers.orderedOptions.run();
      this.$forceUpdate();
    },
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
    getFilteredModels(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c=>c.id === Number(categoryId))[0];
        let tournament = 8;
        if (category.slug.startsWith('signals-')) {
          tournament = 11;
        }
        return userGetters.getModels(this.numerai, tournament, false);
      }
      return [];
    },
    onIsPerpetualChange(autoExpiration) {
      console.log('change', autoExpiration);
      if (autoExpiration) {
        this.form.expirationRound = this.productGetters.getExpirationRound(this.currentListing) || this.globals?.selling_round;
      } else {
        this.form.expirationRound = null;
      }
    },
    changeOption(index) {
      this.$refs.pricingOptionModal.changeOption(index);
      this.$refs.pricingOptionModal.show();
    },
    deleteOption(index) {
      this.form.options.splice(index, 1);
    },
    // createListing() {
    //
    // },
    // updateListing() {
    //
    // },
    // saveListing() {
    //   if (!this.currentListing) {
    //     this.createListing();
    //   } else {
    //     this.updateListing();
    //   }
    // }
    onProductsLoaded(products) {
      this.currentListing = products?.data?.find((p)=>p.id === parseInt(this.id));
      this.form = this.resetForm(this.currentListing);
      this.showAdvanced = (!this.form.isActive) || (this.form.autoExpiration) || (!this.form.useEncryption) || (Boolean(this.form.featuredProducts) && this.form.featuredProducts.length>0) || (this.form.webhook);
    }
  },
  watch: {
    products(newProducts) {
      // const id = this.$route.params.id;
      this.onProductsLoaded(newProducts);
    }
  },
  mounted () {
    if (this.userGetters.getNumeraiApiKeyPublicId(this.user)) {
      this.getNumeraiModels();
    }

    // const id = this.$route.params.id;
    if (this.id && !this.currentListing) {
      this.onProductsLoaded(this.products);
    }

    this._computedWatchers.orderedOptions.run();
    this.$forceUpdate();
  },
  beforeDestroy() {
    if (this.$refs.featuredProductsMultiSelect) {
      this.$refs.featuredProductsMultiSelect.deactivate();
    }
  },
  setup(props, context) {
    const { id } = context.root.$route.params;
    // const { isListingModalOpen, currentListing, toggleListingModal } = useUiState();
    const { user, load: loadUser, loading: userLoading } = useUser();
    const { globals, getGlobals } = useGlobals();
    const { categories, search: categorySearch } = useCategory();
    const { products, search: productSearch, createProduct, updateProduct, deleteProduct, loading: productLoading, error: productError } = useProduct('products');
    const { numerai, getModels: getNumeraiModels, error: numeraiError } = useNumerai('my-listings');
    const { send } = useUiNotification();

    const currentListing = ref(null);

    onSSR(async () => {
      await loadUser();
      await categorySearch();
      await productSearch({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
      await getGlobals();

      if (id) {
        currentListing.value = products?.value?.data?.find((p)=>p.id === parseInt(id));
      }
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
      category: product ? parseInt(productGetters.getCategoryIds(product)[0]) : null,
      description: product ? productGetters.getDescription(product) : null,
      avatar: product ? productGetters.getCoverImage(product) : null,
      isActive: product ? productGetters.getIsActive(product) : true,
      useEncryption: product ? productGetters.getUseEncryption(product) : true,
      webhook: product ? productGetters.getWebhook(product) : null,
      autoExpiration: productGetters.getExpirationRound(product) !== null,
      expirationRound: productGetters.getExpirationRound(product),
      options: product ? product.options : [],
      // hasFeaturedProducts: product?.featured_products?.length > 0,
      featuredProducts: product?.featured_products ? product?.featured_products.map(id => groupedProducts.value.map(gp=>gp.products).flat().find((p)=>parseInt(p.id) === parseInt(String(id)))) : []
    });

    const form = ref(resetForm(currentListing.value));

    const handleForm = (fn) => async () => {
      // resetErrorValues();
      await fn({ id: currentListing.value ? currentListing.value.id : null, product: form.value });
      const hasProductErrors = productError.value.listingModal;
      if (hasProductErrors) {
        send({
          message: productError.value.listingModal?.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
        return;
      }

      await productSearch({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});

      await context.root.$router.push('/listings');
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

    const saveListing = async () => {
      if (!currentListing.value) {
        return handleForm(createProduct)();
      } else {
        return handleForm(updateProduct)();
      }
    };

    return {
      id,
      currentListing,
      form,
      leafCategories: computed(() => categories ? categories.value.filter((category) => {
        return category.items.length === 0;
      }).sort((a, b) => -a.slug.localeCompare(b.slug)) : []),
      numerai: computed(() => numerai ? numerai.value : null),
      groupedProducts,
      products,
      productLoading,
      globals,
      user,
      productGetters,
      userGetters,
      getNumeraiModels,
      populateModelInfo,
      resetForm,
      saveListing
    };
  }
};
</script>

<style lang="scss" scoped>
.featured-products-multiselect::v-deep {
  .multiselect__select {
    &:before{
        top: 30%;
        border-style: none;
        position: relative;
        content: "\e9c5";
        font-family: "Nioicon";
        font-size: 22px;
        color: #8091a7;
    }
  }
  .multiselect__tag {
    color: var(--vs-selected-color);
    background: var(--vs-selected-bg);
    border: var(--vs-selected-border-width) var(--vs-selected-border-style) var(--vs-selected-border-color);
  }
  .multiselect__option {
    color: #8091a7;
    &--highlight {
      color: #1c2b46;
      background: var(--vs-selected-bg);
    }
    &--highlight:after {
      color: #1c2b46;
      background: var(--vs-selected-bg);
    }
  }
}
.editor::v-deep {
  .ql-editor{
      min-height:150px;
  }
}
.is-invalid::v-deep .vs__dropdown-toggle {
  border-color: #dc3545 !important;
  border-top-color: rgb(220, 53, 69) !important;
  border-right-color: rgb(220, 53, 69) !important;
  border-bottom-color: rgb(220, 53, 69) !important;
  border-left-color: rgb(220, 53, 69) !important;
}
</style>
