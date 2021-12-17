<template>
  <div>
    <div class="highlighted">
      <SfHeading
        :level="3"
        title="Order summary"
        class="sf-heading--left sf-heading--no-underline title"
      />
    </div>
    <div class="highlighted">
      <SfLoader :class="{ loader: loading }" :loading="loading">
        <SfProperty
          name="Number of Rounds"
          v-if="!loading && !!products[0] && products[0].category.is_per_round"
          :value="parseInt(productOption.quantity)"
          class="sf-property--full-width sf-property--large property"
        />
        <SfProperty
          name="Order Quantity"
          v-else
          :value="qty"
          class="sf-property--full-width sf-property--large property"
        />
      </SfLoader>
      <!--<SfProperty
        name="Subtotal"
        :value="productGetters.getFormattedPrice(products[0])"
        :class="[
          'sf-property&#45;&#45;full-width',
          'sf-property&#45;&#45;large',
        ]"
      />-->
      <SfLoader :class="{ loader: loading }" :loading="loading">
          <SfProperty
            name="Total"
            v-if="!loading && !!products[0]"
            :value="`${(productOption.price).toFixed(4)} ${productOption.currency}`"
            class="sf-property--full-width sf-property--large property-total"
          >
            <template #value={props}>
              <span class="sf-property__value">
                <span :class="[{ discounted: productOption.special_price }]">{{ props.value }}</span>
                <span v-if="!loading && !!products[0] && productOption.special_price">
                  <br/>
                  {{ `${(productOption.special_price).toFixed(4)} ${productOption.currency}` }}
                </span>
              </span>
            </template>
          </SfProperty>
      </SfLoader>
    </div>
    <CouponCode class="highlighted" />
    <div class="highlighted">
      <SfCharacteristic
        v-for="characteristic in characteristics"
        :key="characteristic.title"
        :title="characteristic.title"
        :description="characteristic.description"
        :icon="characteristic.icon"
        class="characteristic"
      />
    </div>
  </div>
</template>
<script>
import {
  SfHeading,
  SfButton,
  SfCollectedProduct,
  SfProperty,
  SfCharacteristic,
  SfInput,
  SfCircleIcon,
  SfLoader
} from '@storefront-ui/vue';
import { computed, ref } from '@vue/composition-api';
import {useCart, useProduct, checkoutGetters, cartGetters, productGetters} from '@vue-storefront/numerbay';
import CouponCode from '../CouponCode.vue';

export default {
  name: 'CartPreview',
  components: {
    SfHeading,
    SfButton,
    SfCollectedProduct,
    SfProperty,
    SfCharacteristic,
    SfInput,
    SfCircleIcon,
    SfLoader,
    CouponCode
  },
  setup (props, context) {
    const id = context.root.$route.query.product;
    const optionId = parseInt(context.root.$route.query.option);
    const qty = parseInt(context.root.$route.query.qty) || 1;
    const { cart, removeItem, updateItemQty, applyCoupon } = useCart();
    const { products, loading } = useProduct(String(id));
    const listIsHidden = ref(false);
    const totalItems = computed(() => cartGetters.getTotalItems(cart.value));
    const discounts = computed(() => cartGetters.getDiscounts(cart.value));
    const shippingMethodPrice = computed(() => checkoutGetters.getShippingMethodPrice(cart.value));
    return {
      shippingMethodPrice,
      discounts,
      totalItems,
      listIsHidden,
      products: computed(() => products?.value?.data ? products?.value?.data : []),
      productOption: computed(() => products?.value?.data ? productGetters.getOptionById(products?.value?.data[0], optionId) : []),
      loading,
      productGetters,
      removeItem,
      updateItemQty,
      checkoutGetters,
      cartGetters,
      applyCoupon,
      characteristics: [
        {
          title: 'Safety',
          description: 'Your payment is sent directly to the seller',
          icon: 'safety'
        },
        {
          title: 'Delivery',
          description:
            'You’ll be able to download/submit artifacts when seller uploads the item',
          icon: 'shipping'
        }
      ],
      optionId,
      qty
    };
  }
};
</script>

<style lang="scss" scoped>
.highlighted {
  box-sizing: border-box;
  width: 100%;
  background-color: var(--c-light);
  padding: var(--spacer-xl) var(--spacer-xl) 0;
  &:last-child {
    padding-bottom: var(--spacer-xl);
  }
}
.total-items {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacer-xl);
}
.property {
  margin-bottom: var(--spacer-base);
}
.property-total {
  margin-top: var(--spacer-xl);
  padding-top: var(--spacer-lg);
  font-size: var(--font-size-xl);
  border-top: var(--c-white) 1px solid;
  --property-name-font-weight: var(--font-weight--semibold);
  --property-name-color: var(--c-text);
}
.characteristic {
  &:not(:last-child) {
    margin-bottom: var(--spacer-lg);
  }
}
.promo-code {
  display: flex;
  align-items: flex-start;
  &__button {
    --button-width: 6.3125rem;
    --button-height: var(--spacer-lg);
  }
  &__input {
    --input-background: var(--c-white);
    flex: 1;
  }
}
.discounted {
  &::v-deep {
    color: var(--c-danger);
    text-decoration: line-through;
  }
}
.special-price {
  justify-content: flex-end;
  &::v-deep .sf-property__name {
    display: none;
  }
}
</style>
