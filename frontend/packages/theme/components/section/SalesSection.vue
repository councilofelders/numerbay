<template>
  <div class="col-lg-8">
    <div class="user-panel-title-box">
      <div class="d-flex">
        <h3>Sales</h3>
        <button class="icon-btn ms-auto" title="Refresh" :disabled="loading" @click="refresh">
          <em class="ni ni-reload" v-if="!loading"></em><span class="spinner-border spinner-border-sm" role="status"
                                                              v-else></span>
        </button>
      </div>
    </div><!-- end user-panel-title-box -->
    <div class="profile-setting-panel-wrap">
      <div class="table-responsive">
        <table class="table mb-0 table-s2">
          <thead class="fs-14">
          <tr>
            <th scope="col" v-for="(list, i) in [
                              '#',
                              'Product',
                              'Round(s)',
                              'Amount',
                              'Status'
                            ]" :key="i">{{ list }}
            </th>
          </tr>
          </thead>
          <tbody class="fs-13">
          <tr v-if="!displayedOrders || displayedOrders.length === 0">
            <td colspan="3" class="text-secondary">You currently have no sale</td>
          </tr>
          <tr v-for="order in displayedOrders" :key="order.id">
            <th scope="row"><a href="javascript:void(0);" @click="toggleModal(order)"
                               title="Click for details">{{ orderGetters.getId(order) }}</a></th>
            <td>
              <router-link class="btn-link"
                           :to="`/product/${productGetters.getCategory(orderGetters.getProduct(order)).slug}/${productGetters.getName(orderGetters.getProduct(order))}`">
                {{ orderGetters.getItemSku(orderGetters.getProduct(order)) }}
              </router-link>
            </td>
            <td
              v-if="orderGetters.getProduct(order).category.is_per_round && parseInt(orderGetters.getItemQty(order)) > 1">
              {{
                `${orderGetters.getRound(order)}-${parseInt(orderGetters.getRound(order)) + parseInt(orderGetters.getItemQty(order)) - 1}`
              }}
            </td>
            <td v-else>{{ orderGetters.getRound(order) }}</td>
            <td>{{ orderGetters.getFormattedPrice(order, withCurrency = true, decimals = 4) }}</td>
            <td><span class="badge fw-medium" :class="getStatusTextClass(order)">{{
                orderGetters.getStatus(order)
              }}</span></td>
          </tr>
          </tbody>
        </table>
      </div><!-- end table-responsive -->
      <!-- pagination -->
      <div class="text-center mt-4 mt-md-5">
        <Pagination :records="orders.length" v-model="page" :per-page="perPage"></Pagination>
      </div>
    </div><!-- end profile-setting-panel-wrap-->
    <OrderInfoModal :order="currentOrder" modelId="orderInfoModal" ref="orderInfoModal"></OrderInfoModal>
  </div><!-- end col-lg-8 -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';
import Pagination from 'vue-pagination-2';

// Composables
import {onSSR} from '@vue-storefront/core';
import {computed} from '@vue/composition-api';
import {orderGetters, productGetters, useUserOrder} from '@vue-storefront/numerbay';

export default {
  name: 'SalesSection',
  components: {
    Pagination
  },
  data() {
    return {
      SectionData,
      page: 1,
      perPage: 6,
      currentOrder: {}
    };
  },
  computed: {
    displayedOrders() {
      const startIndex = this.perPage * (this.page - 1);
      const endIndex = startIndex + this.perPage;
      return this.orders?.slice(startIndex, endIndex);
    }
  },
  methods: {
    toggleModal(order) {
      this.currentOrder = order;
      this.$refs.orderInfoModal.show();
    },
    refresh() {
      this.search({role: 'seller'});
    }
  },
  mounted() {
    this.orderPollingTimer = setInterval(async () => {
      await this.search({role: 'seller'});
      if (this.currentOrder?.id) {
        this.currentOrder = this.orders.filter((o) => o.id === this.currentOrder.id)[0];
      }
    }, 15000);
  },
  beforeDestroy() {
    clearInterval(this.orderPollingTimer);
  },
  beforeRouteLeave(to, from, next) {
    if (this.orderPollingTimer)
      clearInterval(this.orderPollingTimer);
    next();
  },
  setup() {
    const {orders, search, loading} = useUserOrder('sales-history');

    onSSR(async () => {
      await search({role: 'seller'});
    });

    const getStatusTextClass = (order) => {
      const status = orderGetters.getStatus(order);
      switch (status) {
        case 'expired':
          return 'bg-danger';
        case 'pending':
          return 'bg-warning';
        case 'confirmed':
          return 'bg-success';
        default:
          return '';
      }
    };

    const getSubmissionStatusTextClass = (order) => {
      const status = orderGetters.getSubmissionStatus(order);
      switch (status) {
        case 'failed':
          return 'bg-danger';
        case 'queued':
          return 'bg-warning';
        case 'completed':
          return 'bg-success';
        default:
          return '';
      }
    };

    return {
      orders: computed(() => orders?.value?.data ? orders.value?.data : []),
      loading,
      orderGetters,
      productGetters,
      search,
      getStatusTextClass,
      getSubmissionStatusTextClass
    };
  }
};
</script>
