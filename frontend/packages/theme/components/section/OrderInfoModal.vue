<template>
    <Modal :modal-id="modalId" @registeredModal="modal = $event" modal-class="modal-lg">
      <template slot="title">Order Details</template>
      <div class="row g-2">
        <div class="col-xl-12">
          <table class="table mb-0 table-s1">
            <tbody>
                <tr>
                    <th scope="row">
                        Order ID
                    </th>
                    <td>{{ orderGetters.getId(order) }}</td>
                </tr>
                <tr>
                    <th scope="row">
                        Product
                    </th>
                    <td>{{ orderGetters.getItemSku(orderGetters.getProduct(order)) }}</td>
                </tr>
                <tr v-if="productGetters.getCategory(orderGetters.getProduct(order)).is_per_round && parseInt(orderGetters.getItemQty(order)) > 1">
                    <th scope="row">
                        Rounds
                    </th>
                    <td>{{ `${orderGetters.getRound(order)}-${parseInt(orderGetters.getRound(order))+parseInt(orderGetters.getItemQty(order))-1}` }}</td>
                </tr>
                <tr v-else>
                    <th scope="row">
                        Round
                    </th>
                    <td>{{ orderGetters.getRound(order) }}</td>
                </tr>
                <tr>
                    <th scope="row">
                        Date
                    </th>
                    <td>{{ orderGetters.getDate(order) }}</td>
                </tr>
                <tr>
                    <th scope="row">
                        Buyer
                    </th>
                    <td>{{ orderGetters.getBuyer(order) }}</td>
                </tr>
                <tr>
                    <th scope="row">
                        Submit to Model
                    </th>
                    <td>{{ orderGetters.getSubmitModelName(order) }}</td>
                </tr>
                <tr>
                    <th scope="row">
                        From Address
                    </th>
                  <td><a :href="`https://etherscan.io/address/${orderGetters.getFromAddress(order)}`" target="_blank">{{ orderGetters.getFromAddress(order) }}</a></td>
                </tr>
                <tr>
                    <th scope="row">
                        To Address
                    </th>
                    <td>
                      <a :href="`https://etherscan.io/address/${orderGetters.getToAddress(order)}`" target="_blank">{{ orderGetters.getToAddress(order) }}</a>
                      <div class="d-flex align-items-center float-end" v-if="withCopyButtons">
                          <div class="tooltip-s1">
                              <button v-clipboard:copy="orderGetters.getToAddress(order)" v-clipboard:success="onCopy" class="copy-text ms-2" type="button">
                                  <span class="tooltip-s1-text tooltip-text">Copy</span>
                                  <em class="ni ni-copy"></em>
                              </button>
                          </div>
                      </div>
                    </td>
                </tr>
                <tr>
                    <th scope="row">
                        Total
                    </th>
                    <td>
                      {{ orderGetters.getFormattedPrice(order, withCurrency=true, decimals=4) }}
                      <div class="d-flex align-items-center float-end" v-if="withCopyButtons">
                          <div class="tooltip-s1">
                              <button v-clipboard:copy="JSON.stringify(orderGetters.getPrice(order))" v-clipboard:success="onCopy" class="copy-text ms-2" type="button">
                                  <span class="tooltip-s1-text tooltip-text">Copy</span>
                                  <em class="ni ni-copy"></em>
                              </button>
                          </div>
                      </div>
                    </td>
                </tr>
                <tr>
                    <th scope="row">
                        Transaction Hash
                    </th>
                    <td>
                      <a v-if="orderGetters.getTransactionHash(order)" :href="`https://etherscan.io/tx/${orderGetters.getTransactionHash(order)}`" target="_blank">
                        <span v-if="orderGetters.getTransactionHash(order).length > 25">
                          {{ `${orderGetters.getTransactionHash(order).slice(0, 12)}...${orderGetters.getTransactionHash(order).slice(-12, -1)}` }}
                        </span>
                        <span v-else>{{orderGetters.getTransactionHash(order)}}</span>
                      </a>
                      <span v-else>waiting</span>
                    </td>
                </tr>
                <tr>
                    <th scope="row">
                        Order Status
                    </th>
                    <td>{{ orderGetters.getStatus(order) }}</td>
                </tr>
                <tr v-if="orderGetters.getStatus(order) === 'confirmed'">
                    <th scope="row">
                        Submission Status
                    </th>
                    <td>{{ orderGetters.getSubmissionStatus(order) }}</td>
                </tr>
                <tr v-if="orderGetters.getStatus(order) === 'confirmed'">
                    <th scope="row">
                        Stake Limit
                    </th>
                    <td>{{ orderGetters.getStakeLimit(order) }}</td>
                </tr>
            </tbody>
          </table>
        </div>
      </div>
  </Modal><!-- end modal-->
</template>
<script>
// Composables
import { orderGetters, productGetters } from '@vue-storefront/numerbay';

export default {
  name: 'OrderInfoModal',
  props: {
    modalId: {
      type: String,
      default: 'orderInfoModal'
    },
    withCopyButtons: {
      type: Boolean,
      default: false
    },
    order: {
      type: Object,
      default: () =>({})
    }
  },
  data() {
    return {
      modal: null
    };
  },
  methods: {
    show() {
      this.modal?.show();
    },
    hide() {
      this.modal?.hide();
    },
    getMetricColor(value) {
      if (value > 0) {
        return 'success';
      } else if (value < 0) {
        return 'danger';
      } else {
        return '';
      }
    }
  },
  beforeDestroy() {
    this.modal?.hide();
  },
  setup() {
    const onCopy = (e) => {
      const target = e.trigger.querySelector('.tooltip-text');
      const prevText = target.innerHTML;
      target.innerHTML = 'Copied';
      setTimeout(function() {
        target.innerHTML = prevText;
      }, 1000);
    };

    return {
      orderGetters,
      productGetters,
      onCopy
    };
  }
};
</script>

<style lang="css" scoped>
</style>
