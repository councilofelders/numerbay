<template>
  <div class="col-lg-8">
    <div class="user-panel-title-box">
      <div class="d-flex">
        <h3>Purchases</h3>
        <button class="icon-btn ms-auto" title="Refresh" :disabled="loading" @click="refresh">
          <em class="ni ni-reload" v-if="!loading"></em><span class="spinner-border spinner-border-sm" role="status"
                                                              v-else></span>
        </button>
      </div>
    </div><!-- end user-panel-title-box -->
    <div v-if="!displayedOrders || displayedOrders.length === 0">You have not made any purchase</div>
    <div class="profile-setting-panel-wrap" v-else>
        <ul class="nav nav-tabs nav-tabs-s3 mb-2" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link" :class="'active'" :id="'all'" type="button">All purchases</button>
            </li>
        </ul>
        <div class="tab-content mt-4 tab-content-desktop">
            <div class="tab-pane fade show active" role="tabpanel" aria-labelledby="all-tab">
                <div class="activity-tab-wrap">
                    <div class="card card-creator-s1 mb-4" v-for="order in displayedOrders" :key="order.id">
                        <div class="card-body d-flex align-items-center">
                            <div class="card-media-img flex-shrink-0">
                                <img :src="productGetters.getCoverImage(orderGetters.getProduct(order))" alt="avatar">
                            </div>
                            <div class="flex-grow-1">
                                <h6 class="card-s1-title">
                                  <router-link class="btn-link"
                                               :to="`/product/${productGetters.getCategory(orderGetters.getProduct(order)).slug}/${productGetters.getName(orderGetters.getProduct(order))}`">
                                    {{ productGetters.getName(orderGetters.getProduct(order)).toUpperCase() }}</router-link>
                                </h6>
                                <p class="card-s1-text">
                                  <span>
                                    <span class="btn-link text-decoration-none fw-medium">
                                      {{ productGetters.getCategory(orderGetters.getProduct(order)).slug }}
                                    </span> {{ orderGetters.getMode(order) }} x {{ orderGetters.getItemQty(order) }} for round
                                    <span class="btn-link text-decoration-none fw-medium">{{ orderGetters.getRound(order) }}</span><span class="btn-link text-decoration-none fw-medium"
                                          v-if="productGetters.getCategory(orderGetters.getProduct(order)).is_per_round && parseInt(orderGetters.getItemQty(order)) > 1"
                                    >-{{ parseInt(orderGetters.getRound(order)) + parseInt(orderGetters.getItemQty(order)) - 1 }}
                                    </span> by
                                    <span class="btn-link text-decoration-none fw-medium">{{ orderGetters.getBuyer(order) }}</span>
                                    <span> for <span class="btn-link text-decoration-none fw-medium">{{ orderGetters.getFormattedPrice(order, withCurrency = true, decimals = 4) }}</span></span>
                                  </span>
                                </p>
                                <p class="card-s1-text">{{ orderGetters.getDate(order) }}</p>
                                <p class="card-s1-text">
                                  <span class="badge fw-medium" :class="getStatusTextClass(order)">{{ orderGetters.getStatus(order) }}</span>
                                  <a href="javascript:void(0);" @click="toggleInfoModal(order)" title="Click for details" class="ms-2 text-secondary">View details</a>
                                  <a href="javascript:void(0);" @click="toggleArtifactModal(order)" title="Click for files" class="ms-2 text-primary" v-if="orderGetters.getStatus(order)=='confirmed'">Download</a>
                                </p>
                            </div>
                        </div>
                    </div><!-- end card -->
                </div><!-- end activity-tab-wrap -->
                <!-- pagination -->
                <div class="text-center mt-4 mt-md-5">
                  <Pagination :records="orders.length" v-model="page" :per-page="perPage"></Pagination>
                </div>
            </div><!-- end tab-pane -->
        </div><!-- end tab-content -->
    </div><!-- end profile-setting-panel-wrap-->
    <OrderInfoModal :order="currentOrder" modelId="orderInfoModal" ref="orderInfoModal"
                    :withCopyButtons="true"></OrderInfoModal>
    <div v-if="currentOrder && currentOrder.product">
      <ArtifactModal :order="currentOrder" :encryptedPrivateKey="user.encrypted_private_key"
                     :publicKey="user.public_key" modelId="artifactModal" ref="artifactModal"></ArtifactModal>
    </div>
  </div><!-- end col-lg-8 -->
</template>

<script>
import ArtifactModal from "~/components/section/ArtifactModal";
import OrderInfoModal from "~/components/section/OrderInfoModal";
import Pagination from 'vue-pagination-2';

// Composables
import {onSSR} from '@vue-storefront/core';
import {computed} from '@vue/composition-api';
import {orderGetters, productGetters, useUser, useUserOrder} from '@vue-storefront/numerbay';

export default {
  name: 'PurchasesSection',
  components: {
    ArtifactModal,
    OrderInfoModal,
    Pagination
  },
  data() {
    return {
      page: 1,
      perPage: 10,
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
    },
    refresh() {
      this.search({role: 'buyer'});
    }
  },
  mounted() {
    this.orderPollingTimer = setInterval(async () => {
      await this.search({role: 'buyer'});
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
    const {user} = useUser();
    const {orders, search, loading} = useUserOrder('order-history');

    onSSR(async () => {
      await search({role: 'buyer'});
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

    return {
      orders: computed(() => orders?.value?.data ? orders.value?.data : []),
      loading,
      user,
      orderGetters,
      productGetters,
      search,
      getStatusTextClass,
    };
  }
};
</script>
