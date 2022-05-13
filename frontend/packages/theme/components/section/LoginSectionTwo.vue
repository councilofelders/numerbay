<template>
  <section class="login-section section-space-b pt-4 pt-md-5 mt-md-3">
    <div class="container">
      <div class="row ">
        <div class="col-lg-8 col-xl-6 mx-auto">
          <ul id="myTab" class="row g-gs nav nav-tabs nav-tabs-s2 justify-content-center" role="tablist">
            <li class="nav-item col-sm-6 col-6" role="presentation">
              <button id="meta-mask-tab" class="nav-link active" data-bs-target="#meta-mask" data-bs-toggle="tab"
                      type="button">
                <img :src="require('@/images/brand/metamask.svg')" alt="" class="icon icon-svg">
                <span class="nav-link-title mt-2 mt-sm-3 d-block">MetaMask</span>
              </button>
            </li>
            <li v-if="!authenticated" class="nav-item col-sm-6 col-6" role="presentation">
              <button id="wallet-connect-tab" class="nav-link" data-bs-target="#wallet-connect" data-bs-toggle="tab"
                      type="button">
                <img :src="require('@/images/thumb/icon-users.svg')" alt="" class="icon icon-svg">
                <span class="nav-link-title mt-2 mt-sm-3 d-block">Username (Legacy)</span>
              </button>
            </li>
          </ul>
          <div class="gap-2x"></div><!-- end gap -->
          <div id="myTabContent" class="tab-content">
            <div id="meta-mask" aria-labelledby="meta-mask-tab" class="tab-pane fade show active" role="tabpanel">
              <div class="card-media card-media-s3 text-center">
                <div class="card-media-body">
                  <h3 class="mb-4">{{ SectionData.loginDataTwo.title }}</h3>
                  <button :disabled="connecting" class="btn btn-dark" @click="onWalletConnect">
                    <span v-if="connecting"><span class="spinner-border spinner-border-sm me-2" role="status"></span>Connecting...</span>
                    <span v-else>Connect</span>
                  </button>
                  <p v-if="SectionData.loginDataTwo.btnTextLink" class="mt-3"><a
                    :href="SectionData.loginDataTwo.btnTextLink" class=" fs-13 btn-link fw-regular"
                    target="_blank">{{ SectionData.loginDataTwo.btnTextTwo }}</a></p>
                </div>
              </div><!-- end card-media -->
            </div><!-- end tab-pane -->
            <div id="wallet-connect" aria-labelledby="wallet-connect-tab" class="tab-pane fade" role="tabpanel">
              <div class="card-media card-media-s3 text-center">
                <div class="card-media-body">
                  <h3 class="mb-4">{{ SectionData.loginDataTwo.titleTwo }}</h3>
                  <router-link :to="SectionData.loginDataTwo.btnLink" class="btn btn-dark">
                    {{ SectionData.loginDataTwo.btnTextFour }}
                  </router-link>
                  <p v-if="SectionData.loginDataTwo.btnTextLinkTwo" class="mt-3">
                    <router-link :to="SectionData.loginDataTwo.btnTextLinkTwo" class=" fs-13 btn-link fw-regular"
                                 target="_blank">{{ SectionData.loginDataTwo.btnTextThree }}
                    </router-link>
                  </p>
                </div>
              </div><!-- end card-media -->
            </div><!-- end tab-pane -->
          </div><!-- end tab-content -->
        </div><!-- end col-lg-7 -->
      </div><!-- end row -->
    </div><!-- end container -->
  </section><!-- end login-section -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

// Composables
import {useUser} from '@vue-storefront/numerbay';
import {useUiNotification} from '~/composables';

export default {
  name: 'LoginSectionTwo',
  data() {
    return {
      SectionData,
      connecting: false
    };
  },
  props: {
    authenticated: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    async onWalletConnect() {
      try {
        this.connecting = true;
        await this.$wallet.connect().then(async () => {
          const publicAddress = this.$wallet.account;
          if (this.authenticated) {
            await this.getNonceAuthenticated();
          } else {
            await this.getNonce({publicAddress: publicAddress});
          }
          const {nonce} = this.web3User.nonce;
          const signer = this.$wallet.provider.getSigner();
          const signaturePromise = signer.signMessage(`I am signing my one-time nonce: ${nonce}`);

          const onLoginSuccess = async () => {
            this.connecting = false;
            await this.$router.push('/account');
          };

          signaturePromise.then(async (signature) => {
            if (signature) {
              if (this.authenticated) {
                await this.updateUser({
                  user: {
                    publicAddress: publicAddress,
                    signature: signature
                  }
                }) //.then(onLoginSuccess);
                if (this.user?.public_address) { // success
                  await onLoginSuccess()
                } else { // failure
                  this.connecting = false;
                  await this.loadUser();
                  this.send({
                    message: 'Failed to connect wallet, there may already be an account with this wallet. Try logging out and in again with the wallet',
                    type: 'bg-danger',
                    icon: 'ni-alert-circle',
                    persist: true
                  });
                  await this.$router.push('/account');
                }
              } else {
                await this.loginWeb3({
                  user: {
                    publicAddress: publicAddress,
                    signature: signature
                  }
                }).then(onLoginSuccess);
              }
            }
          }).catch(() => {
            this.connecting = false;
          });
        }).catch(() => {
          this.connecting = false;
        });
      } catch (err) {
        console.error({err});
      }
    }
  },
  mounted() {
    if (this.isAuthenticated && this.user?.username && !this.authenticated) {
      this.$router.push('/account');
    }
  },
  setup() {
    const {
      isAuthenticated, user, load: loadUser, updateUser,
      web3User, getNonce, getNonceAuthenticated, loginWeb3
    } = useUser();
    const {send} = useUiNotification();

    return {
      isAuthenticated,
      user,
      web3User,
      getNonce,
      getNonceAuthenticated,
      loginWeb3,
      updateUser,
      loadUser,
      send
    };
  }
};
</script>
