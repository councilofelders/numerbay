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
                <a v-if="Boolean(modelUrl)" :href="modelUrl" class="" target="_blank">{{ productName }}</a>
                <span v-else>{{ productName }}</span>
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
                  :title="`${productGetters.getQtyDelivered(product)} / ${productGetters.getQtySalesFiltered(product)} quantity delivered on time`"
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
                          <li v-if="socialDiscord"><a :href="socialDiscord" target="_blank"><span
                            :class="`ni-chat`"
                            class="ni icon"></span>Discord</a>
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
                v-if="Boolean(product)"
                v-show="Boolean(productGetters.getCategory(product).is_per_model)"
                :latest-ranks="latestRanks"
                :latest-reps="latestReps"
                :latest-returns="latestReturns"
                :nmr-staked="nmrStaked"
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
                      <NumeraiChart v-if="isSignalsTournament" :chartdata="signalsCorrChartData"
                                    class="numerai-chart"></NumeraiChart>
                      <NumeraiChart v-if="isSignalsTournament" :chartdata="signalsTcIcChartData"
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
                          v-for="(roundPerformance, j) in roundModelPerformancesTableData"
                          :key="j">
                          <th scope="row">{{ roundPerformance.roundNumber }}</th>
                          <td class="text-end"><span><span
                            class="tooltip-s1">{{ formatDecimal(Number(roundPerformance.atRisk), 2) }} NMR<span
                            class="tooltip-s1-text tooltip-text">{{
                              `${roundPerformance.atRisk} NMR`
                            }}</span></span></span></td>
                          <td class="text-end">
                            <span> {{ roundPerformance.corrMultiplier }}xCORR</span>
                            <span> {{ roundPerformance.tcMultiplier }}xTC</span>
                          </td>
                          <td class="text-end" v-if="isSignalsTournament"><span class="tooltip-s1">{{
                              formatDecimal(getRoundScore(roundPerformance, 'fnc_v4', false), 4)
                            }}<span
                              class="tooltip-s1-text tooltip-text">Percentile: {{
                                formatDecimal(getRoundScore(roundPerformance, 'fnc_v4', true) * 100, 1)
                              }}</span></span></td>
                          <td class="text-end" v-else><span class="tooltip-s1">{{
                              formatDecimal(getRoundScore(roundPerformance, 'v2_corr20', false), 4)
                            }}<span
                              class="tooltip-s1-text tooltip-text">Percentile: {{
                                formatDecimal(getRoundScore(roundPerformance, 'v2_corr20', true) * 100, 1)
                              }}</span></span></td>
                          <td class="text-end" v-if="isSignalsTournament"><span class="tooltip-s1">{{
                              formatDecimal(getRoundScore(roundPerformance, 'corr_v4', false), 4)
                            }}<span
                              class="tooltip-s1-text tooltip-text">Percentile: {{
                                formatDecimal(getRoundScore(roundPerformance, 'corr_v4', true) * 100, 1)
                              }}</span></span></td>
<!--                          <td class="text-end" v-if="isSignalsTournament"><span class="tooltip-s1">{{
                              formatDecimal(getRoundScore(roundPerformance, 'corr60', false), 4)
                            }}<span
                              class="tooltip-s1-text tooltip-text">Percentile: {{
                                formatDecimal(getRoundScore(roundPerformance, 'corr60', true) * 100, 1)
                              }}</span></span></td>
                          <td class="text-end" v-else><span class="tooltip-s1">{{
                              formatDecimal(getRoundScore(roundPerformance, 'corj60', false), 4)
                            }}<span
                              class="tooltip-s1-text tooltip-text">Percentile: {{
                                formatDecimal(getRoundScore(roundPerformance, 'corj60', true) * 100, 1)
                              }}</span></span></td>-->
                          <td class="text-end" v-if="isSignalsTournament"><span
                            class="tooltip-s1">{{ formatDecimal(getRoundScore(roundPerformance, 'ic_v2', false), 4) }}<span
                            class="tooltip-s1-text tooltip-text">Percentile: {{
                              formatDecimal(getRoundScore(roundPerformance, 'ic_v2', true) * 100, 1)
                            }}</span></span></td>
                          <td class="text-end" v-if="!isSignalsTournament"><span
                            class="tooltip-s1">{{ formatDecimal(getRoundScore(roundPerformance, 'fnc_v3', false), 4) }}<span
                            class="tooltip-s1-text tooltip-text">Percentile: {{
                              formatDecimal(getRoundScore(roundPerformance, 'fnc_v3', true) * 100, 1)
                            }}</span></span></td>
                          <td class="text-end"><span
                            class="tooltip-s1 text-primary">{{ formatDecimal(getRoundScore(roundPerformance, 'tc', false), 4) }}<span
                            class="tooltip-s1-text tooltip-text">Percentile: {{
                              formatDecimal(getRoundScore(roundPerformance, 'tc', true) * 100, 1)
                            }}</span></span></td>
                          <td class="text-end"><span class="tooltip-s1 text-primary"><span
                            :class="`text-${getMetricColor(Number(getRoundScore(roundPerformance, 'payout')) || 0)}`">{{
                              formatPayout(getRoundScore(roundPerformance, 'payout'))
                            }}</span><span
                            class="tooltip-s1-text tooltip-text">{{
                              `${getRoundScore(roundPerformance, 'payout')} NMR`
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
      <PlaceBidModal ref="placeBidModalWrapper" modalId="placeBidModal"
                     :productName="productName" :owner="owner" :product="product" :isAuthenticated="isAuthenticated"
                     :sellingRound="globals.selling_round" :paymentStep="paymentStep"
                     :toAddress="toAddress" :amount="amount" @onMetaMaskPayBtn="onMetaMaskPayBtn"
                     :numeraiLoading="numeraiLoading" :makeOrderLoading="makeOrderLoading" :numerai="numerai" :isAutoSubmitOptional="isAutoSubmitOptional"
                     @onDateChosen="onDateChosen" @onOptionChange="onOptionChange" @onQuantityChange="onQuantityChange"
                     @onApplyCoupon="onApplyCoupon" @onPlaceOrder="onPlaceOrder"></PlaceBidModal>
    </section><!-- end item-detail-section -->
    <!-- Related product -->
    <RelatedProducts v-if="Boolean(relatedProducts) && relatedProducts.length > 0" :products="relatedProducts"
                     title="Featured by seller"></RelatedProducts>
  </div><!-- end page-wrap -->
</template>

<script>
import _ from 'lodash';
import v2RoundModelPerformances from '~/apollo/queries/numerai/v2RoundModelPerformances'

// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

import ModelMetricsCard from "@/components/section/ModelMetricsCard";
import NumeraiChart from '@/components/section/NumeraiChart';
import RelatedProducts from "@/components/section/RelatedProducts";
import PlaceBidModal from "~/components/section/PlaceBidModal";

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
  userGetters,
  useUser,
  useUserOrder
} from '@vue-storefront/numerbay';
import {useUiNotification} from '~/composables';
import {ethers} from 'ethers';
import {contractAddress, transferAbi} from "../plugins/nmr";

export default {
  name: 'ProductDetails',
  components: {
    PlaceBidModal,
    ModelMetricsCard,
    NumeraiChart,
    RelatedProducts,
  },
  apollo: {
    v2RoundModelPerformances: {
      query: v2RoundModelPerformances,
      variables() {
        return {
          model_id: this.product?.model?.id,
          lastNRounds: 260,
          tournament: this.product?.model?.tournament
        }
      },
      skip () {
        return !this.product
      }
    }
  },
  data() {
    return {
      placeBidModal: null,

      paymentStep: 1,
      amount: 0,
      toAddress: '',
      orderId: null,


      metaMaskPayMsg: null,


      SectionData
    };
  },
  computed: {
    numeraiCorrCorr60TcChartData() {
      return !this.v2RoundModelPerformances? {} : numeraiGetters.getNumeraiCorrCorr60TcChartData(this.v2RoundModelPerformances)
    },
    signalsCorrChartData() {
      return !this.v2RoundModelPerformances? {} : numeraiGetters.getSignalsCorrChartData(this.v2RoundModelPerformances)
    },
    signalsTcIcChartData() {
      return !this.v2RoundModelPerformances? {} : numeraiGetters.getSignalsTcIcChartData(this.v2RoundModelPerformances)
    },
    roundModelPerformancesTableData() {
      return !this.v2RoundModelPerformances? {} : numeraiGetters.getRoundModelPerformancesTableData(this.v2RoundModelPerformances).slice(0, 12)
    },
    isSignalsTournament() {
      return this.productGetters.getCategory(this.product).tournament !== 8;
    },
    performanceTableHeaders() {
      return this.isSignalsTournament ? [
        {name: 'Round', description: null},
        {name: 'At-risk', description: 'The NMR at-risk for this model for this particular round. Equal to the model’s stake value minus any pending releases at round deadline.'},
        {name: 'Stake Type', description: null},
        {name: 'FNCV4', description: 'Correlation of users neutralized submissions with target_20d_factor_feat_neutral'},
        {name: 'CORRV4', description: 'Correlation of unneutralized submission with target_20d_factor_feat_neutral'},
        // {name: 'CORR60', description: 'Correlation of submission with the 60-day signals target'},
        {name: 'ICV2', description: 'Correlation of users unneutralized submissions with binned raw returns (target_20d_raw_return)'},
        {name: 'TC', description: 'How much this submission contributed to Meta Model performance'},
        {name: 'Payout', description: 'Latest projected payout'},
      ] : [
        {name: 'Round', description: null},
        {name: 'At-risk', description: 'The NMR at-risk for this model for this particular round. Equal to the model’s stake value minus any pending releases at round deadline.'},
        {name: 'Stake Type', description: null},
        {name: 'CORR20V2', description: 'Numerai correlation of submission with target cyrus_20'},
        // {name: 'CORJ60', description: 'Correlation of submission with target_jerome_v4_60'},
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
    owner() {
      return this.$route.params.owner || this.productGetters.getOwner(this.product);
    },
    socialDiscord() {
      return this.product?.owner?.social_discord;
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
      return Boolean(this.socialDiscord || this.socialLinkedIn || this.socialTwitter || this.socialWebsite);
    },
    isNumeraiChartReady() {
      return Boolean(this.v2RoundModelPerformances)
      // return !this.productLoading && !this.numeraiLoading && Boolean(this.productGetters.getCategory(this.product).is_per_model) && Boolean(this.numerai.modelInfo);
    },
    productName() {
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
      return this.product?.model?.latest_ranks;
    },
    latestReps() {
      return this.product?.model?.latest_reps;
    },
    latestReturns() {
      return {
        oneDay: this.$route.params.latestReturnOneDay || this.productGetters.getModelReturn(this.product, 'oneDay'),
        threeMonths: this.$route.params.latestReturnThreeMonths || this.productGetters.getModelReturn(this.product, 'threeMonths'),
        oneYear: this.$route.params.latestReturnOneYear || this.productGetters.getModelReturn(this.product, 'oneYear'),
        allTime: this.$route.params.latestReturnAllTime || this.productGetters.getModelReturn(this.product, 'allTime')
      };
    },

  },
  methods: {
    getRoundScore(roundPerformance, scoreName, isPercentile) {
      if (scoreName === 'payout') {
        return (roundPerformance?.submissionScores || []).filter(o=>(o.displayName==='tc'))[0]?.payoutPending
      }

      if (isPercentile) {
        return (roundPerformance?.submissionScores || []).filter(o=>(o.displayName===scoreName))[0]?.percentile
      }
      return (roundPerformance?.submissionScores || []).filter(o=>(o.displayName===scoreName))[0]?.value
    },
    async onDateChosen({selectedRounds, coupon}) {
      await this.search({
        id: this.id,
        categorySlug: this.category,
        name: this.name,
        rounds: selectedRounds.map(r=>r?.roundNumber),
        coupon: coupon
      });
    },
    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    async onOptionChange({selectedRounds, coupon}) {
      await this.search({
        id: this.id,
        categorySlug: this.category,
        name: this.name,
        rounds: selectedRounds.map(r=>r?.roundNumber),
        coupon: coupon
      });
    },
    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    async onQuantityChange({selectedRounds, coupon}) {
      await this.search({
        id: this.id,
        categorySlug: this.category,
        name: this.name,
        rounds: selectedRounds.map(r=>r?.roundNumber),
        coupon: coupon
      });
    },
    async onApplyCoupon({selectedRounds, coupon}) {
      await this.search({
        id: this.id,
        categorySlug: this.category,
        name: this.name,
        rounds: selectedRounds.map(r=>r?.roundNumber),
        coupon: coupon
      });
    },
    async onPlaceOrder({selectedOption, submitSlot, selectedRounds, coupon}) {
      const option = selectedOption;
      if (!this.productGetters.getOptionIsOnPlatform(option)) {
        // visit external listing
        window.open(option.third_party_url, '_blank');
        return;
      }

      const optionId = option.id;
      await this.make({
        id: this.productGetters.getId(this.product),
        optionId,
        submitModelId: submitSlot,
        // quantity: this.quantity,
        rounds: selectedRounds.map(r=>r?.roundNumber),
        coupon: coupon
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
      this.metaMaskPayMsg = 'Waiting for confirmation, do not close';
      await transaction.wait().then(async (receipt) => {
        this.metaMaskPayMsg = 'Validating payment';
        await this.validatePayment({orderId: this.orderId, transactionHash: receipt.transactionHash});
        this.metaMaskPayMsg = null;
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
    async onMetaMaskPayBtn() {
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

      this.metaMaskPayMsg = 'Waiting for payment approval';
      await contract.transfer(this.toAddress, numberOfTokens).then(async (tx) => {
        this.metaMaskPayMsg = 'Waiting for transaction response';
        await this.$wallet.provider.getTransaction(tx.hash).then(this.onTransactionResponse);
      }).catch(async (e) => {
        this.metaMaskPayMsg = null;
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
      this.$refs?.placeBidModalWrapper?.toggle();
      this.$refs?.placeBidModalWrapper?.onQuantityChange();
      // this.onQuantityChange({selectedRounds: [], coupon: null})
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
  mounted() {
    this.$nextTick(() => {
      const modal = this.$refs?.placeBidModalWrapper?.$refs?.placeBidModal?.$refs?.placeBidModal;

      modal?.addEventListener('show.bs.modal', async () => {
        // eslint-disable-next-line camelcase
        await this.orderSearch({
          role: 'buyer',
          filters: {
            product: {in: [this.productGetters.getId(this.product)]},
            // round_order: {in: [this.globals.selling_round]},
            state: {in: ['pending']}
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
              modal?.dispose();
              // this.placeBidModal?.dispose();
            } finally {
              await this.$router.push('/purchases');
            }
          }
        }
      }, false);

      modal?.addEventListener('shown.bs.modal', () => {
        // this.$refs.optionDropdown?.$refs?.search?.focus();
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
    });
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
    const {numerai, getModels, loading: numeraiLoading} = useNumerai(cacheKey);
    const {globals} = useGlobals();
    const {user, isAuthenticated, loading: userLoading} = useUser();
    const {order, make, loading: makeOrderLoading, error: makeOrderError} = useMakeOrder();
    const {orders, search: orderSearch, validatePayment, error: userOrderError} = useUserOrder('product');
    const {send} = useUiNotification();

    const product = computed(() => (products.value.data || [])[0]);

    onSSR(async () => {
      await search({id, categorySlug: category, name}).then(async () => {
        await searchRelatedProducts({filters: {id: {in: product?.value?.featured_products || []}}});
      });
    });

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
