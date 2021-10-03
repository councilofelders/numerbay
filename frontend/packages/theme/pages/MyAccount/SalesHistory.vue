<template>
  <SfTabs :open-tab="1">
    <SfTab title="My sales">
      <div v-if="currentOrder">
        <SfButton class="sf-button--text all-orders" @click="currentOrder = null">All Orders</SfButton>
        <OrderInfoPanel :order="currentOrder"/>
        <!--<SfTable class="products">
          <SfTableHeading>
            <SfTableHeader class="products__name">{{ $t('Product') }}</SfTableHeader>
            <SfTableHeader>{{ $t('Quantity') }}</SfTableHeader>
            <SfTableHeader>{{ $t('Price') }}</SfTableHeader>
          </SfTableHeading>
          <SfTableRow v-for="(item, i) in orderGetters.getItems(currentOrder)" :key="i">
            <SfTableData class="products__name">
              <nuxt-link :to="'/p/'+orderGetters.getItemSku(item)+'/'+orderGetters.getItemSku(item)">
                {{orderGetters.getItemName(item)}}
              </nuxt-link>
            </SfTableData>
            <SfTableData>{{orderGetters.getItemQty(item)}}</SfTableData>
            <SfTableData>{{orderGetters.getFormattedPrice(item)}}</SfTableData>
          </SfTableRow>
        </SfTable>-->
      </div>
      <div v-else>
        <p class="message">
          {{ $t('Details and status of sales') }}
          <SfButton class="sf-button color-secondary" @click="refresh" :disabled="loading">
            Refresh
          </SfButton>
        </p>
        <div v-if="orders.length === 0" class="no-orders">
          <p class="no-orders__title">{{ $t('You currently have no sales') }}</p>
          <SfButton class="no-orders__button" @click="$router.push('/my-account/my-listings')">{{ $t('List products') }}</SfButton>
        </div>
        <SfTable v-else class="orders">
          <SfTableHeading>
            <SfTableHeader
              v-for="tableHeader in tableHeaders"
              :key="tableHeader"
              >{{ tableHeader }}</SfTableHeader>
            <!--<SfTableHeader class="orders__element&#45;&#45;right">
              <span class="smartphone-only">{{ $t('Download') }}</span>
              <SfButton
                class="desktop-only sf-button&#45;&#45;text orders__download-all"
                @click="downloadOrders()"
              >
                {{ $t('Download all') }}
              </SfButton>
            </SfTableHeader>-->
          </SfTableHeading>
          <SfTableRow v-for="order in orders" :key="orderGetters.getId(order)">
            <SfTableData>{{ orderGetters.getId(order) }}</SfTableData>
            <SfTableData>
              <SfLink :link="'/p/'+orderGetters.getProduct(order).id+'/'+orderGetters.getItemSku(orderGetters.getProduct(order))">
                {{ orderGetters.getItemSku(orderGetters.getProduct(order)) }}
              </SfLink>
            </SfTableData>
            <SfTableData>{{ orderGetters.getRound(order) }}</SfTableData>
            <SfTableData>{{ orderGetters.getBuyer(order) }}</SfTableData>
            <SfTableData>{{ orderGetters.getFormattedPrice(order, withCurrency=true, decimals=4) }}</SfTableData>
            <SfTableData>
              <span :class="getStatusTextClass(order)">{{ orderGetters.getStatus(order) }}</span>
            </SfTableData>
            <SfTableData class="orders__view orders__element--right">
              <SfButton class="sf-button--text smartphone-only" @click="downloadOrder(order)">
                {{ $t('Download') }}
              </SfButton>
              <SfButton class="sf-button--text desktop-only" @click="currentOrder = order">
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
  SfTabs,
  SfTable,
  SfButton,
  SfProperty,
  SfLink
} from '@storefront-ui/vue';
import { computed, ref } from '@vue/composition-api';
import { useUserOrder, orderGetters } from '@vue-storefront/numerbay';
import { onSSR } from '@vue-storefront/core';
import OrderInfoPanel from '../../components/Molecules/OrderInfoPanel';

export default {
  name: 'SalesHistory',
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
      this.search({ role: 'seller' });
    }
  },
  mounted() {
    this.orderPollingTimer = setInterval(async () => {
      if (this.currentOrder) {
        // console.log('poll');
        await this.search({ role: 'seller' });
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
    const { orders, search, loading } = useUserOrder('sales-history');
    const currentOrder = ref(null);

    onSSR(async () => {
      await search({ role: 'seller' });
    });

    const tableHeaders = [
      'Order ID',
      'Product',
      'Round',
      'Buyer',
      'Amount',
      'Status',
      'Action'
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
      downloadFile(new Blob([JSON.stringify(orders.value)], {type: 'application/json'}), 'orders.json');
    };

    const downloadOrder = async (order) => {
      downloadFile(new Blob([JSON.stringify(order)], {type: 'application/json'}), 'order ' + orderGetters.getId(order) + '.json');
    };

    const handleRefreshClick = async () => {
      await search({ role: 'buyer' });
    };

    return {
      tableHeaders,
      orders: computed(() => orders?.value?.data ? orders.value?.data : []),
      orderGetters,
      search,
      loading,
      handleRefreshClick,
      getStatusTextClass,
      downloadOrder,
      downloadOrders,
      currentOrder
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
.product {
  &__properties {
    margin: var(--spacer-xl) 0 0 0;
  }
  &__property,
  &__action {
    font-size: var(--font-size--sm);
  }
  &__action {
    color: var(--c-gray-variant);
    font-size: var(--font-size--sm);
    margin: 0 0 var(--spacer-sm) 0;
    &:last-child {
      margin: 0;
    }
  }
  &__qty {
    color: var(--c-text);
  }
}
.products {
  --table-column-flex: 1;
  &__name {
    margin-right: var(--spacer-sm);
    @include for-desktop {
      --table-column-flex: 2;
    }
  }
}
</style>
