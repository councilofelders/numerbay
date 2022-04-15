<template>
  <div class="modal fade" :id="modalId" :ref="modalId" tabindex="-1" aria-hidden="true" :data-bs-backdrop="backdrop">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" :class="modalClass">
      <div class="modal-content">
        <div v-if="$slots.title" class="modal-header">
          <h4 class="modal-title">
            <slot name="title"/>
          </h4>
          <button type="button" class="btn-close icon-btn" data-bs-dismiss="modal" aria-label="Close">
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
