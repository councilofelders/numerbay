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
      name="Date"
      :value="orderGetters.getDate(order)"
      class="sf-property--full-width property"
    />
    <SfProperty
      name="Status"
      :value="orderGetters.getStatus(order)"
      class="sf-property--full-width property"
    />
    <SfProperty
      name="Total"
      :value="orderGetters.getFormattedPrice(order)"
      class="sf-property--full-width property"
    />
    <SfProperty
      name="From Address"
      :value="orderGetters.getFromAddress(order)"
      class="sf-property--full-width property"
    />
    <SfProperty
      name="To Address"
      :value="orderGetters.getToAddress(order)"
      class="sf-property--full-width property"
    />
    <SfProperty
      name="Transaction Hash"
      :value="orderGetters.getTransactionHash(order) || 'Waiting...'"
      class="sf-property--full-width property"
    />
  </div>
</template>

<script>
import { SfProperty } from '@storefront-ui/vue';
import { orderGetters } from '@vue-storefront/numerbay';

export default {
  name: 'OrderInfoPanel',

  components: {
    SfProperty
  },

  props: {
    order: {
      default: null
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
