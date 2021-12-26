<template>
  <div class="form__horizontal">
    <!--<SfRadio
      v-e2e="'payment-option'"
      v-for="option in paymentOptions"
      :key="option.value"
      :value="option.value"
      :description="option.description"
      :selected ="selectedOption"
      name="shippingMethod"
      class="form__radio currency"
      @input="selectOption(option.value)"
    >
      <template #label>
        <div class="currency__label">
          {{ option.label }}  <SfBadge class="color-primary sf-badge flag"  v-if="option.flag">{{ option.flag }}</SfBadge>
        </div>
      </template>
    </SfRadio>-->
  </div>
</template>

<script>
import { SfBadge, SfButton, SfRadio } from '@storefront-ui/vue';
import { ref } from '@vue/composition-api';

const PAYMENT_OPTIONS = [
  { label: 'NMR', value: 'NMR', flag: 'Gas-Free' },
  { label: 'DAI', value: 'DAI' }
];

export default {
  name: 'VsfPaymentProvider',

  components: {
    SfButton,
    SfRadio,
    SfBadge
  },

  setup(props, { emit }) {
    const selectedOption = ref('NMR');

    const selectOption = (option) => {
      selectedOption.value = option;
      emit('status');
    };

    return {
      paymentOptions: PAYMENT_OPTIONS,
      selectedOption: selectedOption,
      selectOption
    };
  }
};
</script>

<style lang="scss" scoped>
.currency {
  &__label {
    display: flex;
    justify-content: space-between;
  }

  &__description {
    --radio-description-margin: 0;
    --radio-description-font-size: var(--font-xs);
  }
}
.form {
  &__horizontal {
    @include for-desktop {
      display: flex;
      flex-direction: row;
      //justify-content: space-between;
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
}
.flag {
  margin-left: 0.4em;
  padding: 0.15em;
}
</style>
