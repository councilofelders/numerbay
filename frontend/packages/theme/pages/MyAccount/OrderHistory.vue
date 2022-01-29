<template>
  <SfTabs :open-tab="1">
    <SfTab title="My orders">
      <div v-if="currentOrder">
        <SfButton class="sf-button--text all-orders" @click="currentOrder = null">All Orders</SfButton>
        <OrderInfoPanel :order="currentOrder" :encryptedPrivateKey="user.encrypted_private_key" :publicKey="user.public_key" :withCopyButtons="orderGetters.getStatus(currentOrder)==='pending'"/>
      </div>
      <div v-else>
        <p class="message">
          {{ $t('Details and status of orders') }}
          <SfButton class="sf-button color-secondary" @click="refresh" :disabled="loading">
            Refresh
          </SfButton>
        </p>
        <div v-if="orders.length === 0" class="no-orders">
          <p class="no-orders__title">{{ $t('You currently have no orders') }}</p>
          <SfButton class="no-orders__button" @click="$router.push('/c/numerai')">{{ $t('Start shopping') }}</SfButton>
        </div>
        <SfTable v-else class="orders">
          <SfTableHeading>
            <SfTableHeader
              v-for="tableHeader in tableHeaders"
              :key="tableHeader"
              >{{ tableHeader }}</SfTableHeader>
            <SfTableHeader class="orders__element--right">
              <span class="smartphone-only">{{ $t('Download') }}</span>
              <SfButton
                class="desktop-only sf-button--text orders__download-all"
                @click="downloadOrders()"
              >
                {{ $t('Export CSV') }}
              </SfButton>
            </SfTableHeader>
          </SfTableHeading>
          <SfTableRow v-for="order in orders" :key="orderGetters.getId(order)">
            <SfTableData>{{ orderGetters.getId(order) }}</SfTableData>
            <SfTableData>
              <SfLink :link="'/p/'+orderGetters.getProduct(order).id+'/'+orderGetters.getItemSku(orderGetters.getProduct(order))">
                {{ orderGetters.getItemSku(orderGetters.getProduct(order)) }}
              </SfLink>
            </SfTableData>
            <SfTableData v-if="orderGetters.getProduct(order).category.is_per_round && parseInt(orderGetters.getItemQty(order)) > 1">{{ `${orderGetters.getRound(order)}-${parseInt(orderGetters.getRound(order))+parseInt(orderGetters.getItemQty(order))-1}` }}</SfTableData>
            <SfTableData v-else>{{ orderGetters.getRound(order) }}</SfTableData>
            <SfTableData>{{ orderGetters.getFormattedPrice(order, withCurrency=true, decimals=4) }}</SfTableData>
            <SfTableData>
              <span :class="getStatusTextClass(order)">{{ orderGetters.getStatus(order) }}</span>
            </SfTableData>
            <SfTableData>
              <span :class="getSubmissionStatusTextClass(order)">{{ orderGetters.getSubmissionStatus(order) }}</span>
            </SfTableData>
            <SfTableData class="orders__view orders__element--right">
              <!--<SfButton class="sf-button&#45;&#45;text smartphone-only" @click="downloadOrder(order)">
                {{ $t('Download') }}
              </SfButton>-->
              <SfButton class="sf-button--text" @click="currentOrder = order">
                {{ $t('View details') }}
              </SfButton>
            </SfTableData>
          </SfTableRow>
        </SfTable>
      </div>
    </SfTab>
  </SfTabs>
</template>

<script>
import {
  SfButton,
  SfLink,
  SfProperty,
  SfTable,
  SfTabs
} from '@storefront-ui/vue';
import { computed, ref } from '@vue/composition-api';
import { orderGetters, productGetters, useUser, useUserOrder } from '@vue-storefront/numerbay';
import OrderInfoPanel from '../../components/Molecules/OrderInfoPanel';
import { onSSR } from '@vue-storefront/core';

export default {
  name: 'OrderHistory',
  components: {
    SfTabs,
    SfTable,
    SfButton,
    SfProperty,
    SfLink,
    OrderInfoPanel
  },
  methods: {
    refresh() {
      this.search({ role: 'buyer' });
    }
  },
  mounted() {
    this.orderPollingTimer = setInterval(async () => {
      if (this.currentOrder) {
        // console.log('poll');
        await this.search({ role: 'buyer' });
        // console.log('this.orders', this.orders.filter((o)=>o.id === this.currentOrder.id))
        this.currentOrder = this.orders.filter((o)=>o.id === this.currentOrder.id)[0];
        if (orderGetters.getStatus(this.currentOrder) === 'confirmed') {
          // console.log('order confirmed, canceling polling');
          clearInterval(this.orderPollingTimer);
        }
      }
    }, 10000);
  },
  beforeDestroy() {
    clearInterval(this.orderPollingTimer);
  },
  beforeRouteLeave (to, from, next) {
    if (this.orderPollingTimer)
      clearInterval(this.orderPollingTimer);
    next();
  },
  setup() {
    const { user } = useUser();
    const { orders, search, loading } = useUserOrder('order-history');
    const currentOrder = ref(null);

    onSSR(async () => {
      await search({ role: 'buyer' });
    });

    const tableHeaders = [
      'Order ID',
      'Product',
      'Round(s)',
      'Amount',
      'Order Status',
      'Submission'
      // 'Action'
    ];

    const getStatusTextClass = (order) => {
      const status = orderGetters.getStatus(order);
      switch (status) {
        case 'expired':
          return 'text-danger';
        case 'pending':
          return 'text-warning';
        case 'confirmed':
          return 'text-success';
        default:
          return '';
      }
    };

    const getSubmissionStatusTextClass = (order) => {
      const status = orderGetters.getSubmissionStatus(order);
      switch (status) {
        case 'failed':
          return 'text-danger';
        case 'queued':
          return 'text-warning';
        case 'completed':
          return 'text-success';
        default:
          return '';
      }
    };

    const downloadFile = (file, name) => {
      const a = document.createElement('a');
      document.body.appendChild(a);
      a.style = 'display: none';

      const url = window.URL.createObjectURL(file);
      a.href = url;
      a.download = name;
      a.click();
      window.URL.revokeObjectURL(url);
    };

    const downloadOrders = async () => {
      let csvContent = [
        'Order ID',
        'Date',
        'Round',
        'Product',
        'Quantity (Round)',
        'Seller',
        'Amount (NMR)',
        'Mode',
        'Transaction Hash',
        'Status',
        'Submit to Model',
        'Submission Status',
        'Stake Limit'
      ].join(',') + '\r\n';

      orders.value.data.forEach((order) => {
        const row = [
          order.id,
          order.date_order,
          orderGetters.getRound(order),
          orderGetters.getItemSku(orderGetters.getProduct(order)),
          parseInt(orderGetters.getItemQty(order)),
          productGetters.getOwner(orderGetters.getProduct(order)),
          orderGetters.getFormattedPrice(order, false, 4),
          order.mode,
          orderGetters.getTransactionHash(order),
          orderGetters.getStatus(order),
          orderGetters.getSubmitModelName(order),
          orderGetters.getSubmissionStatus(order),
          orderGetters.getStakeLimit(order)
        ].join(',');
        csvContent += row + '\r\n';
      });
      // convertToCSV(JSON.stringify(orders.value))
      downloadFile(new Blob([csvContent], {type: 'application/csv'}), 'orders.csv');
    };

    return {
      tableHeaders,
      orders: computed(() => orders?.value?.data ? orders.value?.data : []),
      orderGetters,
      search,
      loading,
      getStatusTextClass,
      getSubmissionStatusTextClass,
      downloadOrders,
      currentOrder,
      user
    };
  }
};
</script>

<style lang='scss' scoped>
.no-orders {
  &__title {
    margin: 0 0 var(--spacer-lg) 0;
    font: var(--font-weight--normal) var(--font-size--base) / 1.6 var(--font-family--primary);
  }
  &__button {
    --button-width: 100%;
    @include for-desktop {
      --button-width: 17,5rem;
    }
  }
}
.orders {
  @include for-desktop {
    &__element {
      &--right {
        --table-column-flex: 0;
        text-align: right;
      }
    }
  }
}
.all-orders {
  --button-padding: var(--spacer-base) 0;
}
.message {
  margin: 0 0 var(--spacer-xl) 0;
  font: var(--font-weight--light) var(--font-size--base) / 1.6 var(--font-family--primary);
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  &__link {
    color: var(--c-primary);
    font-weight: var(--font-weight--medium);
    font-family: var(--font-family--primary);
    font-size: var(--font-size--base);
    text-decoration: none;
    &:hover {
      color: var(--c-text);
    }
  }
}
</style>
