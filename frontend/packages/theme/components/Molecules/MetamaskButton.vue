<template>
  <div class="wrapper">
    <SfButton type="button" class="color-secondary matamask-button form__element" v-if="!isConnected" @click="connectHandler" :disabled="disabled">
      {{ $t('Connect Metamask') }}
    </SfButton>
    <SfButton type="button" class="color-secondary matamask-button form__element" v-else @click="disconnectHandler" :disabled="disabled">
      {{ $t('Disconnect Metamask') }}
    </SfButton>
    <transition name="sf-fade">
      <div v-if="error.web3">
        {{ error.web3 }}
      </div>
    </transition>
  </div>
</template>

<script>
import { SfButton, SfImage } from '@storefront-ui/vue';
import { reactive } from '@vue/composition-api';

export default {
  name: 'MetamaskButton',

  components: {
    SfButton,
    SfImage
  },
  props: {
    disabled: {
      type: Boolean,
      default: false
    },
    isConnected: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    connectHandler() {
      this.$emit('click:connect');
    },
    disconnectHandler() {
      this.$emit('click:disconnect');
    }
  },
  // eslint-disable-next-line no-unused-vars,@typescript-eslint/explicit-module-boundary-types,@typescript-eslint/no-unused-vars
  setup(props, { emit }) {
    const error = reactive({
      web3: null
    });

    const resetErrorValues = () => {
      error.web3 = null;
    };

    return {
      error,
      resetErrorValues
    };
  }

};
</script>

<style lang="scss" scoped>
.matamask-button {
  padding-left: 60px;
  background-size: 100% 100%;
  background: var(--c-secondary) url('/icons/metamask-fox.svg') left;
  background-repeat:no-repeat;
};
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
};
</style>
