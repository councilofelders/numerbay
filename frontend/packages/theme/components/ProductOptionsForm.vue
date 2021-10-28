<template>
  <div class="sf-pricing-details">
    <transition :name="transition">
      <SfTabs
        v-if="editOption"
        key="edit-option"
        :open-tab="1"
        class="tab-orphan"
        data-testid="pricing-details-tabs"
      >
        <SfTab :title="changeOptionTabTitle">
          <slot name="change-option-description">
            <p class="message">
              {{ changeOptionDescription }}
            </p>
          </slot>
          <div class="form">
            <slot name="form">
              <ValidationObserver v-slot="{ handleSubmit }" key="options">
                <form @submit.prevent="handleSubmit(updateOption)">
                  <div class="form__radio-group">
                    <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                      <SfRadio
                        name="isOnPlatform"
                        value="true"
                        label="On-Platform"
                        details="Sell natively on NumerBay for cryptocurrency"
                        description="Payments are directly sent to you from buyers. You can manage buyers and automate file distribution."
                        v-model="isOnPlatform"
                        @change="onPlatformChange(isOnPlatform)"
                        :disabled="!!category && !isTournamentCategory"
                        class="form__radio"
                      />
                      <SfRadio
                        name="isOnPlatform"
                        value="false"
                        label="Off-Platform"
                        details="Link to 3rd-party platforms"
                        description="Off-Platform reference only. Self-managed."
                        v-model="isOnPlatform"
                        @change="onPlatformChange(isOnPlatform)"
                        class="form__radio"
                      />
                    </ValidationProvider>
                  </div>
                  <div v-if="isOnPlatform === 'true'">
                    <div class="form__radio-group">
                      <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                        <SfRadio
                          name="currency"
                          value="NMR"
                          label="NMR"
                          :details="`Payments go to your Numerai wallet ${user.numerai_wallet_address} by default`"
                          description="Alternatively, specify a compatible wallet below"
                          v-model="currency"
                          class="form__radio"
                        >
                          <template #label>
                            NMR  <SfBadge class="color-primary sf-badge flag">Gas-Free</SfBadge>
                          </template>
                        </SfRadio>
                        <SfRadio
                          name="currency"
                          value="DAI"
                          label="DAI"
                          details="On Polygon"
                          description="[Coming Soon]"
                          disabled
                          class="form__radio"
                        />
                        <!--<SfRadio
                          name="isOnPlatform"
                          value="USDC"
                          label="USDC"
                          v-model="form.currency"
                          class="form__radio"
                        />
                        <SfRadio
                          name="isOnPlatform"
                          value="ETH"
                          label="ETH"
                          v-model="form.currency"
                          class="form__radio"
                        />-->
                      </ValidationProvider>
                    </div>
                    <ValidationProvider v-slot="{ errors }">
                      <SfInput
                        v-e2e="'listing-modal-price'"
                        v-model="wallet"
                        :valid="!errors[0]"
                        :errorMessage="errors[0]"
                        name="price"
                        :label="`(Optional) Alternative Wallet for Receiving Payments`"
                        class="form__element"
                      />
                    </ValidationProvider>
                    <div class="form__radio-group">
                      <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                        <SfRadio
                          name="mode"
                          value="file"
                          label="Distribute File"
                          details="Buyers can download artifact files and optionally designate a model slot for submission"
                          description="You can upload artifacts to NumerBay or add external file URLs"
                          v-model="mode"
                          class="form__radio"
                        />
                        <SfRadio
                          name="mode"
                          value="stake"
                          label="Stake Only"
                          details="Submit for buyers automatically without distributing artifact files, without stake limit"
                          description="You must upload artifacts to NumerBay"
                          v-model="mode"
                          class="form__radio"
                          :disabled="!isSubmissionCategory"
                        />
                        <SfRadio
                          name="mode"
                          value="stake_with_limit"
                          label="Stake Only with Limit"
                          details="Submit for buyers automatically without distributing artifact files, with a stake limit (in NMR)"
                          description="You must upload artifacts to NumerBay"
                          v-model="mode"
                          class="form__radio"
                          :disabled="!isSubmissionCategory"
                        />
                      </ValidationProvider>
                    </div>
                    <div v-if="mode === 'stake_with_limit'">
                      <ValidationProvider rules="required|decimal|min_value:1"  v-slot="{ errors }">
                        <SfInput
                          v-model="stakeLimit"
                          :valid="!errors[0]"
                          :errorMessage="errors[0]"
                          name="price"
                          label="Stake Limit for Buyers (in NMR)"
                          type="number"
                          step=0.0001
                          min=1
                          class="form__element"
                        />
                      </ValidationProvider>
                    </div>
                    <div v-if="isPerRoundCategory">
                      Quantity (Number of Rounds)
                      <SfQuantitySelector
                        v-model="quantity"
                        aria-label="Quantity (Number of Rounds)"
                        class="sf-add-to-cart__select-quantity"
                      />
                    </div>
                    <ValidationProvider rules="required|decimal|min_value:1" v-slot="{ errors }">
                      <SfInput
                        v-e2e="'listing-modal-price'"
                        v-model="price"
                        :valid="!errors[0]"
                        :errorMessage="errors[0]"
                        name="price"
                        :label="`Price (per round equivalent, in ${currency})`"
                        type="number"
                        step=0.0001
                        min=1
                        class="form__element"
                      />
                    </ValidationProvider>
                  </div>
                  <div v-else>
                    <div v-if="isPerRoundCategory">
                      Quantity (Number of Rounds)
                      <SfQuantitySelector
                        v-model="quantity"
                        aria-label="Quantity (Number of Rounds)"
                        class="sf-add-to-cart__select-quantity"
                      />
                    </div>
                    <ValidationProvider rules="required|decimal|min_value:0" v-slot="{ errors }">
                      <SfInput
                        v-e2e="'listing-modal-price'"
                        v-model="price"
                        :valid="!errors[0]"
                        :errorMessage="errors[0]"
                        name="price"
                        label="Price (per round equivalent, in $USD)"
                        type="number"
                        step=0.01
                        min=0
                        class="form__element"
                      />
                    </ValidationProvider>
                    <ValidationProvider rules="url" v-slot="{ errors }">
                      <SfInput
                        v-e2e="'listing-modal-thirdPartyUrl'"
                        v-model="thirdPartyUrl"
                        :valid="!errors[0]"
                        :errorMessage="errors[0]"
                        name="thirdPartyUrl"
                        label="Third Party Listing URL (e.g. Gumroad product link)"
                        type="url"
                        class="form__element"
                        @change="encodeURL"
                      />
                    </ValidationProvider>
                  </div>
                  <ValidationProvider v-slot="{ errors }">
                    <SfInput
                      v-model="description"
                      :valid="!errors[0]"
                      :errorMessage="errors[0]"
                      name="price"
                      label="Pricing Option Description"
                      class="form__element"
                    />
                  </ValidationProvider>
                  <div style="display: flex">
                    <SfButton
                      v-if="updateOptionButtonText"
                      class="action-button"
                      data-testid="update-option-button"
                    >
                      {{ updateOptionButtonText }}</SfButton
                    >
                    <SfButton
                      v-if="cancelButtonText"
                      class="action-button color-secondary cancel-button"
                      data-testid="update-option-button"
                      @click="cancelEditing"
                      type="button"
                    >
                      {{ cancelButtonText }}</SfButton
                    >
                  </div>
                </form>
              </ValidationObserver>
            </slot>
          </div>
        </SfTab>
      </SfTabs>
      <SfTabs v-else key="option-list" :open-tab="1" class="tab-orphan">
        <SfTab :title="optionsTabTitle">
          <slot name="pricing-tab-description">
            <p class="message">
              {{ optionsTabDescription }}
            </p>
          </slot>
          <transition-group tag="div" :name="transition" class="pricing-list">
            <slot name="pricing-list">
              <div
                v-for="option in orderedOptions"
                :key="option.key"
                class="pricing"
                data-testid="pricing-option-list-item"
              >
                <div class="pricing__content" v-if="option.is_on_platform">
                  <b>On-Platform</b>
                  <SfProperty
                    name="Price"
                    :value="orderGetters.getFormattedPrice(option, withCurrency=true, decimals=4)"
                    class="sf-property property"
                  />
                  <SfProperty
                    name="Quantity (Number of Rounds)"
                    :value="option.quantity"
                    class="sf-property property"
                  />
                  <SfProperty
                    name="Mode"
                    :value="(option.mode || '').toUpperCase()"
                    class="sf-property property"
                  />
                  <SfProperty
                    name="Stake Limit"
                    :value="orderGetters.getStakeLimit(option)"
                    class="sf-property property"
                    v-if="option.mode === 'stake_with_limit'"
                  />
                  <SfProperty
                    name="Wallet"
                    :value="option.wallet || 'Numerai wallet'"
                    class="sf-property property"
                  />
                  <SfProperty
                    name="Description"
                    :value="option.description"
                    class="sf-property property"
                  />
                </div>
                <div class="pricing__content" v-else>
                  <b>Off-Platform</b>
                  <SfProperty
                    name="Price"
                    :value="orderGetters.getFormattedPrice(option, withCurrency=true, decimals=2)"
                    class="sf-property property"
                  />
                  <SfProperty
                    name="Quantity (Number of Rounds)"
                    :value="option.quantity"
                    class="sf-property property"
                  />
                  <SfProperty
                    name="URL"
                    :value="option.third_party_url"
                    class="sf-property property"
                  />
                  <SfProperty
                    name="Description"
                    :value="option.description"
                    class="sf-property property"
                  />
                </div>
                <div class="pricing__actions">
                  <SfIcon
                    icon="cross"
                    color="gray"
                    size="14px"
                    role="button"
                    class="smartphone-only"
                    @click="deleteOption(option.key)"
                    type="button"
                  />
                  <SfButton
                    v-if="changeButtonText"
                    data-testid="change-option"
                    @click="changeOption(option.key)"
                    type="button"
                  >
                    {{ changeButtonText }}
                  </SfButton>
                  <SfButton
                    v-if="deleteButtonText"
                    class="pricing__button-delete desktop-only"
                    data-testid="delete-option"
                    @click="deleteOption(option.key)"
                    type="button"
                  >
                    {{ deleteButtonText }}
                  </SfButton>
                </div>
              </div>
            </slot>
          </transition-group>
          <SfButton
            v-if="addNewOptionButtonText"
            class="action-button"
            data-testid="add-new-option"
            @click="changeOption(-1)"
            type="button"
          >
            {{ addNewOptionButtonText }}</SfButton
          >
        </SfTab>
      </SfTabs>
    </transition>
  </div>
</template>
<script>
import {
  SfTabs,
  SfInput,
  SfButton,
  SfIcon,
  SfRadio,
  SfBadge,
  SfProperty
} from '@storefront-ui/vue';
import SfQuantitySelector from '~/components/Molecules/SfQuantitySelector';
import { orderGetters } from '@vue-storefront/numerbay';
import _ from 'lodash';
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
// eslint-disable-next-line camelcase
import { required, min_value, integer } from 'vee-validate/dist/rules';

extend('required', {
  ...required,
  message: 'This field is required'
});

extend('min_value', {
  // eslint-disable-next-line camelcase
  ...min_value,
  message: 'This must be greater than 1'
});

extend('integer', {
  ...integer,
  message: 'This field must be an integer'
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

export default {
  name: 'ProductOptionsForm',
  components: {
    SfTabs,
    SfInput,
    SfButton,
    SfIcon,
    SfRadio,
    SfBadge,
    SfQuantitySelector,
    SfProperty,
    ValidationProvider,
    ValidationObserver
  },
  props: {
    optionsTabTitle: {
      type: String,
      default: 'Pricing options'
    },
    changeOptionTabTitle: {
      type: String,
      default: 'Change the option'
    },
    category: {
      type: String,
      default: null
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
    },
    options: {
      type: Array,
      default: () => ([])
    },
    transition: {
      type: String,
      default: 'sf-fade'
    },
    changeOptionDescription: {
      type: String,
      default: ''
    },
    changeButtonText: {
      type: String,
      default: 'Change'
    },
    deleteButtonText: {
      type: String,
      default: 'Delete'
    },
    addNewOptionButtonText: {
      type: String,
      default: 'Add new option'
    },
    updateOptionButtonText: {
      type: String,
      default: 'Update option'
    },
    cancelButtonText: {
      type: String,
      default: 'Cancel'
    },
    inputsLabels: {
      type: Array,
      default: () => [
        'First Name',
        'Last Name',
        'Street Name',
        'House/Apartment number',
        'City',
        'State/Province',
        'Zip-Code',
        'Phone number'
      ]
    },
    selectLabel: {
      type: String,
      default: 'Country'
    },
    optionsTabDescription: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      editOption: false,
      editedOption: -1,
      id: null,
      isOnPlatform: 'true',
      currency: 'NMR',
      mode: 'file',
      stakeLimit: null,
      quantity: 1,
      price: null,
      wallet: null,
      thirdPartyUrl: null,
      description: null
    };
  },
  computed: {
    orderedOptions() {
      if (this.options && this.options.length > 0) {
        for (let i = 0; i < this.options.length; i++) {
          this.options[i].key = i;
        }
      }
      return _.orderBy(this.options, 'id');
    }
  },
  methods: {
    onPlatformChange(isOnPlatform) {
      const index = this.editedOption;
      const option = index > -1 ? this.options[index] : null;

      if (isOnPlatform === 'true') {
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
    encodeURL() {
      if (this.thirdPartyUrl) {
        this.thirdPartyUrl = encodeURI(decodeURI(this.thirdPartyUrl));
      }
    },
    changeOption(index) {
      if (index > -1) {
        const option = this.options[index];
        this.id = option.id;
        this.isOnPlatform = String(option.is_on_platform);
        this.currency = option.currency;
        this.mode = option.mode;
        this.stakeLimit = option.stake_limit;
        this.quantity = option.quantity;
        this.price = option.price;
        this.wallet = option.wallet;
        this.thirdPartyUrl = option.third_party_url;
        this.description = option.description;
        this.editedOption = index;
      } else if (!this.isTournamentCategory) {
        this.isOnPlatform = 'false';
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
    updateOption() {
      const options = this.options;
      const index = this.editedOption;
      const pricing = {
        id: index > -1 ? this.id : null,
        // eslint-disable-next-line camelcase
        is_on_platform: this.isOnPlatform === 'true',
        currency: this.currency,
        mode: this.mode,
        // eslint-disable-next-line camelcase
        stake_limit: this.stakeLimit,
        quantity: this.quantity,
        price: this.price,
        wallet: this.wallet,
        // eslint-disable-next-line camelcase
        third_party_url: this.thirdPartyUrl,
        description: this.description
      };
      if (index > -1) {
        options[index] = pricing;
        this.editedOption = -1;
      } else {
        options.push(pricing);
      }
      this._computedWatchers.orderedOptions.run();
      this.$forceUpdate();
      this.editOption = false;
      this.$emit('update:pricing', options);
    },
    cancelEditing() {
      const options = this.options;
      this.editOption = false;
      this.$emit('cancel-editing', options);
    },
    deleteOption(index) {
      this.options.splice(index, 1);
      this.$emit('delete-option', index);
    }
  },
  setup() {
    return {
      orderGetters
    };
  }
};
</script>
<style lang="scss" scoped>
@import "~@storefront-ui/shared/styles/helpers/";
.sf-pricing-details {
  .pricing-list {
		margin: 0 0 var(--spacer-base) 0;
	}
	.pricing {
		display: flex;
		padding: var(--spacer-base) 0;
		border: 1px solid var(--c-light);
		border-width: 1px 0 0 0;
		&:last-child {
			border-width: 1px 0 1px 0;
		}
		&__content {
			flex: 1;
			color: var(--c-text);
		}
		&__actions {
			display: flex;
			flex-direction: column;
			justify-content: space-between;
			align-items: flex-end;
			@include for-desktop {
				flex-direction: row;
				justify-content: flex-end;
				align-items: center;
			}
		}
		&__button-delete {
			--button-background: var(--c-light);
			--button-color: var(--c-dark-variant);
			&:hover {
				--button-background: var(--_c-light-primary);
			}
			@include for-desktop {
				margin: 0 0 0 var(--spacer-base);
			}
		}
		&__option {
			margin: 0 0 var(--spacer-base) 0;
			&:last-child {
				margin: 0;
			}
		}
	}
	.tab-orphan {
		@include for-mobile {
			--tabs-content-border-width: 0;
			--tabs-title-display: none;
			--tabs-content-padding: 0;
		}
	}
	.form {
		@include for-desktop {
			display: flex;
			flex-wrap: wrap;
			align-items: center;
		}
		&__element {
			margin: 0 0 var(--spacer-base) 0;
			@include for-desktop {
				flex: 0 0 100%;
			}
			&--half {
				@include for-desktop {
					flex: 1 1 50%;
				}
				&-even {
					@include for-desktop {
						padding: 0 0 0 var(--spacer-lg);
					}
				}
			}
		}
		&__select {
			padding-bottom: calc(var(--font-xs) * 1.2);
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
	.message {
		margin: 0 0 var(--spacer-base) 0;
	}
	.action-button {
		--button-width: 100%;
		@include for-desktop {
			--button-width: auto;
		}
	}
	.cancel-button {
		margin-top: var(--spacer-sm);
		@include for-desktop {
			margin: 0 0 0 var(--spacer-xl);
		}
	}
  .flag {
    margin-left: 0.4em;
    padding: 0.15em;
  }
}
</style>
