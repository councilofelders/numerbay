<template>
  <div class="col-lg-8">
    <div class="user-panel-title-box">
      <div class="d-flex">
        <h3>Purchases</h3>
        <button :disabled="loading" class="icon-btn ms-auto" title="Refresh" @click="refresh">
          <em v-if="!loading" class="ni ni-reload"></em><span v-else class="spinner-border spinner-border-sm"
                                                              role="status"></span>
        </button>
      </div>
    </div><!-- end user-panel-title-box -->
    <div v-if="!orders || orders.length === 0">You have not made any purchase</div>
    <div v-else class="profile-setting-panel-wrap">
      <div class="row">
        <div class="col-9">
          <ul class="nav nav-tabs nav-tabs-s3 mb-2" role="tablist">
            <li class="nav-item" role="presentation">
              <button :id="'active'" :class="'active'" class="nav-link" type="button">Active purchases</button>
            </li>
          </ul>
        </div>
        <div class="col-3">
          <a class="float-end" href="javascript:void(0);" @click="downloadOrders">Export CSV</a>
        </div>
      </div>
      <div class="tab-content mt-4 tab-content-desktop">
        <div aria-labelledby="all-tab" class="tab-pane fade show active" role="tabpanel">
          <div class="activity-tab-wrap">
            <div v-for="order in ActiveOrders" :key="order.id" class="card card-creator-s1 mb-4">
              <div class="card-body d-flex align-items-center">
                <div class="card-media-img flex-shrink-0">
                  <img :src="productGetters.getCoverImage(orderGetters.getProduct(order))" alt="avatar">
                </div>
                <div class="flex-grow-1">
                  <h6 class="card-s1-title">
                    <router-link
                      :to="`/product/${productGetters.getCategory(orderGetters.getProduct(order)).slug}/${productGetters.getName(orderGetters.getProduct(order))}`"
                      class="btn-link">
                      {{ productGetters.getName(orderGetters.getProduct(order)).toUpperCase() }}
                    </router-link>
                  </h6>
                  <p class="card-s1-text">
                    <span>
                      <span class="btn-link text-decoration-none fw-medium">
                        {{ productGetters.getCategory(orderGetters.getProduct(order)).slug }}
                      </span> {{ orderGetters.getMode(order) }} x {{ orderGetters.getItemQty(order) }} for round
                      <span class="btn-link text-decoration-none fw-medium">{{
                          orderGetters.getRound(order)
                        }}</span><span
                      v-if="productGetters.getCategory(orderGetters.getProduct(order)).is_per_round && parseInt(orderGetters.getItemQty(order)) > 1"
                      class="btn-link text-decoration-none fw-medium"
                    >-{{
                        orderGetters.getEndRound(order)
                      }}
                      </span> by
                      <span class="btn-link text-decoration-none fw-medium">{{
                          orderGetters.getBuyer(order)
                        }}</span>
                      <span> for <span class="btn-link text-decoration-none fw-medium">{{
                          orderGetters.getFormattedPrice(order, withCurrency = true, decimals = 4)
                        }}</span></span>
                    </span>
                  </p>
                  <p class="card-s1-text">{{ orderGetters.getDate(order) }}</p>
                  <p class="card-s1-text">
                    <span :class="getStatusTextClass(order)" class="badge fw-medium">{{
                        orderGetters.getStatus(order)
                      }}</span>
                    <a class="ms-2 text-secondary" href="javascript:void(0);" title="Click for details"
                       @click="toggleInfoModal(order)">View details</a>
                    <a v-if="orderConfirmed(order)" class="ms-2 text-primary"
                       href="javascript:void(0);"
                       title="Click for files" @click="toggleArtifactModal(order)">Download</a>
                    <a v-if="orderPending(order)" class="ms-2 text-danger"
                       href="javascript:void(0);"
                       title="Cancel this order" @click="handleCancelOrder(order)">Cancel</a>
                  </p>
                </div>
              </div>
            </div><!-- end card -->
          </div><!-- end activity-tab-wrap -->
        </div><!-- end tab-pane -->
      </div><!-- end tab-content -->
      <div class="row mt-5">
        <div class="col-12">
          <ul class="nav nav-tabs nav-tabs-s3 mb-2" role="tablist">
            <li class="nav-item" role="presentation">
              <button :id="'past'" class="nav-link" type="button">Past purchases</button>
            </li>
          </ul>
        </div>
      </div>
      <div class="tab-content mt-4 tab-content-desktop">
        <div aria-labelledby="all-tab" class="tab-pane fade show active" role="tabpanel">
          <div class="activity-tab-wrap">
            <div v-for="order in displayedPastOrders" :key="order.id" class="card card-creator-s1 mb-4">
              <div class="card-body d-flex align-items-center">
                <div class="card-media-img flex-shrink-0">
                  <img :src="productGetters.getCoverImage(orderGetters.getProduct(order))" alt="avatar">
                </div>
                <div class="flex-grow-1">
                  <h6 class="card-s1-title">
                    <router-link
                      :to="`/product/${productGetters.getCategory(orderGetters.getProduct(order)).slug}/${productGetters.getName(orderGetters.getProduct(order))}`"
                      class="btn-link">
                      {{ productGetters.getName(orderGetters.getProduct(order)).toUpperCase() }}
                    </router-link>
                  </h6>
                  <p class="card-s1-text">
                    <span>
                      <span class="btn-link text-decoration-none fw-medium">
                        {{ productGetters.getCategory(orderGetters.getProduct(order)).slug }}
                      </span> {{ orderGetters.getMode(order) }} x {{ orderGetters.getItemQty(order) }} for round
                      <span class="btn-link text-decoration-none fw-medium">{{
                          orderGetters.getRound(order)
                        }}</span><span
                      v-if="productGetters.getCategory(orderGetters.getProduct(order)).is_per_round && parseInt(orderGetters.getItemQty(order)) > 1"
                      class="btn-link text-decoration-none fw-medium"
                    >-{{
                        orderGetters.getEndRound(order)
                      }}
                      </span> by
                      <span class="btn-link text-decoration-none fw-medium">{{
                          orderGetters.getBuyer(order)
                        }}</span>
                      <span> for <span class="btn-link text-decoration-none fw-medium">{{
                          orderGetters.getFormattedPrice(order, withCurrency = true, decimals = 4)
                        }}</span></span>
                    </span>
                  </p>
                  <p class="card-s1-text">{{ orderGetters.getDate(order) }}</p>
                  <p class="card-s1-text">
                    <span :class="getStatusTextClass(order)" class="badge fw-medium">{{
                        orderGetters.getStatus(order)
                      }}</span>
                    <a class="ms-2 text-secondary" href="javascript:void(0);" title="Click for details"
                       @click="toggleInfoModal(order)">View details</a>
                    <a v-if="orderConfirmed(order)" class="ms-2 text-primary"
                       href="javascript:void(0);"
                       title="Click for files" @click="toggleArtifactModal(order)">Download</a>
                    <a v-if="orderConfirmed(order)" class="ms-2 text-danger float-end"
                       href="javascript:void(0);"
                       title="Send email to request a refund" @click="toggleRefundModal(order)">Refund</a>
                  </p>
                </div>
              </div>
            </div><!-- end card -->
          </div><!-- end activity-tab-wrap -->
          <!-- pagination -->
          <div class="text-center mt-4 mt-md-5">
            <Pagination v-model="page" :per-page="perPage" :records="pastOrders.length"></Pagination>
          </div>
        </div><!-- end tab-pane -->
      </div><!-- end tab-content -->
    </div><!-- end profile-setting-panel-wrap-->
    <OrderInfoModal ref="orderInfoModal" :order="currentOrder" :withCopyButtons="true" :withChangeModelButton="true"
                    modelId="orderInfoModal" @update="refresh"></OrderInfoModal>
    <div v-if="currentOrder && currentOrder.product">
      <ArtifactModal ref="artifactModal"
                     :publicKey="user.public_key" :encryptedPrivateKey="user.encrypted_private_key"
                     :publicKeyV2="user.public_key_v2" :encryptedPrivateKeyV2="user.encrypted_private_key_v2"
                     :order="currentOrder" modelId="artifactModal"></ArtifactModal>
      <RefundModal ref="refundModal" :order="currentOrder" modelId="refundModal"></RefundModal>
    </div>
  </div><!-- end col-lg-8 -->
</template>

<script>
import ArtifactModal from "~/components/section/ArtifactModal";
import RefundModal from "~/components/section/RefundModal";
import OrderInfoModal from "~/components/section/OrderInfoModal";
import Pagination from 'vue-pagination-2';
import _ from 'lodash';

// Composables
import {onSSR} from '@vue-storefront/core';
import {computed} from '@vue/composition-api';
import {orderGetters, productGetters, useGlobals, useUser, useUserOrder} from '@vue-storefront/numerbay';

export default {
  name: 'PurchasesSection',
  components: {
    ArtifactModal,
    RefundModal,
    OrderInfoModal,
    Pagination
  },
  data() {
    return {
      page: 1,
      perPage: 6,
      currentOrder: {}
    };
  },
  computed: {
    pastOrders() {
      return _.orderBy(this.orders?.filter(o => (parseInt(this.orderGetters.getEndRound(o)) < this.globals?.selling_round) || (this.orderGetters.getStatus(o) === 'expired')), 'date_order', 'desc');
    },
    displayedPastOrders() {
      const startIndex = this.perPage * (this.page - 1);
      const endIndex = startIndex + this.perPage;
      return this.pastOrders?.slice(startIndex, endIndex);
    },
    ActiveOrders() {
      return _.orderBy(this.orders?.filter(o => (parseInt(this.orderGetters.getEndRound(o)) >= this.globals?.selling_round) && (this.orderGetters.getStatus(o) !== 'expired')), 'date_order', 'desc');
    }
  },
  methods: {
    orderPending(order) {
      return this.orderGetters.getStatus(order)==='pending';
    },
    orderConfirmed(order) {
      return this.orderGetters.getStatus(order)==='confirmed';
    },
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
    toggleRefundModal(order) {
      this.currentOrder = order;
      this.$nextTick(() => {
        this.$refs.refundModal.show();
      });
    },
    async handleCancelOrder(order) {
      await this.cancelOrder({orderId: order?.id});
      await this.refresh();
    },
    async refresh() {
      await this.search({role: 'buyer'});
      if (this.currentOrder?.id) {
        this.currentOrder = this.orders.filter((o) => o.id === this.currentOrder.id)[0];
      }
    }
  },
  mounted() {
    this.orderPollingTimer = setInterval(async () => {
      await this.refresh();
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
    const {orders, search, cancelOrder, loading} = useUserOrder('order-history');
    const {globals} = useGlobals();

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
      globals,
      orders: computed(() => orders?.value?.data ? orders.value?.data : []),
      loading,
      user,
      orderGetters,
      productGetters,
      search,
      getStatusTextClass,
      downloadOrders,
      cancelOrder,
    };
  }
};
</script>
