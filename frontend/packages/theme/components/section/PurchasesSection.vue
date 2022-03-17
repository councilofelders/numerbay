<template>
    <div class="col-lg-8">
        <div class="user-panel-title-box">
            <h3>Purchases</h3>
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
                              'Status',
                              'Action'
                            ]" :key="i">{{ list }}</th>
                        </tr>
                    </thead>
                    <tbody class="fs-13">
                        <tr v-for="order in displayedOrders" :key="order.id">
                            <th scope="row"><a href="javascript:void(0);" @click="toggleInfoModal(order)" title="Click for details">{{ orderGetters.getId(order) }}</a></th>
                          <td><router-link class="btn-link" :to="`/product/${productGetters.getCategory(orderGetters.getProduct(order)).slug}/${productGetters.getName(orderGetters.getProduct(order))}`">{{ orderGetters.getItemSku(orderGetters.getProduct(order)) }}</router-link></td>
                            <td v-if="orderGetters.getProduct(order).category.is_per_round && parseInt(orderGetters.getItemQty(order)) > 1">{{ `${orderGetters.getRound(order)}-${parseInt(orderGetters.getRound(order))+parseInt(orderGetters.getItemQty(order))-1}` }}</td>
                            <td v-else>{{ orderGetters.getRound(order) }}</td>
<!--                            <td>{{ orderGetters.getFormattedPrice(order, withCurrency=true, decimals=4) }}</td>-->
                            <td><span class="badge fw-medium" :class="getStatusTextClass(order)">{{ orderGetters.getStatus(order) }}</span></td>
                            <td>
                              <div class="d-flex justify-content-between" v-if="orderGetters.getStatus(order)=='confirmed'">
                                <button class="icon-btn ms-auto" title="Download Artifacts" @click="toggleArtifactModal(order)"><em class="ni ni-download"></em></button>
                              </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div><!-- end table-responsive -->
            <!-- pagination -->
            <div class="text-center mt-4 mt-md-5">
                <Pagination :records="orders.length" v-model="page" :per-page="perPage"></Pagination>
            </div>
        </div><!-- end profile-setting-panel-wrap-->
        <OrderInfoModal :order="currentOrder" modelId="orderInfoModal" ref="orderInfoModal" :withCopyButtons="true"></OrderInfoModal>
        <div v-if="currentOrder.product"><ArtifactModal :order="currentOrder" :encryptedPrivateKey="user.encrypted_private_key" :publicKey="user.public_key" modelId="artifactModal" ref="artifactModal"></ArtifactModal></div>
    </div><!-- end col-lg-8 -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';
import Pagination from 'vue-pagination-2';

// Composables
import { onSSR } from '@vue-storefront/core';
import { computed } from '@vue/composition-api';
import { orderGetters, productGetters, useUser, useUserOrder } from '@vue-storefront/numerbay';

export default {
  name: 'PurchasesSection',
  components: {
    Pagination
  },
  data () {
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
    toggleInfoModal(order) {
      this.currentOrder = order;
      this.$refs.orderInfoModal.show();
    },
    toggleArtifactModal(order) {
      this.currentOrder = order;
      this.$nextTick(() => {
        this.$refs.artifactModal.show();
      });
    }
  },
  setup() {
    const { user } = useUser();
    const { orders, search, loading } = useUserOrder('order-history');

    onSSR(async () => {
      await search({ role: 'buyer' });
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
      user,
      orderGetters,
      productGetters,
      search,
      getStatusTextClass,
      getSubmissionStatusTextClass
    };
  }
};
</script>
