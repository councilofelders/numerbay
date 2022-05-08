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
              <h1 class="item-detail-title mb-2 text-break">
                <a :href="modelUrl" class="" target="_blank" v-if="Boolean(modelUrl)">{{ title }}</a>
                <span v-else>{{ title }}</span>
              </h1>
              <div class="item-detail-meta d-flex flex-wrap align-items-center mb-3">
                <span class="item-detail-text-meta">Round <span
                  class="text-primary fw-semibold">{{ globals.selling_round }}</span></span>
                <span class="dot-separeted"></span>
                <span class="item-detail-text-meta">{{ category }}</span>
                <span class="dot-separeted"></span>
                <span class="item-detail-text-meta">Sold <span
                  class="text-primary fw-semibold">{{ productGetters.getQtySales(product) }}</span></span>
                <span class="dot-separeted" v-if="productGetters.getOnTimeRating(product)"></span>
                <span class="item-detail-text-meta" v-if="productGetters.getOnTimeRating(product)">On time <span
                  class="text-primary fw-semibold" :class="getDeliveryRateTextClass(productGetters.getOnTimeRating(product))" :title="`${productGetters.getQtyDelivered(product)} / ${productGetters.getQtySales(product)} quantity delivered on time`">{{ productGetters.getOnTimeRating(product) }}</span></span>
              </div>
              <div class="item-credits">
                <div class="row g-4">
                  <div class="col-xl-12">
                    <div class="card-media card-media-s1">
                      <div class="card-media-body">
                        <p class="fw-semibold text-black text-break">@{{ owner }}</p>
                        <span class="fw-medium small">Owner</span>
                        <ul class="social-links mt-2" v-if="hasSocials">
                          <li v-if="socialRocketChat"><a :href="socialRocketChat" target="_blank"><span class="ni icon"
                                                                                                        :class="`ni-chat`"></span>RocketChat</a>
                          </li>
                          <li v-if="socialLinkedIn"><a :href="socialLinkedIn" target="_blank"><span class="ni icon"
                                                                                                    :class="`ni-linkedin`"></span>LinkedIn</a>
                          </li>
                          <li v-if="socialTwitter"><a :href="socialTwitter" target="_blank"><span class="ni icon"
                                                                                                  :class="`ni-twitter`"></span>Twitter</a>
                          </li>
                          <li v-if="socialWebsite"><a :href="socialWebsite" target="_blank"><span class="ni icon"
                                                                                                  :class="`ni-globe`"></span>Website</a>
                          </li>
                        </ul>
                      </div>
                    </div><!-- end card -->
                  </div><!-- end col-->
                </div><!-- end row -->
              </div><!-- end row -->
              <div class="item-detail-btns mt-2">
                <ul class="btns-group d-flex">
                  <li class="flex-grow-1">
                    <a href="javascript:void(0);" @click="togglePlaceBidModal"
                       :class="`btn btn-dark d-block ${productGetters.getIsActive(product)?'':'disabled'}`">{{
                        productGetters.getIsActive(product) ? 'Buy' : 'Not for sale'
                      }}</a>
                  </li>
                </ul>
              </div><!-- end item-detail-btns -->
              <ModelMetricsCard
                class="mt-2"
                v-show="Boolean(productGetters.getCategory(product).is_per_model)"
                :tournament="productGetters.getCategory(product).tournament"
                :nmr-staked="nmrStaked"
                :stake-info="stakeInfo"
                :latest-returns="latestReturns"
                :latest-reps="latestReps"
                :latest-ranks="latestRanks"
                :show="{fnc: productGetters.getCategory(product).tournament==8, tc: productGetters.getCategory(product).tournament==8, ic: productGetters.getCategory(product).tournament==11}"
              ></ModelMetricsCard>
            </div><!-- end item-detail-content -->
          </div><!-- end col -->
          <div class="col-lg-9 ms-auto">
            <div class="item-detail-content">
              <div class="item-detail-chart-container mb-4" v-if="Boolean(productGetters.getCategory(product).is_per_model)">
                <div class="card-border card-full">
                  <div class="card-body card-body-s1">
                    <h5 class="mb-3">Recent Performance</h5>
                    <div class="item-detail-list" v-if="isNumeraiChartReady">
                      <NumeraiChart class="numerai-chart" :chartdata="numeraiCorrTcChartData" v-if="productGetters.getCategory(product).tournament==8"></NumeraiChart>
                      <NumeraiChart class="numerai-chart" :chartdata="numeraiCorrMmcChartData" v-if="productGetters.getCategory(product).tournament==11"></NumeraiChart>
                      <NumeraiChart v-if="productGetters.getCategory(product).tournament==11" class="numerai-chart"
                                    :chartdata="numeraiIcChartData"></NumeraiChart>
                    </div>
                    <div class="item-detail-list placeholder-glow" v-else>
                      <svg class="bd-placeholder-img placeholder" width="100%" :height="productGetters.getCategory(product).tournament==8 ? 240 : 480"
                           xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder"
                           preserveAspectRatio="xMidYMid slice" focusable="false"><title>Placeholder</title>
                        <rect width="100%" height="100%" fill="#868e96"></rect>
                      </svg>
                    </div>
                  </div><!-- end card-body -->
                </div><!-- end card-border -->
              </div><!-- end item-detail-chart-container -->
              <div class="item-detail-description-container mb-4">
                <div class="card-border card-full">
                  <div class="card-body card-body-s1">
                    <h5 class="mb-3">Description</h5>
                    <div class="ql-container ql-snow" style="border: none;">
                      <div class="item-detail-text mb-4 ql-editor" v-html="description"></div>
                    </div>
                  </div><!-- end card-body -->
                </div><!-- end card-border -->
              </div><!-- end item-detail-description-container -->
            </div><!-- end item-detail-content -->
          </div><!-- end col -->
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
              <v-select class="generic-select generic-select-s1" ref="optionDropdown" v-model="optionIdx"
                        v-if="!!product" label="id"
                        :options="productGetters.getOrderedOptions(product)" :reduce="option => option.index"
                        :clearable=false @input="handleSubmit(onOptionChange)">
                <template #selected-option="option">
                  {{ productGetters.getFormattedOption(option) }}
                </template>
                <template v-slot:option="option">
                  {{ productGetters.getFormattedOption(option) }}
                </template>
              </v-select>
            </div>
            <ValidationProvider rules="required|integer|min_value:1|max_value:10" v-slot="{ errors }"
                                v-if="isOnPlatform" slim>
              <div class="mb-3">
                <label class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Enter quantity</label>
                <input type="number" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'"
                       v-model="quantity" min="1" max="10" step="1" @change="handleSubmit(onQuantityChange)">
                <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
              </div>
            </ValidationProvider>
            <div v-if="isAuthenticated">
              <div class="d-flex flex-wrap align-items-center justify-content-between"
                 v-if="!!product && isOnPlatform && productGetters.getCategory(product).is_submission">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" v-model="autoSubmit" id="autoSubmit"
                         :disabled="!isAutoSubmitOptional">
                  <label class="form-check-label form-check-label-s1" for="autoSubmit"> {{ autoSubmitText }} </label>
                </div>
              </div>
              <ValidationProvider rules="required" v-slot="{ errors }" v-if="autoSubmit" slim>
                <div class="mb-3">
                  <label class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Select a submission
                    slot</label>
                  <v-select class="generic-select generic-select-s1" :class="!errors[0] ? '' : 'is-invalid'"
                            ref="slotDropdown" v-model="submitSlot" v-if="!!product && !numeraiLoading" label="name"
                            :options="userGetters.getModels(numerai, productGetters.getTournamentId(product), false)"
                            :reduce="model => model.id" :clearable=true></v-select>
                  <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                </div>
              </ValidationProvider>
            </div>
            <ul class="total-bid-list mt-4" v-if="isOnPlatform">
              <li><span>{{
                  (!!product && productGetters.getCategory(product).is_per_round) ? 'Total number of rounds' : 'Total order quantity'
                }}</span> <span>{{
                  productGetters.getCategory(product).is_per_round ? productGetters.getOrderedOption(product, optionIdx).quantity : quantity
                }}</span></li>
              <li><span>You will pay</span> <span>{{ formattedTotalPrice }}</span></li>
            </ul>
            <div v-if="isAuthenticated">
              <div class="d-flex flex-wrap align-items-center justify-content-between mt-2">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" v-model="useCoupon" id="useCoupon"
                         :disabled="Boolean(couponApplied)">
                  <label class="form-check-label form-check-label-s1" for="useCoupon"> (Optional) Apply coupon
                    code </label>
                </div>
              </div>
              <div class="mb-3 mt-2" v-show="useCoupon">
                <div class="row g-4">
                  <div class="col-8">
                    <input type="text" class="form-control form-control-s1" :class="!couponError ? '' : 'is-invalid'"
                           placeholder="Coupon code" v-model="coupon" :disabled="Boolean(couponApplied)">
                    <div class="text-danger fade" :class="{ 'show': Boolean(couponError) }">{{ couponError }}</div>
                  </div>
                  <div class="col-4">
                    <button class="btn btn-dark" @click="handleCoupon">{{ couponApplied ? 'Remove' : 'Apply' }}</button>
                  </div>
                </div>
              </div>
              <div class="d-flex flex-wrap align-items-center justify-content-between mt-2 mb-4"
                   v-if="!!product && isOnPlatform">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" v-model="terms" id="terms">
                  <label class="form-check-label form-check-label-s1" for="terms"> I understand that I need to make
                    payment in <strong>1 single transaction</strong>, and neither Numerai nor NumerBay is liable for any
                    loss resulted from this transaction. </label>
                </div>
              </div>
              <button @click="handleSubmit(onPlaceOrder)" class="btn btn-dark btn-full d-flex justify-content-center"
                      :disabled="isOnPlatform && (makeOrderLoading || !terms)">
                <span v-if="makeOrderLoading"><span class="spinner-border spinner-border-sm me-2" role="status"></span>Placing Order...</span>
                <span v-else>{{ buyBtnText }}</span>
              </button>
            </div>
            <div v-else>
              <router-link to="/login-v2" class="btn btn-dark btn-full d-flex justify-content-center mt-4">Login</router-link>
            </div>
          </ValidationObserver>
        </div>
        <div v-if="paymentStep === 2">
          <p class="mb-3">Please complete the payment within <strong>45 minutes</strong></p>
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
                <button v-clipboard:copy="JSON.stringify(amount)" v-clipboard:success="onCopy" class="copy-text"
                        type="button">
                  <span class="tooltip-s1-text tooltip-text">Copy</span>
                  <em class="ni ni-copy"></em>
                </button>
              </div>
            </div>
          </div>
          <div class="mb-2">
          <a href="https://numer.ai/wallet" target="_blank" class="btn btn-dark d-block">Open Numerai Wallet (Gas-free)</a>
          </div>
          <div class="mb-2">
          <a href="javascript:void(0);" @click="pay" class="btn btn-light d-block">Pay with MetaMask</a>
          </div>
          <div class="mb-2" v-if="paymentMessage">
            <span class="spinner-border spinner-border-sm text-primary me-2" role="status"></span>
            <span class="text-primary">{{ paymentMessage }}</span>
          </div>
        </div>
      </Modal><!-- end modal-->
    </section><!-- end item-detail-section -->
    <!-- Related product -->
    <RelatedProducts title="Featured by seller" :products="relatedProducts"
                     v-if="Boolean(relatedProducts) && relatedProducts.length > 0"></RelatedProducts>
  </div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

import ModelMetricsCard from "@/components/section/ModelMetricsCard";
import NumeraiChart from '@/components/section/NumeraiChart';
import RelatedProducts from "@/components/section/RelatedProducts";

// Composables
import {onSSR} from '@vue-storefront/core';
import {computed} from '@vue/composition-api';
import {
  cartGetters,
  numeraiGetters,
  orderGetters,
  productGetters,
  useGlobals,
  useMakeOrder,
  useNumerai,
  useProduct,
  useUser,
  useUserOrder,
  userGetters
} from '@vue-storefront/numerbay';
import {useUiNotification} from '~/composables';
import { ethers } from 'ethers';
import {contractAddress, transferAbi} from "../plugins/nmr";

export default {
  name: 'ProductDetails',
  components: {
    ModelMetricsCard,
    NumeraiChart,
    RelatedProducts
  },
  data() {
    return {
      placeBidModal: null,
      paymentStep: 1,
      optionIdx: 0,
      quantity: 1,
      amount: 0,
      toAddress: '',
      useCoupon: false,
      coupon: null,
      terms: false,
      autoSubmit: false,
      submitSlot: null,
      paymentMessage: null,
      SectionData
    };
  },
  computed: {
    selectedOption() {
      return this.productGetters.getOrderedOption(this.product, this.optionIdx);
    },
    category() {
      return this.$route.params.category || this.productGetters.getCategory(this.product).slug;
    },
    isOnPlatform() {
      return this.productGetters.getOptionIsOnPlatform(this.selectedOption);
    },
    isAutoSubmitOptional() {
      return !this.productGetters.getOptionIsOnPlatform(this.selectedOption) || this.productGetters.getMode(this.selectedOption) === 'file';
    },
    autoSubmitText() {
      return this.isAutoSubmitOptional ? '(Optional) Auto-submit this model to Numerai for me' : 'Auto-submit this model to Numerai for me';
    },
    buyBtnText() {
      return this.isOnPlatform ? 'Place an Order' : 'Visit external listing';
    },
    owner() {
      return this.$route.params.owner || this.productGetters.getOwner(this.product);
    },
    socialRocketChat() {
      return this.product?.owner?.social_rocketchat;
    },
    socialLinkedIn() {
      return this.product?.owner?.social_linkedin;
    },
    socialTwitter() {
      return this.product?.owner?.social_twitter;
    },
    socialWebsite() {
      return this.product?.owner?.social_website;
    },
    hasSocials() {
      return Boolean(this.socialRocketChat || this.socialLinkedIn || this.socialTwitter || this.socialWebsite);
    },
    isNumeraiChartReady() {
      return !this.productLoading && !this.numeraiLoading && Boolean(this.productGetters.getCategory(this.product).is_per_model) && Boolean(this.numerai.modelInfo);
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
    stakeInfo() {
      return {
        corrMultiplier: this.$route.params.stakeInfoCorrMultiplier || this.productGetters.getModelStakeInfo(this.product, 'corrMultiplier') || (this.productGetters.getCategory(this.product).tournament === 8 ? 0 : 2),
        mmcMultiplier: this.$route.params.stakeInfoMmcMultiplier || this.productGetters.getModelStakeInfo(this.product, 'mmcMultiplier') || 0,
        tcMultiplier: this.$route.params.stakeInfoTcMultiplier || this.productGetters.getModelStakeInfo(this.product, 'tcMultiplier') || 0
      };
    },
    latestRanks() {
      return {
        corr: this.$route.params.latestRankCorr || this.productGetters.getModelRank(this.product, 'corr'),
        mmc: this.$route.params.latestRankMmc || this.productGetters.getModelRank(this.product, 'mmc'),
        fnc: this.$route.params.latestRankFnc || this.productGetters.getModelRank(this.product, 'fnc'),
        fncV3: this.$route.params.latestRankFncV3 || this.productGetters.getModelRank(this.product, 'fncV3'),
        tc: this.$route.params.latestRankTc || this.productGetters.getModelRank(this.product, 'tc'),
        ic: this.$route.params.latestRankIc || this.productGetters.getModelRank(this.product, 'ic')
      };
    },
    latestReps() {
      return {
        corr: this.$route.params.latestRepCorr || this.productGetters.getModelRep(this.product, 'corr'),
        mmc: this.$route.params.latestRepMmc || this.productGetters.getModelRep(this.product, 'mmc'),
        fnc: this.$route.params.latestRepFnc || this.productGetters.getModelRep(this.product, 'fnc'),
        fncV3: this.$route.params.latestRepFncV3 || this.productGetters.getModelRep(this.product, 'fncV3'),
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
      const option = this.selectedOption;
      return `${((option.special_price === null || option.special_price === undefined) ? option.price : option.special_price)?.toFixed(4)} ${option.currency}`;
    },
    couponError() {
      const option = this.selectedOption;
      return option?.error;
    },
    couponApplied() {
      return cartGetters.getAppliedCoupon(this.selectedOption)?.code;
    }
  },
  methods: {
    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    async onOptionChange(option) {
      await this.search({
        id: this.id,
        categorySlug: this.category,
        name: this.name,
        qty: this.quantity,
        coupon: this.coupon
      });
    },
    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    async onQuantityChange(quantity) {
      await this.search({
        id: this.id,
        categorySlug: this.category,
        name: this.name,
        qty: this.quantity,
        coupon: this.coupon
      });
    },
    async handleCoupon() {
      const couponApplied = cartGetters.getAppliedCoupon(this.selectedOption)?.code;
      if (couponApplied) {
        this.coupon = null;
      }
      await this.search({
        id: this.id,
        categorySlug: this.category,
        name: this.name,
        qty: this.quantity,
        coupon: this.coupon
      });
    },
    async onPlaceOrder() {
      const option = this.selectedOption;
      if (!this.productGetters.getOptionIsOnPlatform(option)) {
        // visit external listing
        window.open(option.third_party_url, '_blank');
        return;
      }

      const optionId = option.id;
      await this.make({
        id: this.productGetters.getId(this.product),
        optionId,
        submitModelId: this.submitSlot,
        quantity: this.quantity,
        coupon: this.coupon
      })
      if (this.makeOrderError?.make) {
        this.send({
          message: this.makeOrderError.make.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
      } else {
        this.toAddress = this.orderGetters.getToAddress(this.order);
        this.amount = this.orderGetters.getPrice(this.order);
        if (this.amount === 0) { // Go straight to purchases page if the order if free
          await this.$router.push('/purchases');
        } else {
          this.paymentStep = 2;
        }
      }
    },
    async pay() {
      if (!userGetters.getPublicAddress(this.user)) {
        this.send({
          message: 'Please connect a MetaMask wallet',
          type: 'bg-danger',
          icon: 'ni-alert-circle',
          persist: true,
          action: {
            text: 'Connect now',
            onClick: async () => {
              await this.$router.push('/account');
            }
          }
        });
        return;
      }

      if (userGetters.getPublicAddress(this.user).toUpperCase() !== this.$wallet.account.toUpperCase()) {
        this.send({
          message: 'Please use the MetaMask wallet connected to your NumerBay account',
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
        return;
      }

      const signer = await this.$wallet.provider.getSigner();
      const contract = new ethers.Contract(contractAddress, transferAbi, signer);

      // const balance = await contract.balanceOf(userGetters.getPublicAddress(this.user));
      // console.log('balance: ' + ethers.utils.formatUnits(balance, 18));

      const numberOfTokens = ethers.utils.parseUnits(String(this.amount), 18);

      this.paymentMessage = 'Waiting for payment approval';
      await contract.transfer(this.toAddress, numberOfTokens).then(async (tx) => {
        this.paymentMessage = 'Waiting for transaction response';
        await this.$wallet.provider.getTransaction(tx.hash).then(async (transaction) => {
          await transaction.wait().then(async (receipt) => {
            this.paymentMessage = 'Validating payment';
            await this.validatePayment({orderId: this.orderGetters.getId(this.orders?.data[0]), transactionHash: receipt.transactionHash});
            this.paymentMessage = null;
            if (this.userOrderError?.validatePayment) {
              await this.send({
                message: this.userOrderError.validatePayment.message,
                type: 'bg-danger',
                icon: 'ni-alert-circle'
              });
            } else {
              await this.send({
                message: 'Payment success',
                type: 'bg-success',
                icon: 'ni-alert-circle'
              });
              await this.$router.push('/purchases');
            }
          });
        })
      }).catch(async (e) => {
        this.paymentMessage = null;
        let message = e.message;
        if (message.includes('UNPREDICTABLE_GAS_LIMIT')) {
          message = 'Insufficient balance or exceeded gas limit';
        }
        this.send({
          message: message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
      });
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
      this.placeBidModal?.toggle();
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
        await this.getGlobals();
        // eslint-disable-next-line camelcase
        await this.orderSearch({
          role: 'buyer',
          filters: {
            product: {in: [this.productGetters.getId(this.product)]},
            round_order: {in: [this.globals.selling_round]},
            state: {in: ['pending', 'confirmed']}
          }
        });
        if (this.orders?.data?.length > 0) {
          if (this.orders?.data[0].state === 'pending') {
            this.toAddress = this.orderGetters.getToAddress(this.orders?.data[0]);
            this.amount = this.orderGetters.getPrice(this.orders?.data[0]);
            this.paymentStep = 2;
            this.send({
              message: 'Please complete the payment for your pending order',
              type: 'bg-warning',
              icon: 'ni-alert-circle',
              persist: true
            });
          } else {
            this.send({
              message: 'You already bought this product for this round',
              type: 'bg-warning',
              icon: 'ni-alert-circle',
              persist: true
            });
            try {
              this.placeBidModal?.dispose();
            } finally {
              await this.$router.push('/purchases');
            }
          }
        }
      }, false);

      modal?.addEventListener('shown.bs.modal', () => {
        this.$refs.optionDropdown?.$refs?.search?.focus();
        if (this.isAuthenticated) {
          this.getModels().catch((e) => {
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
          });
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
    const {id, category, name} = context.root.$route.params;
    const cacheKey = String(id || (category + name));
    const {products, search, loading: productLoading} = useProduct(cacheKey);
    const {
      products: relatedProducts,
      search: searchRelatedProducts,
      loading: relatedLoading
    } = useProduct(`relatedProducts-${cacheKey}`);
    const {numerai, getModels, getModelInfo, loading: numeraiLoading} = useNumerai(cacheKey);
    const {globals, getGlobals, loading: globalsLoading} = useGlobals();
    const {user, isAuthenticated, loading: userLoading} = useUser();
    const {order, make, loading: makeOrderLoading, error: makeOrderError} = useMakeOrder();
    const {orders, search: orderSearch, validatePayment, error: userOrderError} = useUserOrder('product');
    const {send} = useUiNotification();

    const product = computed(() => (products.value.data || [])[0]);

    onSSR(async () => {
      await search({id, categorySlug: category, name}).then(async () => {
        await searchRelatedProducts({filters: {id: {in: product?.value?.featured_products || []}}});
        if (product.value?.category?.is_per_model) {
          await getModelInfo({
            tournament: product.value?.category?.slug.startsWith('signals') ? 11 : 8,
            modelName: product.value?.name
          });
        }
        await getGlobals();
      });
    });

    const onCopy = (e) => {
      const target = e.trigger.querySelector('.tooltip-text');
      const prevText = target.innerHTML;
      target.innerHTML = 'Copied';
      setTimeout(function () {
        target.innerHTML = prevText;
      }, 1000);
    };

    const getDeliveryRateTextClass = (rating) => {
      switch (rating) {
        case 'always':
          return 'text-success';
        case 'good':
          return 'text-success';
        case 'average':
          return 'text-warning';
        case 'poor':
          return 'text-danger';
        default:
          return '';
      }
    };

    return {
      id,
      name,
      product,
      productLoading,
      relatedProducts: computed(() => relatedProducts?.value?.data?.filter((p) => parseInt(p.id) !== parseInt(id))),
      relatedLoading,
      numeraiCorrMmcChartData: computed(() => !numerai?.value?.modelInfo ? {} : numeraiGetters.getNumeraiCorrMmcChartData(numerai.value)),
      numeraiCorrTcChartData: computed(() => !numerai?.value?.modelInfo ? {} : numeraiGetters.getNumeraiCorrTcChartData(numerai.value)),
      numeraiIcChartData: computed(() => !numerai?.value?.modelInfo ? {} : numeraiGetters.getNumeraiIcChartData(numerai.value)),
      numerai,
      numeraiLoading,
      globals,
      globalsLoading,
      isAuthenticated,
      userLoading,
      models: computed(() => product ? userGetters.getModels(numerai.value, productGetters.getTournamentId(product), false) : []),
      order,
      orders,
      validatePayment,
      userOrderError,
      user,
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
      send,
      getDeliveryRateTextClass
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
