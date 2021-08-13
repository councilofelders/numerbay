<template>
  <div class="wrapper">
    <SfButton class="color-secondary matamask-button form__element" v-if="!web3User.isConnected" @click="connectWeb3Modal">
      {{ $t('Connect Metamask') }}
    </SfButton>
    <SfButton class="color-secondary matamask-button form__element" v-else @click="disconnectWeb3Modal">
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
import { useUser } from '@vue-storefront/numerbay';
import { reactive } from '@vue/composition-api';
import {Logger} from '@vue-storefront/core';

export default {
  name: 'MetamaskButton',

  components: {
    SfButton,
    SfImage
  },

  props: {
    valid: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    activeAccount() {
      return this.web3User.activeAccount;
    }
  },
  watch: {
    activeAccount: {
      // avoid emitting event during load
      immediate: false,
      // eslint-disable-next-line func-names,no-unused-vars,@typescript-eslint/no-unused-vars
      handler: function (publicAddress) {
        Logger.debug('on publicAddressChange: ', publicAddress);
        // emit event if publicAddress is cleared or changed to a different value
        if ((!publicAddress) || publicAddress !== localStorage.getItem('cachedPublicAddress')) {
          this.$emit('publicAddressChange', publicAddress, this.web3User.providerEthers, (err, signature)=>{
            if (err) {
              this.error.web3 = 'You need to sign the message.';
              this.disconnectWeb3Modal();
            } else {
              this.resetErrorValues();
              Logger.debug('Web3 signature: ', signature);
            }
          });
        }
      }
    }
  },
  created() {
    this.initWeb3Modal();
    this.ethereumListener();
  },
  // eslint-disable-next-line no-unused-vars,@typescript-eslint/explicit-module-boundary-types,@typescript-eslint/no-unused-vars
  setup(props, { emit }) {
    const error = reactive({
      web3: null
    });

    const resetErrorValues = () => {
      error.web3 = null;
    };

    const { web3User, initWeb3Modal, ethereumListener, connectWeb3Modal, disconnectWeb3Modal } = useUser();

    return {
      web3User,
      error,
      initWeb3Modal,
      ethereumListener,
      connectWeb3Modal,
      disconnectWeb3Modal,
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
