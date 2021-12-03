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
      v-if="order && !isPaymentConfirmed && orderGetters.getCurrency(order) === 'NMR'"
      title="Please make your NMR transfer through your Numerai wallet within 30 minutes of ordering. You can leave this page."
      class="sf-heading--center sf-heading--no-underline content"
    />
    <div v-if="order && !isPaymentConfirmed" class="order-info-panel">
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
  SfButton,
  SfLoader
} from '@storefront-ui/vue';
import { computed } from '@vue/composition-api';
import { orderGetters, useUserOrder } from '@vue-storefront/numerbay';
import OrderInfoPanel from '../../components/Molecules/OrderInfoPanel';

export default {
  name: 'Confirmation',
  components: {
    SfHeading,
    SfButton,
    SfLoader,
    OrderInfoPanel
  },
  watch: {
    orderStatus(value) {
      if (value !== 'pending' && value !== 'unknown') {
        this.$router.push('/my-account/order-history');
      }
    }
  },
  mounted() {
    this.orderPollingTimer = setInterval(async () => {
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
    const { orders, search, loading } = useUserOrder(id);

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
  @include for-mobile {
    width: 100%
  }
}
</style>
