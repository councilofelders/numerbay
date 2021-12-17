<template>
  <div>
    <span
      v-if="promoIsApplied"
      class="applied-coupon"
    >
      {{ $t('Applied Coupon') }}:
      <span class="applied-coupon__code">{{ promoCode }}</span>
    </span>
    <span
      v-if="product && productGetters.getOptionById(product, optionId).error"
      class="applied-coupon"
    >
      <span class="applied-coupon__error">{{ productGetters.getOptionById(product, optionId).error }}</span>
    </span>
    <div class="promo-code">
      <SfInput
        v-model="promoCode"
        name="promoCode"
        :disabled="!!promoIsApplied"
        :label="$t('Enter promo code')"
        class="sf-input--filled promo-code__input"
      />
      <SfButton
        class="promo-code__button"
        @click="handleCoupon"
      >
        {{ promoIsApplied ? $t('Remove') : $t('Apply') }}
      </SfButton>
    </div>
  </div>
</template>

<script>
import { SfButton, SfInput } from '@storefront-ui/vue';
import { useProduct, productGetters, cartGetters } from '@vue-storefront/numerbay';
import {
  computed,
  onMounted,
  watch,
  ref
} from '@vue/composition-api';
export default {
  name: 'CouponCode',
  components: {
    SfButton,
    SfInput
  },
  setup(props, context) {
    const id = context.root.$route.query.product;
    const optionId = parseInt(context.root.$route.query.option);
    // const qty = parseInt(context.root.$route.query.qty) || 1;
    const { products } = useProduct(String(id));
    const product = computed(() => products?.value?.data ? products?.value?.data[0] : null);
    // const { cart, applyCoupon, removeCoupon } = useCart();
    const promoCode = ref(context.root.$route.query.coupon || '');
    const promoIsApplied = computed(
      () => cartGetters.getAppliedCoupon(productGetters.getOptionById(product.value, optionId))?.code
    );
    const setCartCoupon = () => {
      promoCode.value = promoIsApplied.value;
    };

    const applyCoupon = async ({ couponCode }) => {
      context.root.$router.push({ query: { ...context.root.$route.query, coupon: couponCode}});
    };

    const removeCoupon = async () => {
      context.root.$router.push({ query: { ...context.root.$route.query, coupon: null}});
    };

    const handleCoupon = async () => {
      await (promoIsApplied.value
        ? removeCoupon({ currentCart: product.value })
        : applyCoupon({ couponCode: promoCode.value }));
    };
    onMounted(setCartCoupon);
    watch(promoIsApplied, setCartCoupon);
    return {
      product,
      handleCoupon,
      promoIsApplied,
      promoCode,
      optionId,
      productGetters
    };
  }
};
</script>
<style lang="scss" scoped>
.applied-coupon {
  &__code {
    font-weight: bold;
  }
  &__error {
    font-weight: bold;
    color: var(--c-danger)
  }
}
.highlighted {
  box-sizing: border-box;
  width: 100%;
  background-color: var(--c-light);
  padding: var(--spacer-xl) var(--spacer-xl) 0;
  &:last-child {
    padding-bottom: var(--spacer-xl);
  }
  .promo-code {
    &__input {
      --input-background: var(--c-white);
      flex: 1;
    }
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
    --input-background: var(--c-light);
    flex: 1;
  }
}
</style>
