/* eslint-disable no-undef */
<template>
    <div class="page-wrap">
        <section class="item-detail-section section-space">
            <div class="container">
                <div class="row">
                    <div class="col-lg-3">
                        <div class="item-detail-content mb-5 mb-lg-0">
                            <div class="ms-auto">
                                <div class="item-detail-content">
                                    <div class="item-detail-img-container item-detail-img-full mb-4">
                                        <img :src="imgLg" alt="" class="w-100 rounded-3">
                                    </div><!-- end item-detail-img-container -->
                                </div><!-- end item-detail-content -->
                            </div><!-- end col -->
                          <h1 class="item-detail-title mb-2 text-break"><a :href="modelUrl" class="" target="_blank">{{ title }}</a></h1>
                            <div class="item-detail-meta d-flex flex-wrap align-items-center mb-3">
                                <span class="item-detail-text-meta">Round <span class="text-primary fw-semibold">{{ globals.selling_round }}</span></span>
                                <span class="dot-separeted"></span>
                                <span class="item-detail-text-meta">{{ category }}</span>
                                <span class="dot-separeted"></span>
                                <span class="item-detail-text-meta">Past sales <span class="text-primary fw-semibold">{{ productGetters.getTotalSales(product) }}</span></span>
                            </div>
                            <div class="item-credits">
                                <div class="row g-4">
                                    <div class="col-xl-12">
                                        <div class="card-media card-media-s1">
                                            <div class="card-media-body">
                                                <p class="fw-semibold text-black text-break">@{{ owner }}</p>
                                                <span class="fw-medium small">Owner</span>
                                            </div>
                                        </div><!-- end card -->
                                    </div><!-- end col-->
                                </div><!-- end row -->
                            </div><!-- end row -->
<!--                            <p class="item-detail-text mb-4">{{ content }}</p>-->
<!--                            <div class="item-credits">
                                <div class="row g-4">
                                    <div class="col-xl-6" v-for="item in SectionData.itemDetailData.itemDetailList" :key="item.id">
                                        <div class="card-media card-media-s1">
                                            <router-link :to="item.path" class="card-media-img flex-shrink-0 d-block">
                                                <img :src="item.avatar" alt="avatar">
                                            </router-link>
                                            <div class="card-media-body">
                                                <router-link :to="item.path" class="fw-semibold">{{ item.title }}</router-link>
                                                <p class="fw-medium small">{{ item.subTitle }}</p>
                                            </div>
                                        </div>&lt;!&ndash; end card &ndash;&gt;
                                    </div>&lt;!&ndash; end col&ndash;&gt;
                                    <div class="col-xl-12" v-for="item in SectionData.itemDetailData.itemDetailListTwo" :key="item.id">
                                        <div class="card-media card-media-s1">
                                            <router-link :to="item.path" class="card-media-img flex-shrink-0 d-block">
                                                <img :src="item.avatar" alt="avatar">
                                            </router-link>
                                            <div class="card-media-body">
                                                <p class="fw-semibold text-black">{{ item.title }}</p>
                                                <span class="fw-medium small">{{ item.subTitle }}</span>
                                            </div>
                                        </div>&lt;!&ndash; end card &ndash;&gt;
                                    </div>&lt;!&ndash; end col&ndash;&gt;
                                </div>&lt;!&ndash; end row &ndash;&gt;
                            </div>&lt;!&ndash; end row &ndash;&gt;-->
                            <div class="item-detail-btns mt-4">
                                <ul class="btns-group d-flex">
                                    <li class="flex-grow-1">
                                        <a href="javascript:void(0);" @click="togglePlaceBidModal" :class="`btn btn-dark d-block ${productGetters.getIsActive(product)?'':'disabled'}`">{{ productGetters.getIsActive(product) ? 'Buy' : 'Not for sale' }}</a>
<!--                                        <router-link v-show="!isAuthenticated" to="/login-v2" :class="`btn btn-dark d-block ${productGetters.getIsActive(product)?'':'disabled'}`">{{ productGetters.getIsActive(product) ? 'Buy' : 'Not for sale' }}</router-link>-->
                                    </li>
<!--                                    <li class="flex-grow-1">
                                        <div class="dropdown">
                                            <a href="#" class="btn bg-dark-dim d-block" data-bs-toggle="dropdown">{{ SectionData.itemDetailData.btnTextTwo }}</a>
                                            <div class="dropdown-menu card-generic p-2 keep-open w-100 mt-1">
                                                <router-link :to="icon.path" class="dropdown-item card-generic-item" v-for="(icon, i) in SectionData.socialShareList" :key="i"><em class="ni me-2" :class="icon.btnClass"></em>{{ icon.title }}</router-link>
                                            </div>
                                        </div>
                                    </li>-->
                                </ul>
                            </div><!-- end item-detail-btns -->
                            <ModelMetricsCard
                              :nmr-staked="nmrStaked"
                              :latest-returns="latestReturns"
                              :latest-reps="latestReps"
                              :latest-ranks="latestRanks"
                              :show="{fnc: productGetters.getCategory(product).tournament==8, tc: productGetters.getCategory(product).tournament==8, ic: productGetters.getCategory(product).tournament==11}"
                            ></ModelMetricsCard>
                        </div><!-- end item-detail-content -->
                    </div><!-- end col -->
                    <div class="col-lg-9 ms-auto">
                        <div class="item-detail-content">
                            <div class="item-detail-chart-container mb-4">
                              <div class="card-border card-full">
                                <div class="card-body card-body-s1">
                                  <h5 class="mb-3">Recent Performance</h5>
                                  <div class="item-detail-list" v-if="isNumeraiChartReady">
                                    <NumeraiChart class="numerai-chart" :chartdata="numeraiCorrMmcChartData"></NumeraiChart>
                                    <NumeraiChart v-if="productGetters.getCategory(product).tournament==8" class="numerai-chart" :chartdata="numeraiTcChartData"></NumeraiChart>
                                    <NumeraiChart v-if="productGetters.getCategory(product).tournament==11" class="numerai-chart" :chartdata="numeraiIcChartData"></NumeraiChart>
                                  </div>
                                  <div class="item-detail-list placeholder-glow" v-else>
                                    <svg class="bd-placeholder-img placeholder" width="100%" height="480" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder" preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title><rect width="100%" height="100%" fill="#868e96"></rect></svg>
                                  </div>
                                </div><!-- end card-body -->
                              </div><!-- end card-border -->
                            </div><!-- end item-detail-chart-container -->
                            <div class="item-detail-description-container mb-4">
                              <div class="card-border card-full">
                                <div class="card-body card-body-s1">
                                  <h5 class="mb-3">Description</h5>
                                  <div class="item-detail-text mb-4" v-html="description"></div>
                                </div><!-- end card-body -->
                              </div><!-- end card-border -->
                            </div><!-- end item-detail-description-container -->
                        </div><!-- end item-detail-content -->
                    </div><!-- end col -->
<!--                    <div class="col-lg-12">
                        <div class="item-detail-tab mt-5">
                            <div class="row g-gs">
                                <div class="col-xl-4 col-lg-6">
                                    <div class="card-border card-full">
                                        <div class="card-body card-body-s1">
                                                <h5 class="mb-3">{{ SectionData.itemDetailData.itemDetailOwnerListTwo.title }}</h5>
                                                <div class="item-detail-list">
                                                    <div class="card-media card-media-s2" v-for="item in SectionData.itemDetailData.itemDetailOwnerListTwo.ownerList" :key="item.id">
                                                        <router-link :to="item.path" class="card-media-img flex-shrink-0 d-block"><img :src="item.avatar" alt="avatar"></router-link>
                                                        <div class="card-media-body">
                                                            <p class="fw-semibold"><router-link :to="item.path" class="text-black">{{ item.title }}</router-link></p>
                                                            <p class="small">{{ item.subTitle }}</p>
                                                        </div>
                                                    </div>&lt;!&ndash; end card-media &ndash;&gt;
                                                </div>&lt;!&ndash; end item-detail-list &ndash;&gt;
                                        </div>&lt;!&ndash; end card-body &ndash;&gt;
                                    </div>&lt;!&ndash; end card-border &ndash;&gt;
                                </div>&lt;!&ndash; end col &ndash;&gt;
                                <div class="col-xl-4 col-lg-6">
                                    <div class="card-border card-full">
                                        <div class="card-body card-body-s1">
                                            <h5 class="mb-3">{{ SectionData.itemDetailData.itemDetailBidsListTwo.title }}</h5>
                                            <div class="item-detail-list">
                                                <div class="card-media card-media-s2" v-for="item in SectionData.itemDetailData.itemDetailBidsListTwo.bidsList" :key="item.id">
                                                    <router-link :to="item.path" class="card-media-img flex-shrink-0 d-block"><img :src="item.avatar" alt="avatar"></router-link>
                                                    <div class="card-media-body text-truncate">
                                                        <p class="fw-semibold text-black text-truncate">{{ item.title }}</p>
                                                        <p class="small">{{ item.date }}</p>
                                                    </div>
                                                </div>&lt;!&ndash; end card-media &ndash;&gt;
                                            </div>&lt;!&ndash; end item-detail-list &ndash;&gt;
                                        </div>
                                    </div>&lt;!&ndash; end col &ndash;&gt;
                                </div>&lt;!&ndash; end col &ndash;&gt;
                                <div class="col-xl-4">
                                    <div class="card-border card-full">
                                        <div class="card-body card-body-s1">
                                                <h5 class="mb-3">{{ SectionData.itemDetailData.itemDetailHistoryListTwo.title }}</h5>
                                                <div class="item-detail-list">
                                                    <div class="card-media card-media-s2" v-for="item in SectionData.itemDetailData.itemDetailHistoryListTwo.historyList" :key="item.id">
                                                        <router-link :to="item.path" class="card-media-img flex-shrink-0 d-block"><img :src="item.avatar" alt="avatar"></router-link>
                                                        <div class="card-media-body text-truncate">
                                                            <p class="fw-semibold text-black text-truncate">{{ item.title }}</p>
                                                            <p class="small text-truncate">{{ item.subTitle }}</p>
                                                        </div>
                                                    </div>&lt;!&ndash; end card-media &ndash;&gt;
                                                </div>&lt;!&ndash; end item-detail-list &ndash;&gt;
                                        </div>
                                    </div>&lt;!&ndash; end col &ndash;&gt;
                                </div>&lt;!&ndash; end col &ndash;&gt;
                            </div>&lt;!&ndash; end row &ndash;&gt;
                        </div>&lt;!&ndash; end item-detail-tab &ndash;&gt;
                    </div>&lt;!&ndash; end col &ndash;&gt;-->
                </div><!-- end row -->
            </div><!-- .container -->
            <!-- Modal -->
            <Modal modal-id="placeBidModal" @registeredModal="placeBidModal = $event" ref="placeBidModal">
                <template slot="title">{{ paymentStep === 1 ? `Place an Order` : `Payment` }}</template>
                <div v-if="paymentStep === 1">
                  <p class="mb-3">You are about to buy <strong>{{ title }}</strong> from <strong>{{ owner }}</strong></p>
                  <ValidationObserver v-slot="{ handleSubmit }">
                  <div class="mb-3">
                      <label class="form-label">Select an option</label>
                      <v-select class="generic-select generic-select-s1" ref="optionDropdown" v-model="optionIdx" v-if="!!product" label="id"
            :options="productGetters.getOrderedOptions(product)" :reduce="option => option.index" :clearable=false @input="handleSubmit(onOptionChange)">
                        <template #selected-option="option">
                          {{ productGetters.getFormattedOption(option) }}
                        </template>
                        <template v-slot:option="option">
                          {{ productGetters.getFormattedOption(option) }}
                        </template>
                      </v-select>
                  </div>
                  <ValidationProvider rules="required|integer|min_value:1|max_value:10" v-slot="{ errors }" v-if="isOnPlatform" slim>
                  <div class="mb-3">
                      <label class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Enter quantity
  <!--                                <span class="text-primary">5 available</span>-->
                      </label>
                      <input type="number" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" v-model="quantity" min="1" max="10" step="1" @change="handleSubmit(onQuantityChange)">
                      <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                  </div>
                  </ValidationProvider>
                  <div class="d-flex flex-wrap align-items-center justify-content-between mb-4" v-if="!!product && isOnPlatform && productGetters.getCategory(product).is_submission">
                      <div class="form-check">
                          <input class="form-check-input" type="checkbox" v-model="autoSubmit" id="autoSubmit" :disabled="!isAutoSubmitOptional">
                        <label class="form-check-label form-check-label-s1" for="autoSubmit"> {{ autoSubmitText }} </label>
                      </div>
                  </div>
                  <ValidationProvider rules="required" v-slot="{ errors }" v-if="autoSubmit" slim>
                  <div class="mb-3">
                      <label class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Select a submission slot</label>
                      <v-select class="generic-select generic-select-s1" :class="!errors[0] ? '' : 'is-invalid'" ref="slotDropdown" v-model="submitSlot" v-if="!!product && !numeraiLoading" label="name"
            :options="userGetters.getModels(numerai, productGetters.getTournamentId(product), false)" :reduce="model => model.id" :clearable=true></v-select>
                      <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                  </div>
                  </ValidationProvider>
                  <ul class="total-bid-list mb-4" v-if="isOnPlatform">
                      <li><span>{{ (!!product && productGetters.getCategory(product).is_per_round) ? 'Total number of rounds' : 'Total order quantity' }}</span> <span>{{ productGetters.getCategory(product).is_per_round ? productGetters.getOrderedOption(product, optionIdx).quantity : quantity }}</span></li>
                      <li><span>You will pay</span> <span>{{ formattedTotalPrice }}</span></li>
                  </ul>
                  <div class="d-flex flex-wrap align-items-center justify-content-between mb-4" v-if="!!product && isOnPlatform">
                      <div class="form-check">
                          <input class="form-check-input" type="checkbox" v-model="terms" id="terms">
                        <label class="form-check-label form-check-label-s1" for="terms"> I understand that I need to make payment in <strong>1 single transaction</strong>, and neither Numerai nor NumerBay is liable for any loss resulted from this transaction. </label>
                      </div>
                  </div>
                  <button @click="handleSubmit(onPlaceOrder)" class="btn btn-dark btn-full d-flex justify-content-center" :disabled="isOnPlatform && (makeOrderLoading || !terms)">
                    <span v-if="makeOrderLoading"><span class="spinner-border spinner-border-sm me-2" role="status" ></span>Placing Order...</span>
                    <span v-else>{{ buyBtnText }}</span>
                  </button>
                  </ValidationObserver>
                </div>
                <div v-if="paymentStep === 2">
                  <p class="mb-3">Please make payment through your <strong>Numerai wallet</strong> within <strong>45 minutes</strong>. You can leave this page.</p>
                  <div class="mb-3">
                      <label class="form-label">Seller wallet address</label>
                      <div class="d-flex align-items-center border p-3 rounded-3">
                          <input type="text" class="copy-input copy-input-s1" v-model="toAddress" id="copy-input-address" readonly>
                          <div class="tooltip-s1">
                              <button v-clipboard:copy="toAddress" v-clipboard:success="onCopy" class="copy-text" type="button">
                                  <span class="tooltip-s1-text tooltip-text">Copy</span>
                                  <em class="ni ni-copy"></em>
                              </button>
                          </div>
                      </div>
                  </div>
                  <div class="mb-3">
                      <label class="form-label">Amount to send</label>
                      <div class="d-flex align-items-center border p-3 rounded-3">
                          <input type="text" class="copy-input copy-input-s1" v-model="amount" id="copy-input-amount" readonly>
                          <div class="tooltip-s1">
                              <button v-clipboard:copy="JSON.stringify(amount)" v-clipboard:success="onCopy" class="copy-text" type="button">
                                  <span class="tooltip-s1-text tooltip-text">Copy</span>
                                  <em class="ni ni-copy"></em>
                              </button>
                          </div>
                      </div>
                  </div>
                  <a :href="SectionData.placeBidModal.btnLink" class="btn btn-dark d-block">View my orders</a>
                </div>
            </Modal><!-- end modal-->
        </section><!-- end item-detail-section -->
        <!-- Related product -->
        <RelatedProducts title="Featured by seller" :products="relatedProducts" v-if="Boolean(relatedProducts) && relatedProducts.length > 0"></RelatedProducts>
    </div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

import NumeraiChart from '@/components/section/NumeraiChart.vue';

// Composables
import { onSSR } from '@vue-storefront/core';
import { computed, reactive } from '@vue/composition-api';
import { numeraiGetters, orderGetters, productGetters, reviewGetters, useGlobals, useMakeOrder, useNumerai, useProduct, useReview, useUser, useUserOrder, userGetters } from '@vue-storefront/numerbay';
import { useUiNotification } from '~/composables';

export default {
  name: 'ProductDetails',
  components: {
    NumeraiChart
  },
  data() {
    return {
      placeBidModal: null,
      paymentStep: 1,
      optionIdx: 0,
      quantity: 1,
      amount: 0,
      toAddress: '',
      terms: false,
      autoSubmit: false,
      submitSlot: null,
      SectionData,
      // id: this.$route.params.id,
      // title: this.$route.params.title,
      // imgLg: this.$route.params.imgLg,
      metaText: this.$route.params.metaText,
      metaTextTwo: this.$route.params.metaTextTwo,
      metaTextThree: this.$route.params.metaTextThree,
      content: this.$route.params.content
    };
  },
  // props: {
  //   title: {
  //     type: String,
  //     required: true
  //   }
  // },
  // mounted() {
  //   this.products.forEach(element => {
  //     if (this.id === element.id) {
  //       this.imgLg = element.imgLg;
  //       this.title = element.title;
  //       this.metaText = element.metaText;
  //       this.metaTextTwo = element.metaTextTwo;
  //       this.metaTextThree = element.metaTextThree;
  //       this.content = element.content;
  //     }
  //   });
  // },
  computed: {
    category() {
      return this.$route.params.category || this.productGetters.getCategory(this.product).slug;
    },
    isOnPlatform() {
      return this.productGetters.getOptionIsOnPlatform(this.productGetters.getOrderedOption(this.product, this.optionIdx));
    },
    isAutoSubmitOptional() {
      return !this.productGetters.getOptionIsOnPlatform(this.productGetters.getOrderedOption(this.product, this.optionIdx)) || this.productGetters.getMode(this.productGetters.getOrderedOption(this.product, this.optionIdx)) === 'file';
    },
    autoSubmitText() {
      return this.isAutoSubmitOptional ? '(Optional) Auto-submit this model to Numerai for me once seller submits to NumerBay.' : 'Auto-submit this model to Numerai for me.';
    },
    buyBtnText() {
      return this.isOnPlatform ? 'Place an Order' : 'Visit external listing';
    },
    // mode() {
    //   return this.$route.params.mode || this.productGetters.getMode(this.productGetters.getOrderedOption(this.product, 0)).toUpperCase();
    // },
    owner() {
      return this.$route.params.owner || this.productGetters.getOwner(this.product);
    },
    isNumeraiChartReady() {
      return !this.productLoading && !this.numeraiLoading && Boolean(this.productGetters.getCategory(this.product).tournament) && Boolean(this.numerai.modelInfo);
    },
    title() {
      return this.$route.params.title || this.productGetters.getName(this.product).toUpperCase();
    },
    imgLg() {
      return this.$route.params.imgLg || this.productGetters.getCoverImage(this.product);
    },
    description() {
      return this.$route.params.description || this.productGetters.getDescription(this.product) || 'No description available.';
    },
    modelUrl() {
      return this.$route.params.modelUrl || this.productGetters.getModelUrl(this.product);
    },
    nmrStaked() {
      return this.$route.params.nmrStaked || this.productGetters.getModelNmrStaked(this.product, 2);
    },
    latestRanks() {
      return {
        corr: this.$route.params.latestRankCorr || this.productGetters.getModelRank(this.product, 'corr'),
        mmc: this.$route.params.latestRankMmc || this.productGetters.getModelRank(this.product, 'mmc'),
        fnc: this.$route.params.latestRankFnc || this.productGetters.getModelRank(this.product, 'fnc'),
        tc: this.$route.params.latestRankTc || this.productGetters.getModelRank(this.product, 'tc'),
        ic: this.$route.params.latestRankIc || this.productGetters.getModelRank(this.product, 'ic')
      };
    },
    latestReps() {
      return {
        corr: this.$route.params.latestRepCorr || this.productGetters.getModelRep(this.product, 'corr'),
        mmc: this.$route.params.latestRepMmc || this.productGetters.getModelRep(this.product, 'mmc'),
        fnc: this.$route.params.latestRepFnc || this.productGetters.getModelRep(this.product, 'fnc'),
        tc: this.$route.params.latestRepTc || this.productGetters.getModelRep(this.product, 'tc'),
        ic: this.$route.params.latestRepIc || this.productGetters.getModelRep(this.product, 'ic')
      };
    },
    latestReturns() {
      return {
        oneDay: this.$route.params.latestReturnOneDay || this.productGetters.getModelReturn(this.product, 'oneDay'),
        threeMonths: this.$route.params.latestReturnThreeMonths || this.productGetters.getModelReturn(this.product, 'threeMonths'),
        oneYear: this.$route.params.latestReturnOneYear || this.productGetters.getModelReturn(this.product, 'oneYear')
      };
    },
    formattedTotalPrice() {
      const option = this.productGetters.getOrderedOption(this.product, this.optionIdx);
      return `${((option.special_price ? option.special_price : option.price))?.toFixed(4)} ${option.currency}`;
    }

  },
  methods: {
    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    async onOptionChange(option) {
      await this.search({ id: this.id, categorySlug: this.category, name: this.name, qty: this.quantity });
    },
    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    async onQuantityChange(quantity) {
      await this.search({ id: this.id, categorySlug: this.category, name: this.name, qty: this.quantity });
    },
    async onPlaceOrder() {
      const option = this.productGetters.getOrderedOption(this.product, this.optionIdx);
      if (!this.productGetters.getOptionIsOnPlatform(option)) {
        // visit external listing
        window.open(option.third_party_url, '_blank');
        return;
      }

      const optionId = option.id;
      // todo coupon: coupon
      await this.make({id: this.productGetters.getId(this.product), optionId, submitModelId: this.submitSlot, quantity: this.quantity})
      if (this.makeOrderError?.make) {
        this.send({
          message: this.makeOrderError.make.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
      } else {
        this.toAddress = this.orderGetters.getToAddress(this.order);
        this.amount = this.orderGetters.getPrice(this.order);
        this.paymentStep = 2;
      }

      //   .then(() => {
      //   this.toAddress = this.orderGetters.getToAddress(this.order);
      //   this.amount = this.orderGetters.getPrice(this.order);
      //   this.paymentStep = 2;
      // });
    },
    getMetricColor(value) {
      if (value > 0) {
        return 'success';
      } else if (value < 0) {
        return 'danger';
      } else {
        return '';
      }
    },
    togglePlaceBidModal() {
      if (!this.isAuthenticated) {
        this.$router.push('/login-v2');
      } else {
        this.placeBidModal?.toggle();
      }
    }
  },
  watch: {
    async product() {
      if (!this.isAutoSubmitOptional) {
        this.autoSubmit = true;
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      const modal = this.$refs.placeBidModal.$refs.placeBidModal;

      modal?.addEventListener('show.bs.modal', async () => {
        if (!this.isAuthenticated) {
          try {
            this.placeBidModal?.dispose();
          } finally {
            await this.$router.push('/login-v2');
          }
        } else {
          await this.getGlobals();
          // eslint-disable-next-line camelcase
          await this.orderSearch({ role: 'buyer', filters: {product: {in: [this.productGetters.getId(this.product)]}, round_order: {in: [this.globals.selling_round]}, state: {in: ['pending', 'confirmed']}} });
          if (this.orders?.data?.length > 0) {
            // this.send({
            //   message: 'You already bought this product for this round',
            //   type: 'info'
            // });
            // this.$router.push(`/checkout/confirmation?order=${this.orders.data[0].id}`);
            this.toAddress = this.orderGetters.getToAddress(this.orders?.data[0]);
            this.amount = this.orderGetters.getPrice(this.orders?.data[0]);
            this.paymentStep = 2;
          }
        }
      }, false);

      modal?.addEventListener('shown.bs.modal', () => {
        this.$refs.optionDropdown?.$refs?.search?.focus();
        if (this.isAuthenticated) {
          this.getModels();
        }
      }, false);

      if (Boolean(this.product) && !this.isAutoSubmitOptional) {
        this.autoSubmit = true;
      }
    });
  },
  beforeDestroy() {
    this.placeBidModal?.hide();
  },
  setup(props, context) {
    const { id, category, name } = context.root.$route.params;
    const cacheKey = String(id || (category + name));
    const { products, search, loading: productLoading } = useProduct(cacheKey);
    const { products: relatedProducts, search: searchRelatedProducts, loading: relatedLoading } = useProduct(`relatedProducts-${cacheKey}`);
    const { numerai, getModels, getModelInfo, loading: numeraiLoading } = useNumerai(cacheKey);
    const { globals, getGlobals, loading: globalsLoading } = useGlobals();
    const { user, isAuthenticated, loading: userLoading } = useUser();
    const { order, make, loading: makeOrderLoading, error: makeOrderError } = useMakeOrder();
    const { orders, search: orderSearch } = useUserOrder('product');
    const { send } = useUiNotification();

    // const pageData = reactive({
    //   SectionData,
    //   id: context.root.$route.params.id,
    //   title: context.root.$route.params.title,
    //   imgLg: context.root.$route.params.imgLg,
    //   metaText: context.root.$route.params.metaText,
    //   metaTextTwo: context.root.$route.params.metaTextTwo,
    //   metaTextThree: context.root.$route.params.metaTextThree,
    //   content: context.root.$route.params.content
    // });

    const product = computed(() => (products.value.data || [])[0]);

    onSSR(async () => {
      await search({ id, categorySlug: category, name }).then(async ()=>{
        // await searchRelatedProducts({ filters: {user: {in: [product.value.owner.id]}}}); // catId: product.value.category.id,
        await searchRelatedProducts({ filters: {id: {in: product?.value?.featured_products || []}}});
        // await searchReviews({ productId: id });
        // const product = (products.value.data || [])[0];
        if (product.value?.category?.tournament) {
          await getModelInfo({tournament: product.value?.category?.slug.startsWith('signals') ? 11 : 8, modelName: product.value?.name});
        }
        await getGlobals();
      });
    });

    // const product = computed(() => productGetters.getFiltered(products.value.data, { master: true, attributes: context.root.$route.query })[0]);

    const onCopy = (e) => {
      const target = e.trigger.querySelector('.tooltip-text');
      const prevText = target.innerHTML;
      target.innerHTML = 'Copied';
      setTimeout(function() {
        target.innerHTML = prevText;
      }, 1000);
    };

    return {
      // ...pageData,
      id,
      name,
      product,
      productLoading,
      relatedProducts: computed(() => relatedProducts?.value?.data?.filter((p)=>parseInt(p.id) !== parseInt(id))),
      numeraiCorrMmcChartData: computed(() => !numerai?.value?.modelInfo ? {} : numeraiGetters.getNumeraiCorrMmcChartData(numerai.value)),
      numeraiTcChartData: computed(() => !numerai?.value?.modelInfo ? {} : numeraiGetters.getNumeraiTcChartData(numerai.value)),
      numeraiIcChartData: computed(() => !numerai?.value?.modelInfo ? {} : numeraiGetters.getNumeraiIcChartData(numerai.value)),
      numerai,
      numeraiLoading,
      globals,
      isAuthenticated,
      userLoading,
      models: computed(() => product ? userGetters.getModels(numerai.value, productGetters.getTournamentId(product), false) : []),
      order,
      orders,
      productGetters,
      numeraiGetters,
      orderGetters,
      userGetters,
      search,
      getModels,
      make,
      makeOrderLoading,
      makeOrderError,
      onCopy,
      orderSearch,
      getGlobals,
      send
    };
  }
};
</script>

<style lang="scss" scoped>
.is-invalid::v-deep .vs__dropdown-toggle {
  border-color: #dc3545 !important;
  border-top-color: rgb(220, 53, 69) !important;
  border-right-color: rgb(220, 53, 69) !important;
  border-bottom-color: rgb(220, 53, 69) !important;
  border-left-color: rgb(220, 53, 69) !important;
}
</style>
