<template>
    <section class="login-section section-space-b pt-4 pt-md-5 mt-md-3">
            <div class="container">
                <div class="row ">
                    <div class="col-lg-8 col-xl-6 mx-auto">
                        <ul class="row g-gs nav nav-tabs nav-tabs-s2 justify-content-center" id="myTab" role="tablist">
                            <li class="nav-item col-sm-6 col-6" role="presentation">
                                <button class="nav-link active" id="meta-mask-tab" data-bs-toggle="tab" data-bs-target="#meta-mask" type="button">
                                    <img :src="require('@/images/brand/metamask.svg')" alt="" class="icon icon-svg">
                                    <span class="nav-link-title mt-2 mt-sm-3 d-block">MetaMask</span>
                                </button>
                            </li>
                            <li class="nav-item col-sm-6 col-6" role="presentation" v-if="!authenticated">
                                <button class="nav-link" id="wallet-connect-tab" data-bs-toggle="tab" data-bs-target="#wallet-connect" type="button">
                                    <img :src="require('@/images/thumb/icon-users.svg')" alt="" class="icon icon-svg">
                                    <span class="nav-link-title mt-2 mt-sm-3 d-block">Username (Legacy)</span>
                                </button>
                            </li>
                        </ul>
                        <div class="gap-2x"></div><!-- end gap -->
                        <div class="tab-content" id="myTabContent">
                            <div class="tab-pane fade show active" id="meta-mask" role="tabpanel" aria-labelledby="meta-mask-tab">
                                <div class="card-media card-media-s3 text-center">
                                    <div class="card-media-body">
                                        <h3 class="mb-4">{{ SectionData.loginDataTwo.title }}</h3>
                                        <button @click="onWalletConnect" class="btn btn-dark" :disabled="connecting">
                                          <span v-if="connecting"><span class="spinner-border spinner-border-sm me-2" role="status" ></span>Connecting...</span>
                                          <span v-else>Connect</span>
                                        </button>
                                        <p class="mt-3" v-if="SectionData.loginDataTwo.btnTextLink"><a :href="SectionData.loginDataTwo.btnTextLink" target="_blank" class=" fs-13 btn-link fw-regular">{{ SectionData.loginDataTwo.btnTextTwo }}</a></p>
                                    </div>
                                </div><!-- end card-media -->
                            </div><!-- end tab-pane -->
                            <div class="tab-pane fade" id="wallet-connect" role="tabpanel" aria-labelledby="wallet-connect-tab">
                                <div class="card-media card-media-s3 text-center">
                                    <div class="card-media-body">
                                        <h3 class="mb-4">{{ SectionData.loginDataTwo.titleTwo }}</h3>
                                        <router-link :to="SectionData.loginDataTwo.btnLink" class="btn btn-dark">{{ SectionData.loginDataTwo.btnTextFour }}</router-link>
                                        <p class="mt-3" v-if="SectionData.loginDataTwo.btnTextLinkTwo"><router-link :to="SectionData.loginDataTwo.btnTextLinkTwo" target="_blank" class=" fs-13 btn-link fw-regular">{{ SectionData.loginDataTwo.btnTextThree }}</router-link></p>
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
import { useUser } from '@vue-storefront/numerbay';

export default {
  name: 'LoginSectionTwo',
  data () {
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
        await this.$wallet.connect().then(async ()=>{
          const publicAddress = this.$wallet.account;
          if (this.authenticated) {
            await this.getNonceAuthenticated();
          } else {
            await this.getNonce({ publicAddress: publicAddress });
          }
          const { nonce } = this.web3User.nonce;
          const signer = this.$wallet.provider.getSigner();
          const signaturePromise = signer.signMessage(`I am signing my one-time nonce: ${nonce}`);

          const onLoginSuccess = async () => {
            console.log('login success');
            this.connecting = false;
            await this.$router.push('/account');
          };

          signaturePromise.then(async (signature)=>{
            if (signature) {
              if (this.authenticated) {
                await this.updateUser({
                  user: {
                    publicAddress: publicAddress,
                    signature: signature
                  }
                }).then(onLoginSuccess);
              } else {
                await this.loginWeb3({
                  user: {
                    publicAddress: publicAddress,
                    signature: signature
                  }
                }).then(onLoginSuccess);
              }
            }
          }).catch(()=>{
            console.log('login fail');
            this.connecting = false;
          });
        }).catch(()=>{
          console.log('wallet fail');
          this.connecting = false;
        });
      } catch (err) {
        console.log('wallet fail2');
        console.error({ err });
        // this.$bvToast.toast(err.message || 'Wallet connection failed', {
        //   title: 'Wallet',
        //   variant: 'danger'
        // });
      }
    }
    // login() {
    //   identity.open('login');
    // },
    // logout() {
    //   identity.logout();
    //   this.user = null;
    // }
  },
  mounted() {
    if (this.isAuthenticated && this.user?.username && !this.authenticated) {
      this.$router.push('/account');
    }
  },
  setup() {
    const { isAuthenticated, user, register, login, loading, setUser, updateUser, error: userError,
      web3User, initWeb3Modal, ethereumListener, connectWeb3Modal, getNonce, getNonceAuthenticated, loginWeb3 } = useUser();

    return {
      isAuthenticated,
      user,
      web3User,
      getNonce,
      getNonceAuthenticated,
      loginWeb3,
      updateUser
    };
  }
};
</script>
