<template>
  <Modal :modal-id="modalId" modal-class="modal-lg" @registeredModal="modal = $event">
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
          <tr
            v-if="productGetters.getCategory(orderGetters.getProduct(order)).is_per_round && parseInt(orderGetters.getItemQty(order)) > 1">
            <th scope="row">
              Rounds
            </th>
            <td>{{
                `${orderGetters.getRound(order)}-${orderGetters.getEndRound(order)}`
              }}
            </td>
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
              From Address
            </th>
            <td><a :href="`https://etherscan.io/address/${orderGetters.getFromAddress(order)}`"
                   target="_blank">{{ orderGetters.getFromAddress(order) }}</a></td>
          </tr>
          <tr>
            <th scope="row">
              To Address
            </th>
            <td>
              <a :href="`https://etherscan.io/address/${orderGetters.getToAddress(order)}`"
                 target="_blank">{{ orderGetters.getToAddress(order) }}</a>
              <div v-if="withCopyButtons" class="d-flex align-items-center float-end">
                <div class="tooltip-s1">
                  <button v-clipboard:copy="orderGetters.getToAddress(order)" v-clipboard:success="onCopy"
                          class="copy-text ms-2" type="button">
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
              {{ orderGetters.getFormattedPrice(order, withCurrency = true, decimals = 4) }}
              <div v-if="withCopyButtons" class="d-flex align-items-center float-end">
                <div class="tooltip-s1">
                  <button v-clipboard:copy="JSON.stringify(orderGetters.getPrice(order))" v-clipboard:success="onCopy"
                          class="copy-text ms-2" type="button">
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
              <a v-if="orderGetters.getTransactionHash(order)"
                 :href="`https://etherscan.io/tx/${orderGetters.getTransactionHash(order)}`" target="_blank">
                        <span v-if="orderGetters.getTransactionHash(order).length > 25">
                          {{
                            `${orderGetters.getTransactionHash(order).slice(0, 12)}...${orderGetters.getTransactionHash(order).slice(-12, -1)}`
                          }}
                        </span>
                <span v-else>{{ orderGetters.getTransactionHash(order) }}</span>
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
              Stake Limit
            </th>
            <td>{{ orderGetters.getStakeLimit(order) }}</td>
          </tr>
          <tr>
            <th scope="row">
              Auto-Submit Model
            </th>
            <td v-if="!modelChanging">{{ orderGetters.getSubmitModelName(order) }}<span v-if="withChangeModelButton"
                                                                                        class="d-flex align-items-center float-end"><a
              class="btn-link text-primary" @click="toggleModelChange(true)"
              href="javascript:void(0);">Change</a></span></td>
            <td v-else>
              <ValidationObserver v-slot="{ handleSubmit }">
                <div class="row">
                  <div class="col-10">
                    <ValidationProvider v-slot="{ errors }" rules="required" slim>
                      <div>
                        <v-select v-if="!numeraiLoading" ref="slotDropdown"
                                  v-model="submitModel" :class="!errors[0] ? '' : 'is-invalid'" :clearable=true
                                  :options="userGetters.getModels(numerai, tournamentId, false)"
                                  :reduce="model => model.id"
                                  class="generic-select generic-select-s1" label="name"></v-select>
                        <div v-else><span class="spinner-border spinner-border-sm" role="status"></span> Loading models
                        </div>
                        <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                      </div>
                    </ValidationProvider>
                  </div>
                  <div class="col-2">
                    <a class="btn btn-link text-primary d-flex align-items-center float-end"
                       @click="handleSubmit(applyModelChange)" href="javascript:void(0);"
                       :class="(userOrderLoading || numeraiLoading) ? `disabled`: ``">Apply</a>
                  </div>
                </div>
              </ValidationObserver>
            </td>
          </tr>
          <tr v-if="orderGetters.getStatus(order) === 'confirmed'">
            <th scope="row">
              Auto-Submit Status
            </th>
            <td>{{ orderGetters.getSubmissionStatus(order) }}</td>
          </tr>
          <tr v-if="orderGetters.getStatus(order) === 'confirmed'">
            <th scope="row">
              Last Auto-Submit Round
            </th>
            <td>{{ orderGetters.getLastSubmissionRound(order) }}</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Modal><!-- end modal-->
</template>
<script>
// Composables
import {orderGetters, productGetters, userGetters, useNumerai, useUserOrder} from '@vue-storefront/numerbay';
import {useUiNotification} from '~/composables';
import updateOrderSubmissionModel from "../../../api-client/src/api/updateOrderSubmissionModel";

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
    withChangeModelButton: {
      type: Boolean,
      default: false
    },
    order: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      modal: null,
      modelChanging: false,
      submitModel: null,
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
    },
    async toggleModelChange(value) {
      if (value) {
        this.modelChanging = true;
        await this.getModels().catch((e) => {
          this.send({
            message: e?.message,
            type: 'bg-danger',
            icon: 'ni-alert-circle',
            persist: true,
            action: {
              text: 'Change Numerai API Key',
              onClick: async () => {
                await this.$router.push('/numerai-settings');
              }
            }
          });
        });
      } else {
        this.modelChanging = false;
      }
    },
    async applyModelChange() {
      // this.modelChanging = false
      await this.updateOrderSubmissionModel({orderId: this.order?.id, modelId: this.submitModel});
      if (this.userOrderError?.updateOrderSubmissionModel) {
        this.send({
          message: this.userOrderError?.updateOrderSubmissionModel?.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle',
          persist: true,
          action: {
            text: 'Change Numerai API Key',
            onClick: async () => {
              await this.$router.push('/numerai-settings');
            }
          }
        });
      }
      this.$emit('update');
      await this.toggleModelChange(false);
    }
  },
  computed: {
    tournamentId() {
      return this.order?.product?.category?.tournament;
    }
  },
  beforeDestroy() {
    this.modal?.hide();
  },
  setup() {
    const {numerai, getModels, loading: numeraiLoading} = useNumerai('order-info');
    const {updateOrderSubmissionModel, loading: userOrderLoading, error: userOrderError} = useUserOrder('order-info');
    const {send} = useUiNotification();

    const onCopy = (e) => {
      const target = e.trigger.querySelector('.tooltip-text');
      const prevText = target.innerHTML;
      target.innerHTML = 'Copied';
      setTimeout(function () {
        target.innerHTML = prevText;
      }, 1000);
    };

    return {
      orderGetters,
      productGetters,
      userGetters,
      onCopy,
      numerai,
      getModels,
      numeraiLoading,
      updateOrderSubmissionModel,
      userOrderLoading,
      userOrderError,
      send
    };
  }
};
</script>

<style lang="css" scoped>
</style>
