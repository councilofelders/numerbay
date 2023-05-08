<template>
  <Modal :ref="modalId" :modal-id="modalId" @registeredModal="modal = $event">
    <template slot="title">{{ paymentStep === 1 ? `Place an Order` : `Payment` }}</template>
    <div v-if="paymentStep === 1">
      <p class="mb-3">You are about to buy <strong>{{ productName }}</strong> from <strong>{{ owner }}</strong></p>
      <ValidationObserver v-slot="{ handleSubmit }">
        <div class="mb-3">
          <label class="form-label">Select an option</label>
          <v-select v-if="Boolean(product)" ref="optionDropdown" v-model="optionIdx"
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
                            rules="required|integer|min_value:1|max_value:50" v-show="!showCalendar" slim>
          <div class="mb-3">
            <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label">Number of rounds (5 per week)</label>
            <input v-model="quantity" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                   max="50" min="1" step="1" type="number" @change="onQuantityChange">
            <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
          </div>
        </ValidationProvider>
        <div class="mb-3">
          <div class="d-flex align-items-center justify-content-between">
            <label class="form-label">Advanced (pick specific dates)</label>
            <div class="form-check form-switch form-switch-s1">
              <input v-model="showCalendar" class="form-check-input" type="checkbox">
            </div><!-- end form-check -->
          </div>
        </div>
        <div class="mb-3" v-show="showCalendar">
          <MultipleDatePicker @change="onDateChosen" :is-dark="isDark" :minDate="minDate" ref="calendar"></MultipleDatePicker>
        </div>
        <div v-if="isAuthenticated">
          <div v-if="!!product && isOnPlatform && productGetters.getCategory(product).is_submission"
               class="d-flex align-items-center justify-content-between">
            <label class="form-label" for="autoSubmit">Auto-submit to Numerai</label>
            <div class="form-check form-switch form-switch-s1">
              <input id="autoSubmit" v-model="autoSubmit" :disabled="!isAutoSubmitOptional" class="form-check-input" type="checkbox">
            </div><!-- end form-check -->
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
              numSelectedRounds
            }}</span></li>
          <li v-if="(!!product && productGetters.getCategory(product).is_per_round)"><span>Selected rounds</span> <span>{{
              selectedRoundNumbers
            }}</span></li>
          <li><span>You will pay</span> <span>{{ formattedTotalPrice }}</span></li>
        </ul>
        <div v-if="isAuthenticated">
          <div class="d-flex flex-wrap align-items-center justify-content-between mt-2">
            <div class="form-check">
              <input id="useCoupon" v-model="useCoupon" :disabled="Boolean(couponApplied)" class="form-check-input"
                     type="checkbox">
              <label class="form-check-label form-check-label-s1" for="useCoupon"> I have a coupon
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
                <button class="btn btn-dark" @click="onApplyCoupon">{{ couponApplied ? 'Remove' : 'Apply' }}</button>
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
          <div v-if="!!product && product.use_encryption"
               class="d-flex flex-wrap align-items-center justify-content-between mt-2 mb-4">
            <div class="alert alert-info d-flex mb-4" role="alert">
              <svg class="flex-shrink-0 me-3" fill="currentColor" height="30" viewBox="0 0 24 24" width="30">
                <path
                  d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"></path>
              </svg>
              <p class="fs-14">
                Upload is per-order for this product. You need to wait for upload even if a ready badge is shown.
              </p>
            </div><!-- end alert -->
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
        <a class="btn btn-light d-block" href="javascript:void(0);" @click="onMetaMaskPayBtn">Pay with MetaMask</a>
      </div>
      <div v-if="metaMaskPayMsg" class="mb-2">
        <span class="spinner-border spinner-border-sm text-primary me-2" role="status"></span>
        <span class="text-primary">{{ metaMaskPayMsg }}</span>
      </div>
    </div>
  </Modal><!-- end modal-->
</template>
<script>
import _ from 'lodash';

import MultipleDatePicker from "@/components/common/MultipleDatePicker";

// Composables
import {
  cartGetters,
  productGetters,
  userGetters,
} from '@vue-storefront/numerbay';

import moment from 'moment';

export default {
  name: 'PlaceBidModal',
  components: {
     MultipleDatePicker
  },
  props: {
    modalId: {
      type: String,
      default: 'placeBidModal'
    },
    isAuthenticated: {
      type: Boolean,
      default: false
    },
    sellingRound: {
      type: Number,
      default: null
    },
    paymentStep: {
      type: Number,
      default: 1
    },
    toAddress: {
      type: String,
      default: ''
    },
    amount: {
      type: Number,
      default: 0
    },
    metaMaskPayMsg: {
      type: String,
      default: null
    },
    isAutoSubmitOptional: {
      type: Boolean,
      default: true
    },
    numeraiLoading: {
      type: Boolean,
      default: true
    },
    makeOrderLoading: {
      type: Boolean,
      default: false
    },
    productName: {
      type: String,
      default: null
    },
    owner: {
      type: String,
      default: null
    },
    product: {
      type: Object,
      default: null
    },
    numerai: {
      type: Object,
      default: null
    },
  },
  data() {
    return {
      optionIdx: 0,
      quantity: 5,
      showCalendar: false,
      selectedRounds: [],
      autoSubmit: false,
      submitSlot: null,
      useCoupon: false,
      coupon: null,
      terms: false,
      modal: null
    };
  },
  computed: {
    selectedOption() {
      return this.productGetters.getOrderedOption(this.product, this.optionIdx);
    },
    isOnPlatform() {
      return this.productGetters.getOptionIsOnPlatform(this.selectedOption);
    },
    isDark() {
      if(process.client) {
        return localStorage.getItem('website_theme')==='dark-mode';
      }
    },
    minDate() {
      const currentDate = moment.utc()
      const dow = currentDate.day();
      let offset = 0;
      if (dow === 0) { // if Sunday
        offset = 1
      } else if (dow === 1) { // if Monday
        offset = 2
      }
      let minDate = currentDate.subtract(offset, "days")
      return minDate.format("DD/MM/YYYY")
    },
    numSelectedRounds() {
      return this.selectedRounds ? this.selectedRounds.length : 0
    },
    selectedRoundNumbers() {
      return (Boolean(this.selectedRounds) && this.selectedRounds.length > 0) ? this.selectedRounds.map(r=>r?.roundNumber).join(', ') : 'None'
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
    },
    buyBtnText() {
      return this.isOnPlatform ? 'Place an Order' : 'Visit external listing';
    },
  },
  methods: {
    toggle() {
      this.modal?.toggle();
    },

    dateToRound(date) {
      const ifThen = function (a, b, c) {
          return a === b ? c : a;
      };

      const startDate = new Date("2022-10-22T00:00:00.000Z");
      const baseRound = 339
      const endDate = date
      const elapsed = (endDate - startDate) / 86400000
      const daysBeforeFirstMonday = (8 - startDate.getDay()) % 7
      const daysAfterLastMonday = endDate.getDay()-1;
      return Math.ceil(baseRound + ((elapsed - (daysBeforeFirstMonday + daysAfterLastMonday)) / 7 * 5) + ifThen(daysBeforeFirstMonday - 1, -1, 0) + ifThen(daysAfterLastMonday, 6, 5) - 1)
    },

    // nextWeekendRoundNumber(currentRound) {
    //   return currentRound + 4 - currentRound % 5
    // },

    async onApplyCoupon() {
      const couponApplied = cartGetters.getAppliedCoupon(this.selectedOption)?.code;
      if (couponApplied) {
        this.coupon = null;
      }
      this.$emit('onApplyCoupon', {selectedRounds: this.selectedRounds, coupon: this.coupon})
    },

    async onMetaMaskPayBtn() {
      this.$emit('onMetaMaskPayBtn')
    },

    async onOptionChange() {
      this.$emit('onOptionChange', {selectedRounds: this.selectedRounds, coupon: this.coupon})
    },

    async onQuantityChange() {
      this.selectedRounds = Array.from({length: this.quantity}, (x, i) => ({"roundNumber": parseInt(this.sellingRound) + i}));
      this.$emit('onQuantityChange', {selectedRounds: this.selectedRounds, coupon: this.coupon})
    },

    onDateChosen: _.debounce(async function (calendarData) {
      const selectedDates = calendarData?.selectedDates;
      this.selectedRounds = selectedDates.map(dateJson => {
        const dateString = dateJson?.date;
        const dateParts = dateString.split("/");
        const dateObject = new Date(Date.UTC(+dateParts[2], dateParts[1] - 1, +dateParts[0]));
        const roundNumber = this.dateToRound(dateObject)
        return {date: dateObject, roundNumber: roundNumber}
      })
      this.$emit('onDateChosen', {selectedRounds: this.selectedRounds, coupon: this.coupon})
    }, 500),

    async onPlaceOrder() {
      this.$emit('onPlaceOrder', {
        selectedOption: this.selectedOption, submitSlot: this.submitSlot,
        selectedRounds: this.selectedRounds, coupon: this.coupon})
    },
  },
  watch: {
    async product() {
      if (Boolean(this.product) && !this.isAutoSubmitOptional) {
        this.autoSubmit = true;
      }
    },
    showCalendar(value) {
      if (value) { // clear quantity and enable calendar
        this.selectedRounds = []
        this.quantity = 5
      } else { // disable calendar and refresh quantity
        this.onQuantityChange()
      }
    }
  },
  beforeDestroy() {
    this.modal?.hide();
  },
  setup(props) {

    const onCopy = (e) => {
      const target = e.trigger.querySelector('.tooltip-text');
      const prevText = target.innerHTML;
      target.innerHTML = 'Copied';
      setTimeout(function () {
        target.innerHTML = prevText;
      }, 1000);
    };

    return {
      onCopy,
      productGetters,
      userGetters,
    };
  }
};
</script>

<style lang="css" scoped>
</style>
