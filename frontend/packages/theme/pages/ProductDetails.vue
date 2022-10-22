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
                <a v-if="Boolean(modelUrl)" :href="modelUrl" class="" target="_blank">{{ title }}</a>
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
                <span v-if="productGetters.getOnTimeRating(product)" class="dot-separeted"></span>
                <span v-if="productGetters.getOnTimeRating(product)" class="item-detail-text-meta">On time <span
                  :class="getDeliveryRateTextClass(productGetters.getOnTimeRating(product))"
                  :title="`${productGetters.getQtyDelivered(product)} / ${productGetters.getQtySales(product)} quantity delivered on time`"
                  class="text-primary fw-semibold">{{
                    productGetters.getOnTimeRating(product)
                  }}</span></span>
              </div>
              <div class="item-credits">
                <div class="row g-4">
                  <div class="col-xl-12">
                    <div class="card-media card-media-s1">
                      <div class="card-media-body">
                        <p class="fw-semibold text-black text-break">@{{ owner }}</p>
                        <span class="fw-medium small">Owner</span>
                        <ul v-if="hasSocials" class="social-links mt-2">
                          <li v-if="socialRocketChat"><a :href="socialRocketChat" target="_blank"><span
                            :class="`ni-chat`"
                            class="ni icon"></span>RocketChat</a>
                          </li>
                          <li v-if="socialLinkedIn"><a :href="socialLinkedIn" target="_blank"><span
                            :class="`ni-linkedin`"
                            class="ni icon"></span>LinkedIn</a>
                          </li>
                          <li v-if="socialTwitter"><a :href="socialTwitter" target="_blank"><span :class="`ni-twitter`"
                                                                                                  class="ni icon"></span>Twitter</a>
                          </li>
                          <li v-if="socialWebsite"><a :href="socialWebsite" target="_blank"><span :class="`ni-globe`"
                                                                                                  class="ni icon"></span>Website</a>
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
                    <a :class="`btn btn-dark d-block ${productGetters.getIsActive(product)?'':'disabled'}`"
                       href="javascript:void(0);"
                       @click="togglePlaceBidModal">{{
                        productGetters.getIsActive(product) ? 'Buy' : 'Not for sale'
                      }}</a>
                  </li>
                </ul>
              </div><!-- end item-detail-btns -->
              <ModelMetricsCard
                v-show="Boolean(productGetters.getCategory(product).is_per_model)"
                :latest-ranks="latestRanks"
                :latest-reps="latestReps"
                :latest-returns="latestReturns"
                :nmr-staked="nmrStaked"
                :show="{fnc: !isSignalsTournament, tc: true, ic: isSignalsTournament}"
                :stake-info="stakeInfo"
                :tournament="productGetters.getCategory(product).tournament"
                class="mt-2"
              ></ModelMetricsCard>
            </div><!-- end item-detail-content -->
          </div><!-- end col -->
          <div class="col-lg-9 ms-auto">
            <div class="item-detail-content">
              <div v-if="Boolean(productGetters.getCategory(product).is_per_model)"
                   class="item-detail-chart-container mb-4">
                <div class="card-border card-full">
                  <div class="card-body card-body-s1">
                    <h5 class="mb-3">Recent Performance</h5>
                    <div v-if="isNumeraiChartReady" class="item-detail-list">
                      <NumeraiChart v-if="!isSignalsTournament" :chartdata="numeraiCorrCorr60TcChartData"
                                    class="numerai-chart"></NumeraiChart>
                      <NumeraiChart v-if="isSignalsTournament" :chartdata="numeraiCorrChartData"
                                    class="numerai-chart"></NumeraiChart>
                      <NumeraiChart v-if="isSignalsTournament" :chartdata="numeraiTcIcChartData"
                                    class="numerai-chart"></NumeraiChart>
                    </div>
                    <div v-else class="item-detail-list placeholder-glow">
                      <svg :height="isSignalsTournament ? 480 : 240" aria-label="Placeholder"
                           class="bd-placeholder-img placeholder"
                           focusable="false" preserveAspectRatio="xMidYMid slice" role="img"
                           width="100%" xmlns="http://www.w3.org/2000/svg"><title>Placeholder</title>
                        <rect fill="#868e96" height="100%" width="100%"></rect>
                      </svg>
                    </div>
                  </div><!-- end card-body -->
                </div><!-- end card-border -->
              </div><!-- end item-detail-chart-container -->
              <div class="item-detail-performance-table-container mb-4"
                   v-if="Boolean(productGetters.getCategory(product).is_per_model)">
                <div class="card-border card-full">
                  <div class="card-body card-body-s1">
                    <h5 class="mb-3">Recent Rounds</h5>
                    <div class="table-responsive-xl" v-if="isNumeraiChartReady">
                      <table class="table mb-0 table-s2">
                        <thead class="fs-15 text-center">
                        <tr>
                          <th v-for="(header, i) in performanceTableHeaders" :key="i" scope="col"><span class="tooltip-s1">{{ header.name }}<span
                              class="tooltip-s1-text tooltip-text fw-normal" v-if="!!header.description">{{ header.description }}</span></span>
                          </th>
                        </tr>
                        </thead>
                        <tbody class="fs-15">
                        <tr
                          v-for="(roundPerformance, j) in numerai.modelInfo.modelPerformance.roundModelPerformances.slice(0, 6)"
                          :key="j">
                          <th scope="row">{{ roundPerformance.roundNumber }}</th>
                          <td class="text-end"><span><span
                            class="tooltip-s1">{{ formatDecimal(Number(roundPerformance.selectedStakeValue), 2) }} NMR<span
                            class="tooltip-s1-text tooltip-text">{{
                              `${roundPerformance.selectedStakeValue} NMR`
                            }}</span></span></span></td>
                          <td class="text-end">
                            <span v-if="stakeInfo.corrMultiplier"> {{ stakeInfo.corrMultiplier }}xCORR</span>
                            <span v-if="stakeInfo.tcMultiplier"> {{ stakeInfo.tcMultiplier }}xTC</span>
                          </td>
                          <td class="text-end"><span class="tooltip-s1">{{
                              formatDecimal(roundPerformance.corr, 4)
                            }}<span
                              class="tooltip-s1-text tooltip-text">Percentile: {{
                                formatDecimal(roundPerformance.corrPercentile * 100, 1)
                              }}</span></span></td>
                          <td class="text-end"><span class="tooltip-s1">{{
                              formatDecimal(roundPerformance.corr60, 4)
                            }}<span
                              class="tooltip-s1-text tooltip-text">Percentile: {{
                                formatDecimal(roundPerformance.corr60Percentile * 100, 1)
                              }}</span></span></td>
                          <td class="text-end" v-if="isSignalsTournament"><span
                            class="tooltip-s1">{{ formatDecimal(roundPerformance.ic, 4) }}<span
                            class="tooltip-s1-text tooltip-text">Percentile: {{
                              formatDecimal(roundPerformance.icPercentile * 100, 1)
                            }}</span></span></td>
                          <td class="text-end" v-if="!isSignalsTournament"><span
                            class="tooltip-s1">{{ formatDecimal(roundPerformance.fncV3, 4) }}<span
                            class="tooltip-s1-text tooltip-text">Percentile: {{
                              formatDecimal(roundPerformance.fncV3Percentile * 100, 1)
                            }}</span></span></td>
                          <td class="text-end"><span
                            class="tooltip-s1 text-primary">{{ formatDecimal(roundPerformance.tc, 4) }}<span
                            class="tooltip-s1-text tooltip-text">Percentile: {{
                              formatDecimal(roundPerformance.tcPercentile * 100, 1)
                            }}</span></span></td>
                          <td class="text-end"><span class="tooltip-s1 text-primary"><span
                            :class="`text-${getMetricColor(Number(roundPerformance.payout) || 0)}`">{{
                              formatPayout(roundPerformance.payout)
                            }}</span><span
                            class="tooltip-s1-text tooltip-text">{{
                              `${roundPerformance.payout} NMR`
                            }}</span></span></td>
                        </tr>
                        </tbody>
                      </table>
                    </div><!-- end table-responsive -->
                    <a target="_blank" class="btn btn-light btn-full d-flex justify-content-center mt-1"
                       :href="`${productGetters.getModelUrl(product)}/submissions`">All Rounds</a>
                  </div><!-- end card-body -->
                </div><!-- end card-border -->
              </div><!-- end item-detail-performance-table-container -->
              <div class="item-detail-description-container mb-4">
                <div class="card-border card-full">
                  <div class="card-body card-body-s1">
                    <h5 class="mb-3">Description</h5>
                    <div class="ql-container ql-snow" style="border: none;">
                      <div class="item-detail-text mb-4 ql-editor" v-sanitize="description"></div>
                    </div>
                  </div><!-- end card-body -->
                </div><!-- end card-border -->
              </div><!-- end item-detail-description-container -->
            </div><!-- end item-detail-content -->
          </div><!-- end col -->
        </div><!-- end row -->
      </div><!-- .container -->
      <!-- Modal -->
      <Modal ref="placeBidModal" modal-id="placeBidModal" @registeredModal="placeBidModal = $event">
        <template slot="title">{{ paymentStep === 1 ? `Place an Order` : `Payment` }}</template>
        <div v-if="paymentStep === 1">
          <p class="mb-3">You are about to buy <strong>{{ title }}</strong> from <strong>{{ owner }}</strong></p>
          <ValidationObserver v-slot="{ handleSubmit }">
            <div class="mb-3">
              <label class="form-label">Select an option</label>
              <v-select v-if="!!product" ref="optionDropdown" v-model="optionIdx"
                        :clearable=false :options="productGetters.getOrderedOptions(product)"
                        :reduce="option => option.index" class="generic-select generic-select-s1"
                        label="id" @input="handleSubmit(onOptionChange)">
                <template #selected-option="option">
                  {{ productGetters.getFormattedOption(option) }}
                </template>
                <template v-slot:option="option">
                  {{ productGetters.getFormattedOption(option) }}
                </template>
              </v-select>
            </div>
            <ValidationProvider v-if="isOnPlatform" v-slot="{ errors }"
                                rules="required|integer|min_value:1|max_value:10" slim>
              <div class="mb-3">
                <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label">Enter quantity (weekly)</label>
                <input v-model="quantity" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                       max="10" min="1" step="1" type="number" @change="handleSubmit(onQuantityChange)">
                <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
              </div>
            </ValidationProvider>
            <div v-if="isAuthenticated">
              <div v-if="!!product && isOnPlatform && productGetters.getCategory(product).is_submission"
                   class="d-flex flex-wrap align-items-center justify-content-between">
                <div class="form-check">
                  <input id="autoSubmit" v-model="autoSubmit" :disabled="!isAutoSubmitOptional" class="form-check-input"
                         type="checkbox">
                  <label class="form-check-label form-check-label-s1" for="autoSubmit"> {{ autoSubmitText }} </label>
                </div>
              </div>
              <ValidationProvider v-if="autoSubmit" v-slot="{ errors }" rules="required" slim>
                <div class="mb-3">
                  <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label">Select a submission
                    slot</label>
                  <v-select v-if="!!product && !numeraiLoading" ref="slotDropdown"
                            v-model="submitSlot" :class="!errors[0] ? '' : 'is-invalid'" :clearable=true
                            :options="userGetters.getModels(numerai, productGetters.getTournamentId(product), false)"
                            :reduce="model => model.id"
                            class="generic-select generic-select-s1" label="name"></v-select>
                  <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                </div>
              </ValidationProvider>
            </div>
            <ul v-if="isOnPlatform" class="total-bid-list mt-4">
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
                  <input id="useCoupon" v-model="useCoupon" :disabled="Boolean(couponApplied)" class="form-check-input"
                         type="checkbox">
                  <label class="form-check-label form-check-label-s1" for="useCoupon"> (Optional) Apply coupon
                    code </label>
                </div>
              </div>
              <div v-show="useCoupon" class="mb-3 mt-2">
                <div class="row g-4">
                  <div class="col-8">
                    <input v-model="coupon" :class="!couponError ? '' : 'is-invalid'" :disabled="Boolean(couponApplied)"
                           class="form-control form-control-s1" placeholder="Coupon code" type="text">
                    <div :class="{ 'show': Boolean(couponError) }" class="text-danger fade">{{ couponError }}</div>
                  </div>
                  <div class="col-4">
                    <button class="btn btn-dark" @click="handleCoupon">{{ couponApplied ? 'Remove' : 'Apply' }}</button>
                  </div>
                </div>
              </div>
              <div v-if="!!product && isOnPlatform"
                   class="d-flex flex-wrap align-items-center justify-content-between mt-2 mb-4">
                <div class="form-check">
                  <input id="terms" v-model="terms" class="form-check-input" type="checkbox">
                  <label class="form-check-label form-check-label-s1" for="terms"> I understand that I need to make
                    payment in <strong>1 single transaction</strong>, and neither Numerai nor NumerBay is liable for any
                    loss resulted from this transaction. </label>
                </div>
              </div>
              <button :disabled="isOnPlatform && (makeOrderLoading || !terms)"
                      class="btn btn-dark btn-full d-flex justify-content-center"
                      @click="handleSubmit(onPlaceOrder)">
                <span v-if="makeOrderLoading"><span class="spinner-border spinner-border-sm me-2" role="status"></span>Placing Order...</span>
                <span v-else>{{ buyBtnText }}</span>
              </button>
            </div>
            <div v-else>
              <router-link class="btn btn-dark btn-full d-flex justify-content-center mt-4" to="/login-v2">Login
              </router-link>
            </div>
          </ValidationObserver>
        </div>
        <div v-if="paymentStep === 2">
          <p class="mb-3">Please complete the payment within <strong>45 minutes</strong></p>
          <div class="mb-3">
            <label class="form-label">Seller wallet address</label>
            <div class="d-flex align-items-center border p-3 rounded-3">
              <input id="copy-input-address" v-model="toAddress" class="copy-input copy-input-s1" readonly type="text">
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
              <input id="copy-input-amount" v-model="amount" class="copy-input copy-input-s1" readonly type="text">
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
            <a class="btn btn-dark d-block" href="https://numer.ai/wallet" target="_blank">Open Numerai Wallet
              (Gas-free)</a>
          </div>
          <div class="mb-2">
            <a class="btn btn-light d-block" href="javascript:void(0);" @click="pay">Pay with MetaMask</a>
          </div>
          <div v-if="paymentMessage" class="mb-2">
            <span class="spinner-border spinner-border-sm text-primary me-2" role="status"></span>
            <span class="text-primary">{{ paymentMessage }}</span>
          </div>
        </div>
      </Modal><!-- end modal-->
    </section><!-- end item-detail-section -->
    <!-- Related product -->
    <RelatedProducts v-if="Boolean(relatedProducts) && relatedProducts.length > 0" :products="relatedProducts"
                     title="Featured by seller"></RelatedProducts>
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
import {ethers} from 'ethers';
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
      orderId: null,
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
    isSignalsTournament() {
      return this.productGetters.getCategory(this.product).tournament !== 8;
    },
    performanceTableHeaders() {
      return this.isSignalsTournament ? [
        {name: 'Round', description: null},
        {name: 'At-risk', description: 'The NMR at-risk for this model for this particular round. Equal to the model’s stake value minus any pending releases at round deadline.'},
        {name: 'Stake Type', description: null},
        {name: 'CORR', description: 'Correlation of submission with the 20-day signals target'},
        {name: 'CORR60', description: 'Correlation of submission with the 60-day signals target'},
        {name: 'IC', description: 'Mean correlation of this un-neutralized submission with bucketed raw returns'},
        {name: 'TC', description: 'How much this submission contributed to Meta Model performance'},
        {name: 'Payout', description: 'Latest projected payout'},
      ] : [
        {name: 'Round', description: null},
        {name: 'At-risk', description: 'The NMR at-risk for this model for this particular round. Equal to the model’s stake value minus any pending releases at round deadline.'},
        {name: 'Stake Type', description: null},
        {name: 'CORR', description: 'Correlation of submission with target nomi_20'},
        {name: 'CORJ60', description: 'Correlation of submission with target_jerome_v4_60'},
        {name: 'FNCV3', description: 'The mean correlation of this submission after it have been neutralized to the 420 features in the medium subset of the V3 dataset'},
        {name: 'TC', description: 'How much this submission contributed to Meta Model performance'},
        {name: 'Payout', description: 'Latest projected payout'},
      ]
    },
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
        corrMultiplier: this.$route.params.stakeInfoCorrMultiplier || this.productGetters.getModelStakeInfo(this.product, 'corrMultiplier') || (this.isSignalsTournament ? 2 : 0),
        mmcMultiplier: this.$route.params.stakeInfoMmcMultiplier || this.productGetters.getModelStakeInfo(this.product, 'mmcMultiplier') || 0,
        tcMultiplier: this.$route.params.stakeInfoTcMultiplier || this.productGetters.getModelStakeInfo(this.product, 'tcMultiplier') || 0
      };
    },
    latestRanks() {
      return {
        corr: this.$route.params.latestRankCorr || this.productGetters.getModelRank(this.product, 'corr'),
        corr60: this.$route.params.latestRankCorr60 || this.productGetters.getModelRank(this.product, 'corr60'),
        fnc: this.$route.params.latestRankFnc || this.productGetters.getModelRank(this.product, 'fnc'),
        fncV3: this.$route.params.latestRankFncV3 || this.productGetters.getModelRank(this.product, 'fncV3'),
        tc: this.$route.params.latestRankTc || this.productGetters.getModelRank(this.product, 'tc'),
        ic: this.$route.params.latestRankIc || this.productGetters.getModelRank(this.product, 'ic')
      };
    },
    latestReps() {
      return {
        corr: this.$route.params.latestRepCorr || this.productGetters.getModelRep(this.product, 'corr'),
        corr60: this.$route.params.latestRepCorr60 || this.productGetters.getModelRep(this.product, 'corr60'),
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
        this.orderId = this.orderGetters.getId(this.order);
        this.toAddress = this.orderGetters.getToAddress(this.order);
        this.amount = this.orderGetters.getPrice(this.order);
        if (this.amount === 0) { // Go straight to purchases page if the order if free
          await this.$router.push('/purchases');
        } else {
          this.paymentStep = 2;
        }
      }
    },
    async onTransactionResponse(transaction) {
      this.paymentMessage = 'Waiting for confirmation, do not close';
      await transaction.wait().then(async (receipt) => {
        this.paymentMessage = 'Validating payment';
        await this.validatePayment({orderId: this.orderId, transactionHash: receipt.transactionHash});
        this.paymentMessage = null;
        if (this.userOrderError?.validatePayment) {
          await this.send({
            message: this.userOrderError.validatePayment.message,
            type: 'bg-danger',
            icon: 'ni-alert-circle',
            persist: true
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
        await this.$wallet.provider.getTransaction(tx.hash).then(this.onTransactionResponse);
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
        return 'secondary';
      }
    },
    togglePlaceBidModal() {
      this.placeBidModal?.toggle();
    },
    formatDecimal(value, decimals) {
      if (value == null) {
        return '-'
      }
      return (value).toFixed(decimals)
    },
    formatPayout(value) {
      const payout = (Number(value) || 0)
      return `${payout > 0 ? '+' : ''}${payout.toFixed(2)} NMR`
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
            this.orderId = this.orderGetters.getId(this.orders?.data[0]);
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
    const {globals} = useGlobals();
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
      numeraiCorrChartData: computed(() => !numerai?.value?.modelInfo ? {} : numeraiGetters.getNumeraiCorrChartData(numerai.value)),
      numeraiCorrCorr60TcChartData: computed(() => !numerai?.value?.modelInfo ? {} : numeraiGetters.getNumeraiCorrCorr60TcChartData(numerai.value)),
      numeraiTcIcChartData: computed(() => !numerai?.value?.modelInfo ? {} : numeraiGetters.getNumeraiTcIcChartData(numerai.value)),
      numerai,
      numeraiLoading,
      globals,
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
