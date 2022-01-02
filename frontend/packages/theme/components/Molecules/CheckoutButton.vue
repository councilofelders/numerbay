<template>
  <div>
    <SfSelect
      v-e2e="'size-select'"
      :disabled="!(productGetters.getOptions(product).length > 1)"
      v-model="optionIdx"
      label="Option"
      class="sf-select--underlined product__select-size"
      required
    >
      <SfSelectOption v-for="(option, key) in productGetters.getOrderedOptions(product)" :key="key" :value="key">{{ productGetters.getFormattedOption(option) }}</SfSelectOption>
    </SfSelect>
    <SfAddToCart
      v-e2e="'product_add-to-cart'"
      v-model="qty"
      :disabled="!productGetters.getIsActive(product) || !productGetters.getOptionIsOnPlatform(productGetters.getOrderedOption(product, optionIdx)) || !productGetters.getCategory(product).is_per_round"
      class="sf-product-card-horizontal__add-to-cart desktop-only"
    >
      <template #add-to-cart-btn>
        <SfButton
          class="sf-add-to-cart__button"
          :disabled="!productGetters.getIsAvailable(product, optionIdx)"
          @click="$emit('buy', optionIdx, qty)"
        >
          {{productGetters.getIsAvailable(product, optionIdx) ? `${productGetters.getOptionIsOnPlatform(productGetters.getOrderedOption(product, optionIdx)) ? 'Buy for' : 'For Ref Price '} ${productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, optionIdx), true)}` : 'Product Delisted'}}
        </SfButton>
      </template>
    </SfAddToCart>
  </div>
</template>

<script>
import { SfAddToCart, SfButton, SfSelect } from '@storefront-ui/vue';
import { productGetters } from '@vue-storefront/numerbay';

export default {
  name: 'CheckoutButton',

  components: {
    SfAddToCart,
    SfButton,
    SfSelect
  },

  data() {
    return {
      optionIdx: '0',
      qty: 1
    };
  },

  props: {
    product: {
      type: Object
    }
  },
  // eslint-disable-next-line no-unused-vars,@typescript-eslint/explicit-module-boundary-types,@typescript-eslint/no-unused-vars
  setup(props, { emit }) {
    return {
      productGetters
    };
  }

};
</script>

<style lang="scss" scoped>

</style>
