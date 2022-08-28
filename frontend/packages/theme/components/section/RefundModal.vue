<template>
  <Modal :modal-id="modalId" modal-class="modal-lg" @registeredModal="modal = $event">
    <template slot="title">Request Refund for Order {{ order.id }}</template>
    <div class="row g-2">
      <div class="col-xl-12">
        <ValidationObserver key="refund" v-slot="{ handleSubmit }">
          <div class="row">
            <ValidationProvider v-slot="{ errors }" rules="required" slim>
              <div class="col-lg-12 mb-3">
                <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label" for="wallet">Wallet to receive refund</label>
                <input id="wallet" v-model="form.wallet" :class="!errors[0] ? '' : 'is-invalid'"
                       class="form-control form-control-s1" type="text">
                <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
              </div><!-- end col -->
            </ValidationProvider>
            <ValidationProvider v-slot="{ errors }" rules="" slim>
              <div class="col-lg-12 mb-3">
                <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label" for="contact">Contact method</label>
                <input id="contact" v-model="form.contact" :class="!errors[0] ? '' : 'is-invalid'"
                       class="form-control form-control-s1" type="text" placeholder="E.g. email address or RochetChat link">
                <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
              </div><!-- end col -->
            </ValidationProvider>
            <ValidationProvider v-slot="{ errors }" rules="" slim>
              <div class="col-lg-12 mb-3">
                <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label" for="message">Message</label>
                <input id="message" v-model="form.message" :class="!errors[0] ? '' : 'is-invalid'"
                       class="form-control form-control-s1" type="text" placeholder="Short message to describe the situation">
                <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
              </div><!-- end col -->
            </ValidationProvider>
          </div><!-- end row -->
          <button :disabled="orderLoading" class="btn btn-dark mt-3 d-flex justify-content-center"
                  type="button" @click="handleSubmit(handleSendRefundRequest)">
            <span v-if="orderLoading"><span class="spinner-border spinner-border-sm me-2" role="status"></span>Sending...</span>
            <span v-else>Send Request</span>
          </button>
        </ValidationObserver>
      </div>
    </div>
  </Modal><!-- end modal-->
</template>
<script>
// Composables
import {useUserOrder} from '@vue-storefront/numerbay';
import {useUiNotification} from '~/composables';

export default {
  name: 'RefundModal',
  props: {
    modalId: {
      type: String,
      default: 'refundModal'
    },
    order: {
      type: Object,
      default: () => ({})
    },
    publicKey: {
      type: String,
      default: null
    },
    encryptedPrivateKey: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      modal: null,
      form: {}
    };
  },
  methods: {
    show() {
      this.modal?.show();
    },
    hide() {
      this.modal?.hide();
    },
    async handleSendRefundRequest() {
      await this.sendRefundRequest({orderId: this.order.id, wallet: this.form.wallet, contact: this.form.contact, message: this.form.message});
      if (this.orderError.sendRefundRequest) {
        this.send({
          message: this.orderError.sendRefundRequest.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
      } else {
        this.send({
          message: 'Request sent',
          type: 'bg-success',
          icon: 'ni-check'
        });
        this.hide()
      }
    }
  },
  beforeDestroy() {
    this.modal?.hide();
  },
  setup(props) {
    const {sendRefundRequest, loading: orderLoading, error: orderError} = useUserOrder(`${props.order.id}`);
    const {send} = useUiNotification();

    return {
      sendRefundRequest,
      orderLoading,
      orderError,
      send
    };
  }
};
</script>

<style lang="css" scoped>
</style>
