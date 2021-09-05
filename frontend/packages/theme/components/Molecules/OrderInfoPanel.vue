<template>
  <div class="highlighted highlighted--total">
    <SfProperty
      name="Order ID"
      :value="orderGetters.getId(order)"
      class="sf-property--full-width property"
    />
    <SfProperty
      name="Product"
      :value="orderGetters.getItemSku(orderGetters.getProduct(order))"
      class="sf-property--full-width property"
    />
    <SfProperty
      name="Round"
      :value="orderGetters.getRound(order)"
      class="sf-property--full-width property"
    />
    <SfProperty
      name="Date"
      :value="orderGetters.getDate(order)"
      class="sf-property--full-width property"
    />
    <SfProperty
      name="Buyer"
      :value="orderGetters.getBuyer(order)"
      class="sf-property--full-width property"
    />
    <SfProperty
      name="From Address"
      :value="orderGetters.getFromAddress(order)"
      class="sf-property--full-width property"
    />
    <SfProperty
      name="To Address"
      class="sf-property--full-width property"
    >
      <template #value>
        <span class="sf-property__value">
          {{orderGetters.getToAddress(order)}}
        <SfButton
            v-if="withCopyButtons"
            class="sf-button--text"
            @click="copyToClipboard(orderGetters.getToAddress(order))"
        >
          Copy
        </SfButton>
        </span>
      </template>
    </SfProperty>
    <SfProperty
      name="Total"
      class="sf-property--full-width property"
    >
      <template #value>
        <span class="sf-property__value">
          {{orderGetters.getFormattedPrice(order, withCurrency=true, decimals=4)}}
        <SfButton
            v-if="withCopyButtons"
            class="sf-button--text"
            @click="copyToClipboard(orderGetters.getPrice(order))"
        >
          Copy
        </SfButton>
        </span>
      </template>
    </SfProperty>
    <SfProperty
      name="Transaction Hash"
      class="sf-property--full-width property"
    >
      <template #value>
        <span class="sf-property__value" v-if="orderGetters.getTransactionHash(order)" >
          <SfInput :value="orderGetters.getTransactionHash(order)" class="sf-input--outline"></SfInput>
        </span>
        <span class="sf-property__value" v-else>
          waiting
        </span>
      </template>
    </SfProperty>
    <SfProperty
      name="Status"
      :value="orderGetters.getStatus(order)"
      class="sf-property--full-width property"
    />
  </div>
</template>

<script>
import { SfProperty, SfIcon, SfButton, SfInput } from '@storefront-ui/vue';
import { orderGetters } from '@vue-storefront/numerbay';

export default {
  name: 'OrderInfoPanel',
  components: {
    SfProperty,
    SfIcon,
    SfButton,
    SfInput
  },
  props: {
    order: {
      default: null
    },
    withCopyButtons: {
      default: false
    }
  },
  methods: {
    async copyToClipboard(text) {
      try {
        await this.$copyText(text);
      } catch (e) {
        console.error('Copy failed: ', e);
      }
    }
  },
  // eslint-disable-next-line no-unused-vars,@typescript-eslint/explicit-module-boundary-types,@typescript-eslint/no-unused-vars
  setup(props, { emit }) {
    return {
      orderGetters
    };
  }

};
</script>

<style lang="scss" scoped>
.highlighted {
  box-sizing: border-box;
  width: 100%;
  background-color: var(--c-light);
  padding: var(--spacer-sm);
  --property-value-font-size: var(--font-size--base);
  --property-name-font-size: var(--font-size--base);
  &:last-child {
    margin-bottom: 0;
  }
  ::v-deep .sf-property__name {
    white-space: nowrap;
  }
  ::v-deep .sf-property__value {
    text-align: right;
  }
  &--total {
    margin-bottom: var(--spacer-sm);
  }
  @include for-desktop {
    padding: var(--spacer-xl);
    --property-name-font-size: var(--font-size--lg);
    --property-name-font-weight: var(--font-weight--medium);
    --property-value-font-size: var(--font-size--lg);
    --property-value-font-weight: var(--font-weight--semibold);
  }
}
</style>
