<template>
  <div id="confirmation">

    <SfLoader :class="{ loading: !isPaymentConfirmed }" :loading="!isPaymentConfirmed"></SfLoader>
    <SfHeading
      :level="4"
      :title="isPaymentConfirmed ? 'Payment Confirmed' : 'Waiting for Payment Confirmation'"
      class="sf-heading--center sf-heading--no-underline title"
    />
    <SfHeading
      :level="5"
      v-if="!loading && !isPaymentConfirmed && orderGetters.getCurrency(order) === 'NMR'"
      title="Please make your NMR transfer through your Numerai wallet within 15 minutes of ordering. You can leave this page."
      class="sf-heading--center sf-heading--no-underline content"
    />
    <div v-if="!loading && !isPaymentConfirmed" class="order-info-panel">
      <OrderInfoPanel :order="order" withCopyButtons="true"/>
      <SfButton class="sf-button--full-width color-secondary" @click="$router.push('/my-account/order-history')">
        {{ $t('Go to My Orders') }}
      </SfButton>
    </div>
  </div>
</template>

<script>
import {
  SfHeading,
  SfTable,
  SfCheckbox,
  SfButton,
  SfDivider,
  SfImage,
  SfIcon,
  SfPrice,
  SfProperty,
  SfAccordion,
  SfLink,
  SfLoader
} from '@storefront-ui/vue';
import { computed } from '@vue/composition-api';
import { orderGetters, useUserOrder } from '@vue-storefront/numerbay';
import OrderInfoPanel from '../../components/Molecules/OrderInfoPanel';

export default {
  name: 'Confirmation',
  components: {
    SfHeading,
    SfTable,
    SfCheckbox,
    SfButton,
    SfDivider,
    SfImage,
    SfIcon,
    SfPrice,
    SfProperty,
    SfAccordion,
    SfLink,
    SfLoader,
    OrderInfoPanel
  },
  watch: {
    orderStatus(value) {
      if (value === 'confirmed') {
        this.$router.push('/my-account/order-history');
      }
    }
  },
  mounted() {
    this.orderPollingTimer = setInterval(async () => {
      console.log('status: ', this.orderStatus);
      if (this.orderStatus !== 'pending' && this.orderStatus !== 'unknown') {
        clearInterval(this.orderPollingTimer);
        await this.$router.push('/my-account/order-history');
        return;
      }
      const id = this.$route.query.order;
      await this.search({ role: 'buyer', id });
    }, 5000);
  },
  beforeDestroy() {
    clearInterval(this.orderPollingTimer);
  },
  beforeRouteLeave (to, from, next) {
    if (this.orderPollingTimer)
      clearInterval(this.orderPollingTimer);
    next();
  },
  setup(props, context) {
    const id = context.root.$route.query.order;
    const { orders, search, loading } = useUserOrder();

    search({ role: 'buyer', id });

    const order = computed(() => (orders?.value?.data || [])[0]);
    const orderStatus = computed(() => orderGetters.getStatus((orders?.value?.data || [])[0]));
    const isPaymentConfirmed = computed(() => orderGetters.getStatus((orders?.value?.data || [])[0]) === 'confirmed');

    if (orderStatus.value !== 'pending' && orderStatus.value !== 'unknown') {
      context.root.$router.push('/my-account/order-history');
    }

    return {
      loading,
      orderStatus,
      isPaymentConfirmed,
      search,
      order,
      orderGetters
    };
  }
};
</script>

<style lang="scss" scoped>
.title {
  padding-top: var(--spacer-xl);
  margin: var(--spacer-xl) 0 var(--spacer-base) 0;
}
.table {
  margin: 0 0 var(--spacer-base) 0;
  &__row {
    justify-content: space-between;
  }
  @include for-desktop {
    &__header {
      text-align: center;
      &:last-child {
        text-align: right;
      }
    }
    &__data {
      text-align: center;
    }
    &__description {
      text-align: left;
      flex: 0 0 12rem;
    }
    &__image {
      --image-width: 5.125rem;
      text-align: left;
      margin: 0 var(--spacer-xl) 0 0;
    }
  }
}
.product-sku {
  color: var(--c-text-muted);
  font-size: var(--font-size--sm);
}
.price {
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
}
.product-price {
  --price-font-size: var(--font-size--base);
}
.summary {
  &__terms {
    margin: var(--spacer-base) 0 0 0;
  }
  &__total {
    margin: 0 0 var(--spacer-sm) 0;
    flex: 0 0 16.875rem;
  }
  &__action {
    @include for-desktop {
      display: flex;
      margin: var(--spacer-xl) 0 0 0;
    }
  }
  &__action-button {
    margin: 0;
    width: 100%;
    margin: var(--spacer-sm) 0 0 0;
    @include for-desktop {
      margin: 0 var(--spacer-xl) 0 0;
      width: auto;
    }
    &--secondary {
      @include for-desktop {
        text-align: right;
      }
    }
  }
  &__back-button {
    margin: var(--spacer-xl) 0 0 0;
    width: 100%;
    @include for-desktop {
      margin: 0 var(--spacer-xl) 0 0;
      width: auto;
    }
    color:  var(--c-white);
    &:hover {
      color:  var(--c-white);
    }
  }
  &__property-total {
    margin: var(--spacer-xl) 0 0 0;
  }
}
.property {
  margin: 0 0 var(--spacer-sm) 0;
  &__name {
    color: var(--c-text-muted);
  }
}
.accordion {
  margin: 0 0 var(--spacer-xl) 0;
  &__item {
    display: flex;
    align-items: flex-start;
  }
  &__content {
    flex: 1;
  }
  &__edit {
    flex: unset;
  }
}
.content {
  margin: 0 0 var(--spacer-xl) 0;
  color: var(--c-text);
  &:last-child {
    margin: 0;
  }
  &__label {
    font-weight: var(--font-weight--normal);
  }
}
.order-info-panel {
  width: 75%;
  margin:0 auto;
}
</style>
