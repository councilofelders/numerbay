<template>
  <Modal :modal-id="modalId" @registeredModal="modal = $event" backdrop="static" modal-class="modal-lg">
    <template slot="title">Update Option</template>
    <ValidationObserver v-slot="{ handleSubmit }" key="options">
    <div class="form-item mb-4">
        <div class="mb-4">
            <label class="mb-2 form-label">Option description</label>
            <input type="text" class="form-control form-control-s1" placeholder="Option description" v-model="description">
        </div>
    </div><!-- end form-item -->
    <div class="form-item mb-4">
        <div class="mb-4">
            <div class="d-flex align-items-center justify-content-between">
                <div class="me-2">
                    <h5 class="mb-1">Sell on-platform</h5>
                    <p class="form-text">Sell natively on NumerBay</p>
                </div>
                <div class="form-check form-switch form-switch-s1">
                    <input class="form-check-input" type="checkbox" v-model="isOnPlatform" @change="onPlatformChange(isOnPlatform)">
                </div><!-- end form-check -->
            </div><!-- end d-flex -->
        </div>
    </div><!-- end form-item -->
    <div v-if="isOnPlatform">
      <div class="form-item mb-4">
          <div class="mb-4">
              <div class="d-flex align-items-center justify-content-between">
                  <div class="me-2">
                      <h5 class="mb-1">Use Numerai wallet</h5>
                    <p class="form-text text-break">Receive payments with your Numerai wallet <a class="link-secondary" :href="`https://etherscan.io/address/${user.numerai_wallet_address}`" target="_blank">{{ user.numerai_wallet_address}}</a></p>
                  </div>
                  <div class="form-check form-switch form-switch-s1">
                      <input class="form-check-input" type="checkbox" v-model="useNumeraiWallet">
                  </div><!-- end form-check -->
              </div><!-- end d-flex -->
              <div class="mt-4">
                  <input type="text" class="form-control form-control-s1" placeholder="Alternative wallet for receiving payments" v-if="!useNumeraiWallet" v-model="wallet">
              </div>
          </div>
      </div><!-- end form-item -->
      <div class="form-item mb-4">
          <h5 class="mb-3">Select mode</h5>
          <ul class="row g-3 nav nav-tabs nav-tabs-s2" id="myTab" role="tablist">
              <li class="nav-item col-4 col-sm-4 col-lg-3 tooltip-s1" role="presentation" v-for="list in listingModes" :key="list.id">
                  <button class="nav-link" :class="mode === list.value ? 'active':''" :id="list.value" data-bs-toggle="tab" type="button" @click="mode = list.value">
                      <span class="tooltip-s1-text tooltip-s1-text-lg tooltip-text">{{ list.description }}</span>
                      <em class="ni nav-link-icon" :class="list.icon"></em>
                      <span class="nav-link-title mt-1 d-block">{{ list.title }}</span>
                  </button>
              </li>
          </ul>
      </div><!-- end form-item -->
      <ValidationProvider rules="required|decimal|min_value:1"  v-slot="{ errors }" v-if="mode === 'stake_with_limit'" slim>
      <div class="form-item mb-4">
          <div class="mb-4">
              <label class="mb-2 form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Stake limit</label>
              <input type="number" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="Stake limit in NMR" min="1" v-model="stakeLimit">
              <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
          </div>
      </div><!-- end form-item -->
      </ValidationProvider>
      <ValidationProvider rules="required|integer|min_value:1" v-slot="{ errors }" key="onPlatformQuantity" slim>
      <div class="form-item mb-4">
          <div class="mb-4">
              <label class="mb-2 form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Bundled quantity</label>
              <input type="number" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="Quantity or number of rounds per unit" min="1" v-model="quantity">
              <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
          </div>
      </div><!-- end form-item -->
      </ValidationProvider>
      <ValidationProvider rules="required|decimal|min_value:1" v-slot="{ errors }" key="onPlatformPrice" slim>
      <div class="form-item mb-4">
          <div class="mb-4">
              <label class="mb-2 form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Total price</label>
              <input type="number" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="Total Price in NMR" min="1" v-model="price">
              <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
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
                      <input class="form-check-input" type="checkbox" v-model="coupon">
                  </div><!-- end form-check -->
              </div><!-- end d-flex -->
              <div v-if="coupon">
                <ValidationProvider rules="decimal|min_value:0" v-slot="{ errors }" key="rewardMinSpend" slim>
                <div class="form-item mb-4">
                    <div class="mb-4">
                        <label class="mb-2 form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Min spend for reward</label>
                        <input type="number" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="(Optional) Min Spend on This Product (in NMR) for Rewarding Coupon" min="0" v-model="couponSpecs.reward_min_spend">
                        <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                    </div>
                </div><!-- end form-item -->
                </ValidationProvider>
                <div class="form-item mb-4">
                  <label class="mb-2 form-label">Applicable products</label>
                  <client-only>
                    <multiselect ref="couponMultiSelect" placeholder="Applicable Products (in Addition to This Product)" v-model="couponSpecs.applicable_products" class="coupon-multiselect"
                         :options="groupedProducts" :multiple="true" :close-on-select="false" group-values="products" group-label="category" :group-select="true" track-by="id" label="sku"
                    >
                      <template slot="option" slot-scope="props">
                        <span>{{ props.option.$isLabel ? props.option.$groupLabel : props.option.name }}</span>
                      </template>
                    </multiselect>
                  </client-only>
                </div>
                <ValidationProvider rules="required|integer|min_value:1|max_value:100" v-slot="{ errors }" key="discountPercent" slim>
                <div class="form-item mb-4">
                    <div class="mb-4">
                        <label class="mb-2 form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Discount %</label>
                        <input type="number" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="Coupon Discount % (0-100, 100 being free)" min="1" v-model="couponSpecs.discount_percent">
                        <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                    </div>
                </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider rules="required|decimal|min_value:0" v-slot="{ errors }" key="maxDiscount" slim>
                <div class="form-item mb-4">
                    <div class="mb-4">
                        <label class="mb-2 form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Max discount</label>
                        <input type="number" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="Coupon Max Discount (in NMR)" min="0" v-model="couponSpecs.max_discount">
                        <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                    </div>
                </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider rules="decimal|min_value:0" v-slot="{ errors }" key="minSpend" slim>
                <div class="form-item mb-4">
                    <div class="mb-4">
                        <label class="mb-2 form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Min spend for redemption</label>
                        <input type="number" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="(Optional) Min Spend (in NMR) for Redeeming Coupon" min="0" v-model="couponSpecs.min_spend">
                        <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                    </div>
                </div><!-- end form-item -->
                </ValidationProvider>
              </div>
          </div>
      </div><!-- end form-item -->
    </div>
    <div v-else>
      <ValidationProvider rules="required|integer|min_value:1" v-slot="{ errors }" key="offPlatformQuantity" slim>
      <div class="form-item mb-4">
          <div class="mb-4">
              <label class="mb-2 form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Bundled quantity</label>
              <input type="number" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="Quantity or number of rounds per unit" min="1" v-model="quantity">
              <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
          </div>
      </div><!-- end form-item -->
      </ValidationProvider>
      <ValidationProvider rules="required|decimal|min_value:1" v-slot="{ errors }" key="offPlatformPrice" slim>
      <div class="form-item mb-4">
          <div class="mb-4">
              <label class="mb-2 form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Total price</label>
              <input type="number" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="Price in USD equivalent" min="1" v-model="price">
              <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
          </div>
      </div><!-- end form-item -->
      </ValidationProvider>
      <ValidationProvider rules="url" v-slot="{ errors }" slim>
      <div class="form-item mb-4">
          <div class="mb-4">
              <label class="mb-2 form-label" :class="{ 'text-danger': Boolean(errors[0]) }" for="thirdPartyUrl">Third-party listing URL</label>
              <input type="text" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'" placeholder="e.g. Gumroad product link" id="thirdPartyUrl" v-model="thirdPartyUrl" @change="encodeURL">
              <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
          </div>
      </div><!-- end form-item -->
      </ValidationProvider>
    </div>
    <button class="btn btn-dark" type="button" @click="handleSubmit(saveOption)">Save</button>
    </ValidationObserver>
  </Modal>
</template>

<script>
// Composables
import { orderGetters, productGetters } from '@vue-storefront/numerbay';
import { extend } from 'vee-validate';
import _ from 'lodash';

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
      useNumeraiWallet: true,
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
        useNumeraiWallet: true,
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
          applicable_products: option.coupon_specs?.applicable_product_ids ? option.coupon_specs.applicable_product_ids.map(id => this.groupedProducts.map(gp=>gp.products).flat().find((p)=>parseInt(p.id) === parseInt(String(id)))) : [],
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
        coupon_specs: {
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
        }
      };
      if (index > -1) {
        console.log('pricing', pricing);
        console.log('options before', options);

        options[index] = pricing;
        console.log('options after', options);
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
  // mounted() {
  //
  //   /* ============= Custom Tooltips =============== */
  //   function customTooltip(selector, active) {
  //     const elem = document.querySelectorAll(selector);
  //     if (elem.length > 0) {
  //       elem.forEach(item => {
  //         const parent = item.parentElement;
  //         const next = item.nextElementSibling;
  //         createPopper(item, next);
  //         parent.addEventListener('mouseenter', function() {
  //           parent.classList.add(active);
  //         });
  //         parent.addEventListener('mouseleave', function() {
  //           parent.classList.remove(active);
  //         });
  //       });
  //     }
  //   }
  //
  //   customTooltip('.custom-tooltip', 'active');
  // },
  beforeDestroy() {
    this.modal?.hide();
  },
  setup() {

    return {
      orderGetters,
      productGetters
    };
  }
};
</script>

<style lang="scss" scoped>
.coupon-multiselect::v-deep {
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
</style>
