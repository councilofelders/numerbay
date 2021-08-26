<template>
  <SfButton class="bid-button" :disabled="disabled" v-on="$listeners">
    <div class="stats">
      <div class="stat-value">
        {{ price }}
      </div>
      <h3>{{ label }}</h3>
    </div>
    <div class="button-divider"></div>
    <div>
      <h2>{{ disabled? 'NA':'BUY' }}</h2>
    </div>
  </SfButton>
</template>

<script>
import { SfButton } from '@storefront-ui/vue';

export default {
  name: 'BuyButton',

  components: {
    SfButton
  },

  props: {
    disabled: {
      type: Boolean,
      default: false
    },
    price: {
      tyoe: [Number, String],
      default: '$-'
    },
    label: {
      type: String,
      default: 'Price'
    }
  },
  // eslint-disable-next-line no-unused-vars,@typescript-eslint/explicit-module-boundary-types,@typescript-eslint/no-unused-vars
  setup(props, { emit }) {
    return {};
  }

};
</script>

<style lang="scss" scoped>
.bid-button {
  text-decoration: none;
  background-color: #08a05c;
  padding: 0.6em;
  flex-wrap: nowrap;
  flex-direction: row;
}
.button-divider {
  align-self: stretch;
  border-left: 1px solid green;
  margin: 0 18px;
}
.bid-button h2 {
  font-size: var(--h3-font-size);;
}
.bid-button h3 {
  color: #c6e6c2;
  font-size: var(--font-size--sm);
}
.bid-button:disabled,
.bid-button[disabled]{
  background-color: var(--c-gray-lighten);
  h3 {
    color: var(--c-text-disabled);
    font-size: var(--font-size--sm);
  }
  .button-divider {
    align-self: stretch;
    border-left: 1px solid var(--c-text-disabled);
    margin: 0 18px;
  }
}
.stats {
  text-align: left;
}
.stat-value {
  font-size: var(--h3-font-size);;
  font-weight: 500;
}
</style>
