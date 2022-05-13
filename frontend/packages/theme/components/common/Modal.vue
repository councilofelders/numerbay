<template>
  <div :id="modalId" :ref="modalId" :data-bs-backdrop="backdrop" aria-hidden="true" class="modal fade" tabindex="-1">
    <div :class="modalClass" class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div v-if="$slots.title" class="modal-header">
          <h4 class="modal-title">
            <slot name="title"/>
          </h4>
          <button aria-label="Close" class="btn-close icon-btn" data-bs-dismiss="modal" type="button">
            <em class="ni ni-cross"></em>
          </button>
        </div>
        <div class="modal-body">
          <slot/>
        </div><!-- end modal-body -->
      </div><!-- end modal-content -->
    </div><!-- end modal-dialog -->
  </div><!-- end modal-->
</template>
<script>
export default {
  name: 'Modal',
  props: {
    modalId: {
      type: String,
      default: 'modal'
    },
    modalClass: {
      type: String,
      default: ''
    },
    backdrop: {
      default: true
    }
  },
  mounted() {
    this.$emit('registeredModal', this.getBootstrapModal(this.$refs[this.modalId]));
  }
};
</script>

<style lang="css" scoped>
</style>
