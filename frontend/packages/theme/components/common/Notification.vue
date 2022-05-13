<template>
  <transition-group class="notifications" name="slide-fade" tag="div">
    <div v-for="notification in notifications" :key="notification.id" :class="notification.type"
         aria-atomic="true" aria-live="assertive"
         class="toast align-items-center text-white border-0 show my-3"
         role="alert"
    >
      <div class="d-flex">
        <span v-if="Boolean(notification.icon)" :class="notification.icon"
              class="mx-1 m-auto ni fs-12"></span>
        <div class="toast-body">
          {{ notification.message }}
          <div v-if="Boolean(notification.action) && Boolean(notification.action.text)">
            <a class="btn-link fw-regular text-white" type="button"
               @click="notification.action.onClick()">{{ notification.action.text }}</a>
          </div>
        </div>
        <button aria-label="Close" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"
                type="button"></button>
      </div>
    </div>
  </transition-group>
</template>

<script>
import {useUiNotification} from '~/composables';

export default {
  name: 'Notification',
  setup() {
    const {notifications} = useUiNotification();
    return {
      notifications
    };
  }
};
</script>

<style lang="scss" scoped>
.notifications {
  position: fixed;
  width: 100%;
  left: 0;
  bottom: 0;
  right: 0;
  z-index: 10000;
  top: 100px;
  left: auto;
  bottom: auto;
  right: 5%;
  width: 320px;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s;
  transition: opacity 0.25s linear;
}

.slide-fade-enter {
  transform: translateY(40px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(80px);
  opacity: 0;
}
</style>
