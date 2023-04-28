<template>
  <div class="col-lg-9 ps-xl-5">
    <div class="user-panel-title-box">
      <h3>Edit Profile</h3>
    </div><!-- end user-panel-title-box -->
    <div class="profile-setting-panel-wrap">
      <ul id="myTab" class="nav nav-tabs nav-tabs-s1 nav-tabs-mobile-size" role="tablist">
        <li v-for="list in SectionData.editProfileData.editProfileTabNav" :key="list.id" class="nav-item"
            role="presentation">
          <button :id="list.slug" :class="list.isActive" :data-bs-target="list.bsTarget" class="nav-link"
                  data-bs-toggle="tab" type="button">{{ list.title }}
          </button>
        </li>
      </ul>
      <div id="myTabContent" class="tab-content mt-4">
        <div id="account-information" aria-labelledby="account-information-tab" class="tab-pane fade show active"
             role="tabpanel">
          <div class="profile-setting-panel">
            <h5 class="mb-4">Edit Profile</h5>
            <ValidationObserver key="profile" v-slot="{ handleSubmit }">
              <div class="row mt-4">
                <ValidationProvider v-slot="{ errors }" rules="required|min:2" slim>
                  <div class="col-lg-6 mb-3">
                    <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label"
                           for="username">Username</label>
                    <input id="username" v-model="form.username" :class="!errors[0] ? '' : 'is-invalid'"
                           class="form-control form-control-s1" required type="text">
                    <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                  </div><!-- end col -->
                </ValidationProvider>
                <ValidationProvider v-slot="{ errors }" rules="email" slim>
                  <div class="col-lg-6 mb-3">
                    <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label" for="email">Email</label>
                    <input id="email" v-model="form.email" :class="!errors[0] ? '' : 'is-invalid'"
                           class="form-control form-control-s1" type="email">
                    <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                  </div><!-- end col -->
                </ValidationProvider>
              </div><!-- end row -->
              <div class="row">
                <ValidationProvider v-slot="{ errors }" rules="url" slim>
                  <div class="col-lg-6 mb-3">
                    <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label" for="discordLink">Discord
                      Link</label>
                    <input id="discordLink" v-model="form.socialDiscord" :class="!errors[0] ? '' : 'is-invalid'"
                           class="form-control form-control-s1"
                           placeholder="E.g. https://discord.com/users/363554690652438528" type="text">
                    <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                  </div><!-- end col -->
                </ValidationProvider>
                <ValidationProvider v-slot="{ errors }" rules="url" slim>
                  <div class="col-lg-6 mb-3">
                    <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label" for="linkedInLink">LinkedIn
                      Link</label>
                    <input id="linkedInLink" v-model="form.socialLinkedIn" :class="!errors[0] ? '' : 'is-invalid'"
                           class="form-control form-control-s1"
                           placeholder="E.g. https://www.linkedin.com/in/richardcraib" type="text">
                    <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                  </div><!-- end col -->
                </ValidationProvider>
                <ValidationProvider v-slot="{ errors }" rules="url" slim>
                  <div class="col-lg-6 mb-3">
                    <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label" for="twitterLink">Twitter
                      Link</label>
                    <input id="twitterLink" v-model="form.socialTwitter" :class="!errors[0] ? '' : 'is-invalid'"
                           class="form-control form-control-s1"
                           placeholder="E.g. https://twitter.com/numerai" type="text">
                    <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                  </div><!-- end col -->
                </ValidationProvider>
                <ValidationProvider v-slot="{ errors }" rules="url" slim>
                  <div class="col-lg-6 mb-3">
                    <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label" for="webLink">Web
                      Link</label>
                    <input id="webLink" v-model="form.socialWebsite" :class="!errors[0] ? '' : 'is-invalid'"
                           class="form-control form-control-s1"
                           placeholder="E.g. https://numer.ai/" type="text">
                    <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                  </div><!-- end col -->
                </ValidationProvider>
              </div><!-- end row -->
              <button :disabled="userLoading" class="btn btn-dark mt-3 d-flex justify-content-center"
                      type="button" @click="handleSubmit(onUpdateProfile)">
                <span v-if="userLoading"><span class="spinner-border spinner-border-sm me-2" role="status"></span>Saving...</span>
                <span v-else>Update Profile</span>
              </button>
            </ValidationObserver>
            <hr class="my-4">
            <h5 class="mb-4">Encryption Key</h5>
            <div v-if="!Boolean(userGetters.getPublicKey(user)) && !Boolean(userGetters.getPublicKeyV2(user))" class="alert alert-warning d-flex mb-4" role="alert">
              <svg class="flex-shrink-0 me-3" fill="currentColor" height="30" viewBox="0 0 24 24" width="30">
                <path
                  d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"></path>
              </svg>
              <p class="fs-14">
                Some purchases may require a key pair for client-side encryption, please generate one below.
              </p>
            </div><!-- end alert -->
            <div v-if="Boolean(userGetters.getPublicKey(user)) && !Boolean(userGetters.getPublicKeyV2(user))" class="alert alert-warning d-flex mb-4" role="alert">
              <svg class="flex-shrink-0 me-3" fill="currentColor" height="30" viewBox="0 0 24 24" width="30">
                <path
                  d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"></path>
              </svg>
              <p class="fs-14">
                The current encryption mechanism is deprecated, please migrate by generate a new key pair below. This operation cannot be undone. <a class="link-secondary" href="https://docs.numerbay.ai/updates/encryption-v2" target="_blank"><em
                        class="ni ni-help"></em> Learn more about the deprecation</a>.
              </p>
            </div><!-- end alert -->
            <div class="row mt-4">
              <div class="col-lg-8">
                <a class="btn btn-outline-dark" @click="toggleKeyChangeModal" v-if="Boolean(userGetters.getPublicKey(user)) || Boolean(userGetters.getPublicKeyV2(user))">Replace key pair</a>
                <a class="btn btn-dark" @click="generateKeyPair" v-else>Generate key pair</a>
                <button v-if="Boolean(userGetters.getPublicKey(user)) || Boolean(userGetters.getPublicKeyV2(user))" class="copy-text ms-2" type="button"
                        @click="exportKeyPair"><em class="ni ni-download"></em> Export key file
                </button>
              </div>
            </div>
            <hr class="my-4">
            <h5 class="mb-4">Wallet</h5>
            <div v-if="userGetters.getPublicAddress(user)" class="row mt-4">
              <div class="col-lg-8">
                <div class="d-flex align-items-center">
                  <input id="copy-input" v-model="userGetters.getPublicAddress(user)" class="copy-input copy-input-s1"
                         readonly type="text">
                  <div class="tooltip-s1">
                    <button v-clipboard:copy="userGetters.getPublicAddress(user)" v-clipboard:success="onCopy"
                            class="copy-text ms-2" type="button">
                      <span class="tooltip-s1-text tooltip-text">Copy</span>
                      <em class="ni ni-copy"></em>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="alert alert-warning d-flex mb-4" role="alert">
              <svg class="flex-shrink-0 me-3" fill="currentColor" height="30" viewBox="0 0 24 24" width="30">
                <path
                  d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"></path>
              </svg>
              <p class="fs-14">
                Please connect a wallet in order to generate a key pair.
              </p>
            </div><!-- end alert -->
            <div class="row mt-4">
              <div class="col-lg-8">
                <router-link :to="{
                              name: 'login v2',
                              params: {
                                authenticated: true
                              }
                            }" class="btn btn-outline-dark"><em class="ni ni-plus"></em> Connect a new wallet
                </router-link>
              </div>
            </div>
          </div><!-- end profile-setting-panel -->
        </div><!-- end tab-pane -->
        <div id="change-password" aria-labelledby="change-password-tab" class="tab-pane fade" role="tabpanel">
          <div class="profile-setting-panel">
            <h5 class="mb-4">Change Password</h5>
            <ValidationObserver key="password" v-slot="{ handleSubmit, reset }">
              <ValidationProvider v-slot="{ errors }" rules="required|min:6" slim vid="newPassword">
                <div class="mb-3">
                  <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label" for="newPassword">New
                    Password</label>
                  <div class="position-relative">
                    <input id="newPassword" v-model="pwdForm.password" :class="!errors[0] ? '' : 'is-invalid'"
                           class="form-control form-control-s1" name="newPassword" placeholder="New password" type="password">
                    <a :class="!errors[0] ? '' : 'text-danger'" class="password-toggle" href="newPassword"
                       title="Toggle show/hide pasword">
                      <em class="password-shown ni ni-eye-off"></em>
                      <em class="password-hidden ni ni-eye"></em>
                    </a>
                  </div>
                  <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                </div>
              </ValidationProvider>
              <ValidationProvider v-slot="{ errors }" rules="required|min:6|confirmed:newPassword" slim>
                <div class="mb-3">
                  <label :class="{ 'text-danger': Boolean(errors[0]) }" class="form-label" for="confirmNewPassword">Confirm
                    New Password</label>
                  <div class="position-relative">
                    <input id="confirmNewPassword" v-model="pwdForm.confirmPassword" :class="!errors[0] ? '' : 'is-invalid'"
                           class="form-control form-control-s1" name="confirmPassword" placeholder="Confirm new password"
                           type="password">
                    <a :class="!errors[0] ? '' : 'text-danger'" class="password-toggle" href="confirmNewPassword"
                       title="Toggle show/hide pasword">
                      <em class="password-shown ni ni-eye-off"></em>
                      <em class="password-hidden ni ni-eye"></em>
                    </a>
                  </div>
                  <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                </div>
              </ValidationProvider>
              <button :disabled="userLoading" class="btn btn-dark mt-3 d-flex justify-content-center"
                      type="button" @click="handleSubmit(onUpdatePassword(reset))">
                <span v-if="userLoading"><span class="spinner-border spinner-border-sm me-2" role="status"></span>Saving...</span>
                <span v-else>Update Password</span>
              </button>
            </ValidationObserver>
          </div><!-- end profile-setting-panel -->
        </div><!-- end tab-pane -->
      </div><!-- end tab-content -->
    </div><!-- end profile-setting-panel-wrap-->
    <!-- Modal -->
    <Modal ref="keyChangeModal" modal-id="keyChangeModal" @registeredModal="keyChangeModal = $event">
      <template slot="title">Regenerate Encryption Key</template>
        <p class="mb-3">You are about to replace your existing encryption key pair with a new one.</p>
        <div class="alert alert-warning d-flex mb-4" role="alert">
          <svg class="flex-shrink-0 me-3" fill="currentColor" height="30" viewBox="0 0 24 24" width="30">
            <path
              d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"></path>
          </svg>
          <p class="fs-14">
            You will lose access to all existing files encrypted with the old key.
          </p>
        </div><!-- end alert -->
        <a class="btn btn-dark btn-full d-flex justify-content-center mt-4" @click="replaceKeyPair">Confirm
        </a>
    </Modal><!-- end modal-->
  </div><!-- end col-lg-8 -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

// Composables
import {ref} from '@vue/composition-api';
import {encodeBase64} from 'tweetnacl-util';
import {useUser, userGetters} from '@vue-storefront/numerbay';
import {useUiNotification} from '~/composables';
import {extend} from 'vee-validate';
import {confirmed} from 'vee-validate/dist/rules';

extend('confirmed', {
  ...confirmed,
  message: 'Password not matched'
});

extend('url', {
  validate: (value) => {
    if (value) {
      // eslint-disable-next-line
      return /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(value);
    }

    return false;
  },
  message: 'This must be a valid URL'
});

export default {
  name: 'AccountSection',
  data() {
    return {
      SectionData,
      pwdForm: {},
      keyChangeModal: null
    };
  },
  mounted() {

    /* ===========SHOW UPLOADED IMAGE ================== */
    function uploadImage(selector) {
      const elem = document.querySelectorAll(selector);
      if (elem.length > 0) {
        elem.forEach(item => {
          item.addEventListener('change', function () {
            if (item.files && item.files[0]) {
              const img = document.getElementById(item.dataset.target);
              img.onload = function () {
                URL.revokeObjectURL(img.src);
              };
              img.src = URL.createObjectURL(item.files[0]);

              const allowedExtensions = ['jpg', 'JPEG', 'JPG', 'png'];
              const fileExtension = this.value.split('.').pop();
              const lastDot = this.value.lastIndexOf('.');
              const ext = this.value.substring(lastDot + 1);
              const extTxt = img.value = ext;
              if (!allowedExtensions.includes(fileExtension)) {
                alert(extTxt + ' file type not allowed, Please upload jpg, JPG, JPEG, or png file');
                img.src = ' ';
              }
            }
          });
        });
      }
    }

    uploadImage('.upload-image');

    /* =========== Show/Hide passoword ============== */
    function showHidePassword(selector) {
      const elem = document.querySelectorAll(selector);
      if (elem.length > 0) {
        elem.forEach(item => {
          item.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.getElementById(item.getAttribute('href'));
            if (target.type == 'password') {
              target.type = 'text';
              item.classList.add('is-shown');
            } else {
              target.type = 'password';
              item.classList.remove('is-shown');
            }
          });

        });
      }
    }

    showHidePassword('.password-toggle');

  },
  methods: {
    async onUpdateProfile() {
      await this.updateUser({
        user: {
          username: this.form.username,
          email: this.form.email,
          socialDiscord: this.form.socialDiscord,
          socialLinkedIn: this.form.socialLinkedIn,
          socialTwitter: this.form.socialTwitter,
          socialWebsite: this.form.socialWebsite,
        }
      });
      this.form = this.resetForm();
      if (this.userError.updateUser) {
        this.send({
          message: this.userError.updateUser.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
      } else {
        this.send({
          message: 'Successfully updated profile',
          type: 'bg-success',
          icon: 'ni-check'
        });
      }
    },
    async onSaveFactor() {
      await this.updateUser({
        user: {
          factor: this.form.factor,
        }
      });
      this.form = this.resetForm();
      if (this.userError.updateUser) {
        this.send({
          message: this.userError.updateUser.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
      } else {
        this.send({
          message: 'Successfully updated pricing adjustment factor',
          type: 'bg-success',
          icon: 'ni-check'
        });
      }
    },
    toggleKeyChangeModal() {
      this.keyChangeModal?.toggle();
    },
    beforeDestroy() {
      this.keyChangeModal?.hide();
    },
    async replaceKeyPair() {
      this.keyChangeModal?.hide();
      await this.generateKeyPair();
    },
    async generateKeyPair() {
      if (!this.userGetters.getPublicAddress(this.user)) {
        await this.send({
          message: 'Please connect a MetaMask wallet first',
          type: 'bg-warning',
          icon: 'ni-alert-circle'
        });
        return;
      }

      const keys = await this.$encryption.createKeys(this.$wallet.provider.getSigner());

      let encryptedPrivateKey = null;
      try {
        encryptedPrivateKey = JSON.stringify({
          data: this.$encryption.symmetricalEncrypt({data: keys.privateKey}, keys.storageEncryptionKey),
          salt: keys.storageEncryptionKeySalt
        })
      } catch {
        await this.send({
          message: 'Signature is required',
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
        return;
      }

      await this.updateUser({
        user: {
          publicKeyV2: keys.publicKey,
          encryptedPrivateKeyV2: encryptedPrivateKey
        }
      });
      this.form = this.resetForm();

      await this.send({
        message: 'Key pair generated, please export for safe-keeping',
        type: 'bg-success',
        icon: 'ni-check'
      });
    },
    onUpdatePassword(resetValidationFn) {
      return () => {
        this.updateUser({
          user: {
            password: this.pwdForm.password
          }
        });
        resetValidationFn();
        this.pwdForm = {};
        if (this.userError.updateUser) {
          this.send({
            message: this.userError.updateUser.message,
            type: 'bg-danger',
            icon: 'ni-alert-circle'
          });
        } else {
          this.send({
            message: 'Successfully updated password',
            type: 'bg-success',
            icon: 'ni-check'
          });
        }
      };
    },
    downloadFile(file, name) {
      const a = document.createElement('a');
      document.body.appendChild(a);
      a.style = 'display: none';

      const url = window.URL.createObjectURL(file);
      a.href = url;
      a.download = name;
      a.click();
      window.URL.revokeObjectURL(url);
    },
    async exportKeyPair() {
      if (this.userGetters.getPublicKeyV2(this.user)) {
        await this.exportKeyPairV2();
      } else {
        await this.exportKeyPairLegacy();
      }
    },
    async exportKeyPairV2() {
      try {
        const encryptedPrivateKeyObj = JSON.parse(this.form.encryptedPrivateKeyV2)
        const symmetricalKeySalt = encryptedPrivateKeyObj.salt;
        const storageEncryptionKey = (await this.$encryption.getSymmetricalKeyFromSignature(this.$wallet.provider.getSigner(), symmetricalKeySalt)).symmetricalKey;

        const privateKey = this.$encryption.symmetricalDecrypt(
          encryptedPrivateKeyObj.data,
          storageEncryptionKey
        ).data

        const keyJson = JSON.stringify({public_key: this.form.publicKeyV2, private_key: privateKey});
        this.downloadFile(new Blob([keyJson], {type: 'application/json'}), 'numerbay.json');
      } catch (err) {
        this.send({
          message: err?.message || 'Failed to export key pair.',
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
      }
    },
    async exportKeyPairLegacy() {
      try {
        if (!this.$wallet.account) {
          await this.$wallet.connect();
        }

        const privateKeyStr = await window.ethereum.request({
          method: 'eth_decrypt',
          params: [this.form.encryptedPrivateKey, this.$wallet.account]
        });

        const privateKey = encodeBase64(new Uint8Array(privateKeyStr.split(',').map((item) => parseInt(item))));
        // eslint-disable-next-line camelcase
        const keyJson = JSON.stringify({public_key: this.form.publicKey, private_key: privateKey});
        this.downloadFile(new Blob([keyJson], {type: 'application/json'}), 'numerbay.json');
      } catch (err) {
        this.send({
          message: err?.message || 'Failed to export key pair.',
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
      }
    }
  },
  setup() {
    const {user, isAuthenticated, loading: userLoading, updateUser, error: userError} = useUser();
    const {send} = useUiNotification();

    const resetForm = () => ({
      username: userGetters.getUsername(user.value),
      email: userGetters.getEmailAddress(user.value),
      socialDiscord: userGetters.getSocialDiscord(user.value),
      socialLinkedIn: userGetters.getSocialLinkedIn(user.value),
      socialTwitter: userGetters.getSocialTwitter(user.value),
      socialWebsite: userGetters.getSocialWebsite(user.value),
      // publicAddress: userGetters.getPublicAddress(user.value),
      // nonce: userGetters.getNonce(user.value),
      publicKey: user.value?.public_key,
      encryptedPrivateKey: user.value?.encrypted_private_key,
      publicKeyV2: user.value?.public_key_v2,
      encryptedPrivateKeyV2: user.value?.encrypted_private_key_v2,
      factor: user.value?.props?.factor
    });

    const form = ref(resetForm());

    const onCopy = (e) => {
      const target = e.trigger.querySelector('.tooltip-text');
      const prevText = target.innerHTML;
      target.innerHTML = 'Copied';
      setTimeout(function () {
        target.innerHTML = prevText;
      }, 1000);
    };

    return {
      form,
      user,
      userLoading,
      userError,
      userGetters,
      resetForm,
      updateUser,
      onCopy,
      send
    };
  }
};
</script>
