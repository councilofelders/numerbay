<template>
  <div class="page-wrap">
    <!-- create -->
    <section class="create-section section-space-b pt-4 pt-md-5 mt-md-4">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-8">
            <div class="section-head-sm">
              <router-link :to="`/listings`" class="btn-link fw-semibold"><em class="ni ni-arrow-left"></em> My listings
              </router-link>
              <h1 class="mt-2">{{ !id ? `Create new listing` : `Edit listing` }}</h1>
            </div>
          </div><!-- end col -->
          <div class="col-lg-8">
            <ValidationObserver v-slot="{ handleSubmit }">
              <form action="#" class="form-create mb-5 mb-lg-0">
                <ValidationProvider v-slot="{ errors }" rules="required" slim>
                  <div class="form-item mb-4">
                    <h5 :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-1">Choose category</h5>
                    <p :class="{ 'text-danger': Boolean(errors[0]) }" class="form-text mb-3">Select the category of
                      listing. This cannot be changed later.</p>
                    <v-select v-model="form.category" :class="!errors[0] ? '' : 'is-invalid'"
                              :clearable=false :disabled="Boolean(currentListing)" :options="leafCategories"
                              :reduce="option => option.id" class="generic-select"
                              label="slug" placeholder="Select Category" @input="onCategoryChange"></v-select>
                    <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider v-if="isPerModelCategory(form.category)" v-slot="{ errors }" rules="required"
                                    slim>
                  <div class="form-item mb-4">
                    <h5 :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-1">Select model</h5>
                    <p :class="{ 'text-danger': Boolean(errors[0]) }" class="form-text mb-3">Select the tournament model
                      for listing. This cannot be changed later.</p>
                    <v-select v-model="form.name" :class="!errors[0] ? '' : 'is-invalid'" :clearable=false
                              :disabled="Boolean(currentListing)" :options="getFilteredModels(form.category)" :reduce="option => option.name"
                              class="generic-select" label="name" placeholder="Select Model"
                              @input="populateModelInfo"></v-select>
                    <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider v-else v-slot="{ errors }" rules="required|min:2|alpha_dash" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Product name</label>
                      <p :class="{ 'text-danger': Boolean(errors[0]) }" class="form-text mb-3">Set the product name.
                        This cannot be changed later.</p>
                      <input v-model="form.name" :class="!errors[0] ? '' : 'is-invalid'" :disabled="Boolean(currentListing)"
                             class="form-control form-control-s1" placeholder="Product Name" type="text">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider v-slot="{ errors }" rules="secureUrl" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Avatar</label>
                      <input v-model="form.avatar" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                             placeholder="Https URL to an image (optional)" type="text" @change="encodeURL">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                    <object v-if="Boolean(form.avatar)" :data="form.avatar" class="col-xs-12 col-md-3 rounded-3"
                            style="max-width: 100%" type="image/png">
                      <img alt="" class="col-xs-12 col-md-3 rounded-3"
                           src="https://res.cloudinary.com/numerbay/image/upload/v1682662306/profile_picture_light_c4nzhq.jpg" style="max-width: 100%">
                    </object>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <div v-if="!Boolean(currentListing) && isTournamentCategory(form.category)">
                  <div v-if="!isSignalsDataCategory(form.category)" class="alert alert-success d-flex mb-4"
                       role="alert">
                    <svg class="flex-shrink-0 me-3" fill="currentColor" height="30" viewBox="0 0 24 24" width="30">
                      <path
                        d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"></path>
                    </svg>
                    <p class="fs-14">
                      Buyer-side encryption is enabled by default, uploading artifact files requires active sales.<br/>
                      <a class="link-secondary" href="https://docs.numerbay.ai/updates/encryption" target="_blank"><em
                        class="ni ni-help"></em> Learn more about encryption</a>
                    </p>
                  </div><!-- end alert -->
                  <div v-else class="alert alert-warning d-flex mb-4" role="alert">
                    <svg class="flex-shrink-0 me-3" fill="currentColor" height="30" viewBox="0 0 24 24" width="30">
                      <path
                        d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"></path>
                    </svg>
                    <p class="fs-14">
                      Buyer-side encryption is disabled by default due to large files, you can enable it in advanced
                      settings.<br/>
                      <a class="link-secondary" href="https://docs.numerbay.ai/updates/encryption" target="_blank"><em
                        class="ni ni-help"></em> Learn more about encryption</a>
                    </p>
                  </div><!-- end alert -->
                </div>
                <div class="form-item mb-4">
                  <div class="mb-4">
                    <div class="d-flex align-items-center justify-content-between">
                      <div class="me-2">
                        <h5 class="mb-1">Sell for weekday rounds</h5>
                        <p class="form-text">Sell this product for both weekday and weekend rounds</p>
                      </div>
                      <div class="form-check form-switch form-switch-s1">
                        <input v-model="form.isDaily" class="form-check-input" type="checkbox">
                      </div><!-- end form-check -->
                    </div><!-- end d-flex -->
                  </div>
                </div><!-- end form-item -->
                <div class="form-item mb-4">
                  <div class="mb-4">
                    <div class="d-flex align-items-center justify-content-between">
                      <div class="me-2">
                        <h5 class="mb-1">Show advanced settings</h5>
                      </div>
                      <div class="form-check form-switch form-switch-s1">
                        <input v-model="showAdvanced" class="form-check-input" type="checkbox">
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
                          <input v-model="form.isActive" class="form-check-input" type="checkbox">
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
                          <input v-model="form.autoExpiration" class="form-check-input" data-target="switch-content-expiration"
                                 type="checkbox" @change="onIsPerpetualChange(form.autoExpiration)">
                        </div><!-- end form-check -->
                      </div><!-- end d-flex -->
                      <ValidationProvider v-if="form.autoExpiration" v-slot="{ errors }"
                                          rules="required|integer|min_value:0" slim>
                        <div class="mt-4">
                          <input v-model="form.expirationRound" :class="!errors[0] ? '' : 'is-invalid'"
                                 class="form-control form-control-s1"
                                 min="0" placeholder="Round after which this product will be delisted"
                                 type="number">
                          <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
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
                          <a class="link-secondary" href="https://docs.numerbay.ai/updates/encryption" target="_blank">Learn
                            more about encryption <em class="ni ni-help"></em></a>
                        </div>
                        <div class="form-check form-switch form-switch-s1">
                          <input v-model="form.useEncryption" class="form-check-input" type="checkbox">
                        </div><!-- end form-check -->
                      </div><!-- end d-flex -->
                    </div>
                  </div><!-- end form-item -->
                  <ValidationProvider v-slot="{ errors }" rules="url" slim>
                    <div class="form-item mb-4">
                      <div class="mb-4">
                        <h5 :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-1">Webhook url</h5>
                        <p :class="{ 'text-danger': Boolean(errors[0]) }" class="form-text">Url to call on new sale
                          order. Useful for products using client-side encryption</p>
                        <a class="link-secondary"
                           href="https://docs.numerbay.ai/docs/tutorial-basics/sell-a-product#advanced-settings"
                           target="_blank">Learn more about webhook <em class="ni ni-help"></em></a>
                        <div class="row g-4">
                          <div class="col-lg-10 col-sm-8">
                            <input v-model="form.webhook" :class="[(Boolean(errors[0]) || (Boolean(webhookResponseCode) && webhookResponseCode!==200)) ? 'is-invalid' : '',  webhookResponseCode===200 ? 'is-valid' : '']"
                                   class="form-control form-control-s1"
                                   placeholder="Webhook URL (optional)" type="text" @change="encodeURL">
                          </div>
                          <div class="col-lg-2 col-sm-4">
                            <button :disabled="productWebhookLoading" class="btn btn-dark" type="button"
                                    @click="handleTestProductWebhook(form.webhook)">
                              <span v-if="productWebhookLoading"><span class="spinner-border spinner-border-sm"
                                                                       role="status"></span></span>
                              <span v-else>Test</span>
                            </button>
                          </div>
                        </div>
                        <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                      </div>
                    </div><!-- end form-item -->
                  </ValidationProvider>
                  <div class="form-item mb-4">
                    <h5 class="mb-1">Featured products</h5>
                    <p class="form-text mb-3">Other products to display in the product page (optional)</p>
                    <client-only>
                      <multiselect ref="featuredProductsMultiSelect" v-model="form.featuredProducts" :close-on-select="false"
                                   :group-select="true"
                                   :multiple="true" :options="groupedProducts" class="featured-products-multiselect"
                                   group-label="category" group-values="products" label="sku" placeholder=""
                                   track-by="id"
                      >
                        <template slot="option" slot-scope="props">
                          <span>{{ props.option.$isLabel ? props.option.$groupLabel : props.option.name }}</span>
                        </template>
                      </multiselect>
                    </client-only>
                  </div><!-- end form-item -->
                  <ValidationProvider v-slot="{ errors }" rules="integer|min_value:1" slim>
                    <div class="form-item mb-4">
                      <div class="mb-4">
                        <h5 :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-1">Locked up to round</h5>
                        <p :class="{ 'text-danger': Boolean(errors[0]) }" class="form-text">Round until which there will be no new sales</p>
                        <div class="row g-4">
                          <div class="col-lg-10 col-sm-8">
                            <input v-model="form.roundLock" :class="!errors[0] ? '' : 'is-invalid'"
                                   class="form-control form-control-s1"
                                   placeholder="Lock till round" min="1" step="1" type="number">
                          </div>
                          <div class="col-lg-2 col-sm-4">
                            <button class="btn btn-outline-dark" type="button"
                                    @click="handleClearLockRound()">
                              <span>Clear</span>
                            </button>
                          </div>
                        </div>
                        <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                      </div>
                    </div><!-- end form-item -->
                  </ValidationProvider>
                </div>
                <div class="form-item mb-4">
                  <h5 class="mb-3">Pricing options</h5>
                  <a :class="form.options.length > 0 ? 'btn-outline-dark' : 'btn-dark'" class="btn"
                     @click="changeOption(-1)"><em class="ni ni-plus"></em> New Option</a>
                  <div class="row g-gs mt-1" :key="updateList">
                    <div v-for="option in orderedOptions" :key="option.id" class="col-xl-6">
                      <div class="card card-full">
                        <div class="card-body card-body-s1">
                          <p class="mb-3 fs-13 mb-4">{{ option.is_on_platform ? `On-platform` : `Off-platform` }}</p>
                          <div class="card-media mb-3">
                            <div class="card-media-body">
                              <h4>{{ productGetters.getOptionFormattedPrice(option, withCurrency = true) }}</h4>
                              <p class="fw-medium fs-14">{{
                                  option.mode
                                }}{{
                                  option.mode === 'stake_with_limit' ? ` [${productGetters.getStakeLimit(option)}]` : ``
                                }} x {{ option.quantity }}</p>
                              <p class="fs-15">{{ option.description }}</p>
                            </div><!-- end card-media-body -->
                          </div><!-- end card-media -->
                          <div class="card-media mb-3">
                            <div class="card-media-body text-truncate">
                              <span class="fw-medium fs-13">{{
                                  option.is_on_platform ? (option.wallet || 'Numerai wallet') : option.third_party_url
                                }}</span>
                            </div>
                          </div><!-- end d-flex -->
                          <ul class="btns-group">
                            <li><a class="btn-link flex-grow-1 fw-medium fs-13 text-success" href="javascript:void(0);"
                                   @click="changeOption(option.key)">Change</a></li>
                            <li><a class="btn-link flex-grow-1 fw-medium fs-13 text-danger" href="javascript:void(0);"
                                   @click="deleteOption(option.key)">Delete</a></li>
                          </ul>
                        </div><!-- end card-body -->
                      </div><!-- end card -->
                    </div><!-- end col -->
                  </div><!-- end row -->
                </div><!-- end form-item -->
                <div class="form-item mb-4">
                  <label class="mb-2 form-label">Description</label>
                  <a class="float-end fs-15"
                     href="https://docs.numerbay.ai/docs/tutorial-basics/sell-a-product#product-description" target="_blank"><em class="ni ni-help"></em> Markdown shortcuts</a>
                  <client-only>
                    <div class="mb-4 editor">
                      <quill-editor
                        ref="descriptionEditor"
                        v-model="form.description"
                        :options="editorOption"
                        name="description"
                      />
                      <input ref="imageInput" accept="image/*" class="d-none" style="display: none" type="file"
                             @change="_doImageUpload">
                    </div>
                  </client-only>
                </div><!-- end form-item -->
                <button :disabled="productLoading" class="btn btn-dark" type="button"
                        @click="handleSubmit(saveListing)">
                  <span v-if="productLoading"><span class="spinner-border spinner-border-sm me-2" role="status"></span>Saving...</span>
                  <span v-else>Save</span>
                </button>
              </form>
            </ValidationObserver>
          </div><!-- endn col -->
        </div><!-- row-->
        <PricingOptionModal
          ref="pricingOptionModal"
          :groupedProducts="groupedProducts"
          :is-modal-open="isModalOpen"
          :isPerRoundCategory="isPerRoundCategory(form.category)"
          :isSubmissionCategory="isSubmissionCategory(form.category)"
          :isTournamentCategory="isTournamentCategory(form.category)"
          :options="form.options"
          :user="user"
          modalId="pricingOptionModal"
          @update:pricing="refresh"
        ></PricingOptionModal>
      </div><!-- container -->
    </section><!-- create-section -->
  </div><!-- end page-wrap -->
</template>

<script>
import PricingOptionModal from "../components/section/PricingOptionModal";

// Composables
import {computed, ref} from '@vue/composition-api';
import {onSSR} from '@vue-storefront/core';
import {
  productGetters,
  useCategory,
  useGlobals,
  useNumerai,
  useProduct,
  useUser,
  userGetters
} from '@vue-storefront/numerbay';
import {useUiNotification} from '~/composables';
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
  components: {
    PricingOptionModal
  },
  middleware: [
    'is-authenticated'
  ],
  data() {
    return {
      updateList: 0,  // todo better reactivity for pricing options data
      optionForm: {},
      isModalOpen: false,
      modal: null,
      showAdvanced: false,
      webhookResponseCode: null,
      imageUpload: {
        url: 'https://api.cloudinary.com/v1_1/numerbay/image/upload'
      },
      editorOption: {
        theme: 'snow',
        modules: {
          markdownShortcuts: {}, // https://patricklee.nyc/quill-markdown-shortcuts/
          toolbar: {
            container: [
              ['bold', 'italic', 'underline', 'strike'],
              ['blockquote', 'code-block'],
              [{list: 'ordered'}, {list: 'bullet'}],
              [{indent: '-1'}, {indent: '+1'}],
              [{header: [1, 2, 3, 4, 5, 6, false]}],
              [{color: []}, {background: []}],
              [{font: []}],
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
    quillInstance() {
      return this.$refs.descriptionEditor.quill;
    }
  },
  methods: {
    insertImage() {
      // manipulate the DOM to do a click on hidden input
      this.$refs.imageInput.click();
    },
    async _doImageUpload(event) {
      this.send({
        message: 'Uploading image, please wait...',
        type: 'bg-info',
        icon: 'ni-info'
      });
      // only upload the first image
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
      if (categoryId) {
        const category = this.leafCategories.filter(c => c.id === Number(categoryId))[0];
        console.log('category', category)
        switch (category?.slug) {
          case 'signals-data':
            this.form.useEncryption = false;
            if (!this.form.description) {
              this.form.description = `<h1>Data Overview</h1><p>This product offers [DATA TYPE] for [COVERAGE], sourced from [DATA SOURCE].</p><p><br></p><p>This data is used by the following models:</p><ul><li>[LINKS TO SIGNALS MODEL]</li></ul><p><br></p><p>Data file is in [FORMAT] and is typically uploaded at [DAY OF WEEK] [TIME OF DAY].</p><p><br></p><h1>Coverage</h1><p>This data file contains [NUMBER] [COUNTRY] tickers, ... from [YYYYMMDD] to [YYYYMMDD]</p><p><br></p><h1>Column Definitions</h1><p>The data file has [NUMBER OF COLUMNS]:</p><ol><li><strong>Column1 </strong>[TYPE] - [DESCRIPTION]</li><li><strong>Column2 </strong>[TYPE] - [DESCRIPTION]</li></ol><p><br></p><h1>Sample Data</h1><p>[Table or screenshot or link to sample data file]</p>`;
            }
            break;
          default:
            this.form.useEncryption = true;
            return;
        }
      }
    },
    refresh() {
      this._computedWatchers.orderedOptions.run();
      // this.$forceUpdate();
      this.updateList += 1;
    },
    isSubmissionCategory(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c => c.id === Number(categoryId))[0];
        return category?.is_submission;
      }
      return false;
    },
    isPerRoundCategory(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c => c.id === Number(categoryId))[0];
        return category?.is_per_round;
      }
      return false;
    },
    isPerModelCategory(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c => c.id === Number(categoryId))[0];
        return category?.is_per_model;
      }
      return false;
    },
    isSignalsDataCategory(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c => c.id === Number(categoryId))[0];
        return category?.slug === 'signals-data';
      }
      return false;
    },
    isTournamentCategory(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c => c.id === Number(categoryId))[0];
        if (Boolean(category) && Boolean(category.tournament)) {
          return true;
        }
      }
      return false;
    },
    getFilteredModels(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c => c.id === Number(categoryId))[0];
        let tournament = 8;
        if (category.slug.startsWith('signals-')) {
          tournament = 11;
        } else if (category.slug.startsWith('crypto-')) {
          tournament = 12;
        }
        return userGetters.getModels(this.numerai, tournament, false);
      }
      return [];
    },
    onIsPerpetualChange(autoExpiration) {
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
    onProductsLoaded(products) {
      this.currentListing = products?.data?.find((p) => p.id === parseInt(this.id));
      this.form = this.resetForm(this.currentListing);
      this.showAdvanced = (!this.form.isActive) || (this.form.autoExpiration) || (!this.form.useEncryption) || (Boolean(this.form.featuredProducts) && this.form.featuredProducts.length > 0) || (this.form.webhook) || Boolean(this.form.roundLock);
    },
    async handleTestProductWebhook(url) {
      await this.testProductWebhook({url})
      const hasProductErrors = this.productError.listingModal;
      if (hasProductErrors) {
        this.webhookResponseCode = 500;
        this.send({
          message: this.productError.listingModal?.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
        return;
      }
      this.webhookResponseCode = 200;
    },
    async handleClearLockRound() {
      this.form.roundLock = null;
    }
  },
  watch: {
    products(newProducts) {
      this.onProductsLoaded(newProducts);
    }
  },
  mounted() {
    if (this.userGetters.getNumeraiApiKeyPublicId(this.user)) {
      this.getNumeraiModels().catch((e) => {
        this.send({
          message: e?.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle',
          persist: true,
          action: {
            text: 'Change Numerai API Key',
            onClick: async () => {
              await this.$router.push('/numerai-settings');
            }
          }
        });
      })
    }

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
    const {id} = context.root.$route.params;
    const {user, load: loadUser, loading: userLoading} = useUser();
    const {globals} = useGlobals();
    const {categories, search: categorySearch} = useCategory();
    const {
      products,
      search: productSearch,
      createProduct,
      updateProduct,
      deleteProduct,
      testProductWebhook,
      loading: productLoading,
      loadingWebhook: productWebhookLoading,
      error: productError
    } = useProduct('products');
    const {numerai, getModels: getNumeraiModels, error: numeraiError} = useNumerai('my-listings');
    const {send} = useUiNotification();

    const currentListing = ref(null);

    onSSR(async () => {
      await loadUser();
      await categorySearch();
      await productSearch({filters: {user: {in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});

      if (id) {
        currentListing.value = products?.value?.data?.find((p) => p.id === parseInt(id));
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
      isDaily: product ? productGetters.getIsDaily(product) : true,
      useEncryption: product ? productGetters.getUseEncryption(product) : true,
      webhook: product ? productGetters.getWebhook(product) : null,
      autoExpiration: productGetters.getExpirationRound(product) !== null,
      expirationRound: productGetters.getExpirationRound(product),
      options: product ? product.options : [],
      featuredProducts: product?.featured_products ? product?.featured_products.map(id => groupedProducts.value.map(gp => gp.products).flat().find((p) => parseInt(p.id) === parseInt(String(id)))) : [],
      roundLock: product ? productGetters.getRoundLock(product) : null
    });

    const form = ref(resetForm(currentListing.value));

    const handleForm = (fn) => async () => {
      // resetErrorValues();
      await fn({id: currentListing.value ? currentListing.value.id : null, product: form.value});
      const hasProductErrors = productError.value.listingModal;
      if (hasProductErrors) {
        send({
          message: productError.value.listingModal?.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
        return;
      }

      await productSearch({filters: {user: {in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});

      await context.root.$router.push('/listings');
    };

    const populateModelInfo = async (name) => {
      if (name) {
        const models = numerai.value.models.filter((m) => m.name === name);
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
      testProductWebhook,
      productLoading,
      productWebhookLoading,
      productError,
      globals,
      user,
      productGetters,
      userGetters,
      getNumeraiModels,
      populateModelInfo,
      resetForm,
      saveListing,
      send
    };
  }
};
</script>

<style lang="scss" scoped>
.featured-products-multiselect::v-deep {
  .multiselect__select {
    &:before {
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
  .ql-editor {
    min-height: 150px;
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
