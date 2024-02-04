<template>
  <Modal :modal-id="modalId" backdrop="static" modal-class="modal-lg" @registeredModal="modal = $event">
    <template slot="title">Update Option</template>
    <ValidationObserver key="options" v-slot="{ handleSubmit }">
      <div class="form-item mb-4">
        <div class="mb-4">
          <div class="d-flex align-items-center justify-content-between">
            <div class="me-2">
              <h5 class="mb-1">Sell on-platform</h5>
              <p class="form-text">Sell natively on NumerBay</p>
            </div>
            <div class="form-check form-switch form-switch-s1">
              <input v-model="isOnPlatform" class="form-check-input" type="checkbox"
                     @change="onPlatformChange(isOnPlatform)">
            </div><!-- end form-check -->
          </div><!-- end d-flex -->
        </div>
      </div><!-- end form-item -->
      <div v-if="isOnPlatform">
        <ValidationProvider key="onPlatformPrice" v-slot="{ errors }" rules="required|decimal|min_value:0" slim>
          <div class="form-item mb-4">
            <div class="mb-4">
              <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Total price</label>
              <input v-model="price" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                     min="0" placeholder="Total Price in NMR" type="number">
              <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
            </div>
          </div><!-- end form-item -->
        </ValidationProvider>
        <ValidationProvider key="onPlatformQuantity" v-slot="{ errors }" rules="required|integer|min_value:1" slim>
          <div class="form-item mb-4">
            <div class="mb-4">
              <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Bundled quantity (Number of rounds)</label>
              <input v-model="quantity" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                     min="1" placeholder="Quantity or number of rounds per unit" type="number">
              <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
            </div>
          </div><!-- end form-item -->
        </ValidationProvider>
      </div>
      <div v-else>
        <ValidationProvider key="offPlatformPrice" v-slot="{ errors }" rules="required|decimal|min_value:1" slim>
          <div class="form-item mb-4">
            <div class="mb-4">
              <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Total price</label>
              <input v-model="price" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                     min="1" placeholder="Price in USD equivalent" type="number">
              <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
            </div>
          </div><!-- end form-item -->
        </ValidationProvider>
        <ValidationProvider key="offPlatformQuantity" v-slot="{ errors }" rules="required|integer|min_value:1" slim>
          <div class="form-item mb-4">
            <div class="mb-4">
              <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Bundled quantity (Number of rounds)</label>
              <input v-model="quantity" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                     min="1" placeholder="Quantity or number of rounds per unit" type="number">
              <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
            </div>
          </div><!-- end form-item -->
        </ValidationProvider>
        <ValidationProvider v-slot="{ errors }" rules="url" slim>
          <div class="form-item mb-4">
            <div class="mb-4">
              <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label" for="thirdPartyUrl">Third-party
                listing URL</label>
              <input id="thirdPartyUrl" v-model="thirdPartyUrl" :class="!errors[0] ? '' : 'is-invalid'"
                     class="form-control form-control-s1" placeholder="e.g. Gumroad product link" type="text"
                     @change="encodeURL">
              <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
            </div>
          </div><!-- end form-item -->
        </ValidationProvider>
      </div>
      <div class="form-item mb-4">
        <div class="mb-4">
          <label class="mb-2 form-label">Option description</label>
          <input v-model="description" class="form-control form-control-s1" placeholder="Option description"
                 type="text">
        </div>
      </div><!-- end form-item -->
      <div v-if="isOnPlatform">
        <div class="form-item mb-4">
          <div class="mb-4">
            <div class="d-flex align-items-center justify-content-between">
              <div class="me-2">
                <h5 class="mb-1">Override default external wallet</h5>
<!--                <p class="form-text text-break">Receive payments with your Numerai wallet <a :href="`https://etherscan.io/address/${user.numerai_wallet_address}`"
                                                                                             class="link-secondary"
                                                                                             target="_blank">{{
                    user.numerai_wallet_address
                  }}</a>
                </p>-->
              </div>
              <div class="form-check form-switch form-switch-s1">
                <input v-model="overrideExternalWallet" class="form-check-input" type="checkbox">
              </div><!-- end form-check -->
            </div><!-- end d-flex -->
            <div v-if="overrideExternalWallet" class="mt-4">
              <label class="mb-2 form-label">External wallet for receiving payments</label>
              <input v-model="wallet"
                     class="form-control form-control-s1" placeholder="External wallet for receiving payments" type="text">
            </div>
          </div>
        </div><!-- end form-item -->
        <div class="form-item mb-4">
          <h5 class="mb-3">Select sale mode</h5>
          <ul id="myTab" class="row g-3 nav nav-tabs nav-tabs-s2" role="tablist">
            <li v-for="list in listingModes" :key="list.id" class="nav-item col-4 col-sm-4 col-lg-3 tooltip-s1"
                role="presentation">
              <button :id="list.value"
                      :class="[mode === list.value ? 'active':'', isListingModeDisabled(list.value) ? 'disabled':'']"
                      :disabled="isListingModeDisabled(list.value)" class="nav-link"
                      data-bs-toggle="tab" type="button" @click="mode = list.value">
                <span class="tooltip-s1-text tooltip-s1-text-lg tooltip-text">{{ list.description }}</span>
                <em :class="list.icon" class="ni nav-link-icon"></em>
                <span class="nav-link-title mt-1 d-block">{{ list.title }}</span>
              </button>
            </li>
          </ul>
        </div><!-- end form-item -->
        <ValidationProvider v-if="mode === 'stake_with_limit'" v-slot="{ errors }" rules="required|decimal|min_value:1"
                            slim>
          <div class="form-item mb-4">
            <div class="mb-4">
              <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Stake limit</label>
              <input v-model="stakeLimit" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                     min="1" placeholder="Stake limit in NMR" type="number">
              <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
            </div>
          </div><!-- end form-item -->
        </ValidationProvider>
        <div class="form-item mb-4">
          <div class="mb-4">
            <div class="d-flex align-items-center justify-content-between">
              <div class="me-2">
                <h5 class="mb-1">Reward coupons to buyers</h5>
              </div>
              <div class="form-check form-switch form-switch-s1">
                <input v-model="coupon" class="form-check-input" type="checkbox">
              </div><!-- end form-check -->
            </div><!-- end d-flex -->
            <div v-if="coupon">
              <ValidationProvider key="rewardMinSpend" v-slot="{ errors }" rules="decimal|min_value:0" slim>
                <div class="form-item mb-4">
                  <div class="mb-4">
                    <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Min spend for
                      reward</label>
                    <input v-model="couponSpecs.reward_min_spend" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                           min="0" placeholder="(Optional) Min Spend on This Product (in NMR) for Rewarding Coupon"
                           type="number">
                    <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                  </div>
                </div><!-- end form-item -->
              </ValidationProvider>
              <div class="form-item mb-4">
                <label class="mb-2 form-label">Applicable products</label>
                <client-only>
                  <multiselect ref="couponMultiSelect" v-model="couponSpecs.applicable_products"
                               :close-on-select="false" :group-select="true"
                               :multiple="true" :options="groupedProducts" class="coupon-multiselect"
                               group-label="category" group-values="products" label="sku" placeholder="Applicable Products (in Addition to This Product)"
                               track-by="id"
                  >
                    <template slot="option" slot-scope="props">
                      <span>{{ props.option.$isLabel ? props.option.$groupLabel : props.option.name }}</span>
                    </template>
                  </multiselect>
                </client-only>
              </div>
              <ValidationProvider key="discountPercent" v-slot="{ errors }"
                                  rules="required|integer|min_value:1|max_value:100" slim>
                <div class="form-item mb-4">
                  <div class="mb-4">
                    <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Discount %</label>
                    <input v-model="couponSpecs.discount_percent" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                           min="1" placeholder="Coupon Discount % (0-100, 100 being free)"
                           type="number">
                    <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                  </div>
                </div><!-- end form-item -->
              </ValidationProvider>
              <ValidationProvider key="maxDiscount" v-slot="{ errors }" rules="required|decimal|min_value:0" slim>
                <div class="form-item mb-4">
                  <div class="mb-4">
                    <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Max discount per order (in NMR)</label>
                    <input v-model="couponSpecs.max_discount" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                           min="0" placeholder="Coupon Max Discount (in NMR)" type="number">
                    <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                  </div>
                </div><!-- end form-item -->
              </ValidationProvider>
              <div v-if="couponSpecs.max_discount && couponSpecs.max_discount > 10" class="alert alert-warning d-flex mb-4" role="alert">
                <svg class="flex-shrink-0 me-3" fill="currentColor" height="30" viewBox="0 0 24 24" width="30">
                  <path
                    d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"></path>
                </svg>
                <p class="fs-14">
                  Be sure to set a reasonable max discount (applied per order) to avoid unintended exploitation.
                </p>
              </div><!-- end alert -->
              <ValidationProvider key="minSpend" v-slot="{ errors }" rules="decimal|min_value:0" slim>
                <div class="form-item mb-4">
                  <div class="mb-4">
                    <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Min spend for
                      redemption</label>
                    <input v-model="couponSpecs.min_spend" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                           min="0" placeholder="(Optional) Min Spend (in NMR) for Redeeming Coupon"
                           type="number">
                    <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                  </div>
                </div><!-- end form-item -->
              </ValidationProvider>
            </div>
          </div>
        </div><!-- end form-item -->
      </div>
      <button class="btn btn-dark" type="button" @click="handleSubmit(saveOption)">Save</button>
    </ValidationObserver>
  </Modal>
</template>

<script>
// Composables
import {extend} from 'vee-validate';

extend('decimal', {
  validate: (value, {decimals = '*', separator = '.'} = {}) => {
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

export default {
  name: 'PricingOptionModal',
  props: {
    modalId: {
      type: String,
      default: 'pricingOptionModal'
    },
    isModalOpen: {
      default: false
    },
    options: {
      type: Array,
      default: () => ([])
    },
    groupedProducts: {
      type: Array,
      default: () => ([])
    },
    isTournamentCategory: {
      type: Boolean,
      default: false
    },
    isSubmissionCategory: {
      type: Boolean,
      default: false
    },
    isPerRoundCategory: {
      type: Boolean,
      default: false
    },
    user: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      modal: null,
      listingModes: [
        {
          id: 1,
          title: 'Distribute File',
          description: 'Buyers can download files and optionally designate a submission slot',
          value: 'file',
          icon: 'ni-files'
        },
        {
          id: 2,
          title: 'Stake Only',
          description: 'Submit for buyers without distributing files',
          value: 'stake',
          icon: 'ni-lock'
        },
        {
          id: 3,
          title: 'Stake with Limit',
          description: 'Submit for buyers without distributing files, with a NMR stake limit',
          value: 'stake_with_limit',
          icon: 'ni-lock-alt'
        }
      ],
      editOption: false,
      editedOption: -1,
      id: null,
      isOnPlatform: true,
      currency: 'NMR',
      overrideExternalWallet: false,
      mode: 'file',
      stakeLimit: null,
      quantity: 1,
      price: null,
      wallet: null,
      thirdPartyUrl: null,
      description: null,
      coupon: false,
      couponSpecs: {}
    };
  },
  methods: {
    show() {
      this.modal?.show();
    },
    hide() {
      this.modal?.hide();
    },
    resetData() {
      const initialData = {
        editOption: false,
        editedOption: -1,
        id: null,
        isOnPlatform: true,
        currency: 'NMR',
        overrideExternalWallet: false,
        mode: 'file',
        stakeLimit: null,
        quantity: 1,
        price: null,
        wallet: null,
        thirdPartyUrl: null,
        description: null,
        coupon: false
      };
      Object.keys(initialData).forEach(k => this[k] = initialData[k]);
    },
    encodeURL() {
      if (this.thirdPartyUrl) {
        this.thirdPartyUrl = encodeURI(decodeURI(this.thirdPartyUrl));
      }
    },
    onPlatformChange(isOnPlatform) {
      const index = this.editedOption;
      const option = index > -1 ? this.options[index] : null;

      if (isOnPlatform) {
        this.currency = 'NMR';
        this.wallet = index > -1 ? option.wallet : null;
        this.mode = index > -1 ? (option.mode || 'file') : 'file';
        this.stakeLimit = index > -1 ? option.stake_limit : null;
      } else {
        this.currency = 'USD';
        this.wallet = null;
        this.mode = null;
        this.stakeLimit = null;
      }
    },
    isListingModeDisabled(mode) {
      return !this.isSubmissionCategory && mode !== 'file';
    },
    changeOption(index) {
      this.resetData();
      if (index > -1) {
        const option = this.options[index];
        this.id = option.id;
        this.isOnPlatform = Boolean(option.is_on_platform);
        this.currency = option.currency;
        this.mode = option.mode;
        this.stakeLimit = option.stake_limit;
        this.quantity = option.quantity;
        this.price = option.price;
        this.wallet = option.wallet;
        this.thirdPartyUrl = option.third_party_url;
        this.description = option.description;
        this.editedOption = index;
        this.coupon = option.coupon ? option.coupon : false;
        this.couponSpecs = {
          // eslint-disable-next-line camelcase
          applicable_products: option.coupon_specs?.applicable_product_ids ? option.coupon_specs.applicable_product_ids.map(id => this.groupedProducts.map(gp => gp.products).flat().find((p) => parseInt(p.id) === parseInt(String(id)))) : [],
          // eslint-disable-next-line camelcase
          discount_percent: option.coupon_specs?.discount_percent,
          // eslint-disable-next-line camelcase
          max_discount: option.coupon_specs?.max_discount,
          // eslint-disable-next-line camelcase
          min_spend: option.coupon_specs?.min_spend,
          // eslint-disable-next-line camelcase
          reward_min_spend: option.coupon_specs?.reward_min_spend
        };
      } else if (!this.isTournamentCategory) {
        this.isOnPlatform = false;
        this.currency = 'USD';
        this.wallet = null;
        this.mode = null;
        this.stakeLimit = null;
      }
      if (!this.isPerRoundCategory) {
        this.quantity = 1;
      }
      this.editOption = true;
      this.$emit('change-option', index);
    },
    saveOption() {
      const options = this.options;
      const index = this.editedOption;
      const pricing = {
        id: index > -1 ? this.id : null,
        // eslint-disable-next-line camelcase
        is_on_platform: Boolean(this.isOnPlatform),
        currency: this.currency,
        mode: this.mode,
        // eslint-disable-next-line camelcase
        stake_limit: Number(this.stakeLimit),
        quantity: parseInt(this.quantity),
        price: Number(this.price),
        wallet: this.wallet,
        // eslint-disable-next-line camelcase
        third_party_url: this.thirdPartyUrl,
        description: this.description,
        coupon: this.coupon ? this.coupon : false,
        // eslint-disable-next-line camelcase
        coupon_specs: this.coupon ? {
          // eslint-disable-next-line camelcase
          applicable_product_ids: this.couponSpecs.applicable_products ? this.couponSpecs.applicable_products.map(p => p.id) : [],
          // eslint-disable-next-line camelcase
          discount_percent: this.couponSpecs.discount_percent,
          // eslint-disable-next-line camelcase
          max_discount: this.couponSpecs.max_discount,
          // eslint-disable-next-line camelcase
          min_spend: this.couponSpecs.min_spend,
          // eslint-disable-next-line camelcase
          reward_min_spend: this.couponSpecs.reward_min_spend
        } : null
      };
      if (index > -1) {
        options[index] = pricing;
        this.editedOption = -1;
      } else {
        options.push(pricing);
      }
      this.$forceUpdate();
      this.editOption = false;
      this.$emit('update:pricing', options);
      this.hide();
    }
  },
  beforeDestroy() {
    this.modal?.hide();
  }
};
</script>

<style lang="scss" scoped>
.coupon-multiselect::v-deep {
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
</style>
