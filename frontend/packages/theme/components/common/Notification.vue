<template>
  <transition-group tag="div" class="notifications" name="slide-fade">
    <div class="toast align-items-center text-white border-0 show my-3" :class="notification.type" role="alert"
         aria-live="assertive" aria-atomic="true"
         v-for="notification in notifications"
         :key="notification.id"
    >
      <div class="d-flex">
        <div class="toast-body">
          <span class="ni mx-1" :class="notification.icon"
                v-if="Boolean(notification.icon)"></span>{{ notification.message }}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"
                aria-label="Close"></button>
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

<style scoped lang="scss">
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
