<template>
  <div class="col-lg-9 ps-xl-5">
    <div class="user-panel-title-box">
      <h3>Edit Profile</h3>
    </div><!-- end user-panel-title-box -->
    <div class="profile-setting-panel-wrap">
      <ul class="nav nav-tabs nav-tabs-s1 nav-tabs-mobile-size" id="myTab" role="tablist">
        <li class="nav-item" role="presentation" v-for="list in SectionData.editProfileData.editProfileTabNav"
            :key="list.id">
          <button class="nav-link" :class="list.isActive" :id="list.slug" data-bs-toggle="tab"
                  :data-bs-target="list.bsTarget" type="button">{{ list.title }}
          </button>
        </li>
      </ul>
      <div class="tab-content mt-4" id="myTabContent">
        <div class="tab-pane fade show active" id="account-information" role="tabpanel"
             aria-labelledby="account-information-tab">
          <div class="profile-setting-panel">
            <h5 class="mb-4">Edit Profile</h5>
            <ValidationObserver v-slot="{ handleSubmit }" key="profile">
              <div class="row mt-4">
                <ValidationProvider rules="required|min:2" v-slot="{ errors }" slim>
                  <div class="col-lg-6 mb-3">
                    <label for="username" class="form-label"
                           :class="{ 'text-danger': Boolean(errors[0]) }">Username</label>
                    <input type="text" id="username" class="form-control form-control-s1"
                           :class="!errors[0] ? '' : 'is-invalid'" v-model="form.username" required>
                    <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                  </div><!-- end col -->
                </ValidationProvider>
                <ValidationProvider rules="email" v-slot="{ errors }" slim>
                  <div class="col-lg-6 mb-3">
                    <label for="email" class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Email</label>
                    <input type="email" id="email" class="form-control form-control-s1"
                           :class="!errors[0] ? '' : 'is-invalid'" v-model="form.email">
                    <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                  </div><!-- end col -->
                </ValidationProvider>
              </div><!-- end row -->
              <div class="row">
                <ValidationProvider rules="url" v-slot="{ errors }" slim>
                  <div class="col-lg-6 mb-3">
                    <label for="rocketChatLink" class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">RocketChat
                      Link</label>
                    <input type="text" id="rocketChatLink" class="form-control form-control-s1"
                           :class="!errors[0] ? '' : 'is-invalid'"
                           placeholder="E.g. https://rocketchat.numer.ai/direct/slyfox" v-model="form.socialRocketChat">
                    <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                  </div><!-- end col -->
                </ValidationProvider>
                <ValidationProvider rules="url" v-slot="{ errors }" slim>
                  <div class="col-lg-6 mb-3">
                    <label for="linkedInLink" class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">LinkedIn
                      Link</label>
                    <input type="text" id="linkedInLink" class="form-control form-control-s1"
                           :class="!errors[0] ? '' : 'is-invalid'"
                           placeholder="E.g. https://www.linkedin.com/in/richardcraib" v-model="form.socialLinkedIn">
                    <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                  </div><!-- end col -->
                </ValidationProvider>
                <ValidationProvider rules="url" v-slot="{ errors }" slim>
                  <div class="col-lg-6 mb-3">
                    <label for="twitterLink" class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Twitter
                      Link</label>
                    <input type="text" id="twitterLink" class="form-control form-control-s1"
                           :class="!errors[0] ? '' : 'is-invalid'"
                           placeholder="E.g. https://twitter.com/numerai" v-model="form.socialTwitter">
                    <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                  </div><!-- end col -->
                </ValidationProvider>
                <ValidationProvider rules="url" v-slot="{ errors }" slim>
                  <div class="col-lg-6 mb-3">
                    <label for="webLink" class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Web
                      Link</label>
                    <input type="text" id="webLink" class="form-control form-control-s1"
                           :class="!errors[0] ? '' : 'is-invalid'"
                           placeholder="E.g. https://numer.ai/" v-model="form.socialWebsite">
                    <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                  </div><!-- end col -->
                </ValidationProvider>
              </div><!-- end row -->
              <button class="btn btn-dark mt-3 d-flex justify-content-center" type="button"
                      @click="handleSubmit(onUpdateProfile)" :disabled="userLoading">
                <span v-if="userLoading"><span class="spinner-border spinner-border-sm me-2" role="status"></span>Saving...</span>
                <span v-else>Update Profile</span>
              </button>
            </ValidationObserver>
            <hr class="my-4">
            <h5 class="mb-4">Encryption Key</h5>
            <div class="alert alert-warning d-flex mb-4" role="alert" v-if="!Boolean(userGetters.getPublicKey(user))">
              <svg class="flex-shrink-0 me-3" width="30" height="30" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"></path>
              </svg>
              <p class="fs-14">
                Some purchases may require a key pair for client-side encryption, please generate one below.
              </p>
            </div><!-- end alert -->
            <div class="row mt-4">
              <div class="col-lg-8">
                <a class="btn" :class="Boolean(userGetters.getPublicKey(user)) ? 'btn-outline-dark' : 'btn-dark'"
                   @click="generateKeyPair">Generate key pair</a>
                <button class="copy-text ms-2" type="button" v-if="Boolean(userGetters.getPublicKey(user))"
                        @click="exportKeyPair"><em class="ni ni-download"></em> Export key file
                </button>
              </div>
            </div>
            <hr class="my-4">
            <h5 class="mb-4">Wallet</h5>
            <div class="row mt-4" v-if="userGetters.getPublicAddress(user)">
              <div class="col-lg-8">
                <div class="d-flex align-items-center">
                  <input type="text" class="copy-input copy-input-s1" v-model="userGetters.getPublicAddress(user)"
                         id="copy-input" readonly>
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
            <div class="alert alert-warning d-flex mb-4" role="alert" v-else>
              <svg class="flex-shrink-0 me-3" width="30" height="30" viewBox="0 0 24 24" fill="currentColor">
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
        <div class="tab-pane fade" id="change-password" role="tabpanel" aria-labelledby="change-password-tab">
          <div class="profile-setting-panel">
            <h5 class="mb-4">Change Password</h5>
            <ValidationObserver v-slot="{ handleSubmit, reset }" key="password">
              <ValidationProvider vid="newPassword" rules="required|min:6" v-slot="{ errors }" slim>
                <div class="mb-3">
                  <label for="newPassword" class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">New
                    Password</label>
                  <div class="position-relative">
                    <input type="password" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'"
                           id="newPassword" name="newPassword" placeholder="New password" v-model="pwdForm.password">
                    <a href="newPassword" class="password-toggle" :class="!errors[0] ? '' : 'text-danger'"
                       title="Toggle show/hide pasword">
                      <em class="password-shown ni ni-eye-off"></em>
                      <em class="password-hidden ni ni-eye"></em>
                    </a>
                  </div>
                  <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                </div>
              </ValidationProvider>
              <ValidationProvider rules="required|min:6|confirmed:newPassword" v-slot="{ errors }" slim>
                <div class="mb-3">
                  <label for="confirmNewPassword" class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Confirm
                    New Password</label>
                  <div class="position-relative">
                    <input type="password" class="form-control form-control-s1" :class="!errors[0] ? '' : 'is-invalid'"
                           id="confirmNewPassword" name="confirmPassword" placeholder="Confirm new password"
                           v-model="pwdForm.confirmPassword">
                    <a href="confirmNewPassword" class="password-toggle" :class="!errors[0] ? '' : 'text-danger'"
                       title="Toggle show/hide pasword">
                      <em class="password-shown ni ni-eye-off"></em>
                      <em class="password-hidden ni ni-eye"></em>
                    </a>
                  </div>
                  <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                </div>
              </ValidationProvider>
              <button class="btn btn-dark mt-3 d-flex justify-content-center" type="button"
                      @click="handleSubmit(onUpdatePassword(reset))" :disabled="userLoading">
                <span v-if="userLoading"><span class="spinner-border spinner-border-sm me-2" role="status"></span>Saving...</span>
                <span v-else>Update Password</span>
              </button>
            </ValidationObserver>
          </div><!-- end profile-setting-panel -->
        </div><!-- end tab-pane -->
      </div><!-- end tab-content -->
    </div><!-- end profile-setting-panel-wrap-->
  </div><!-- end col-lg-8 -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

// Composables
import {ref} from '@vue/composition-api';
import {encrypt} from 'eth-sig-util';
import nacl from 'tweetnacl';
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
      pwdForm: {}
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
          socialRocketChat: this.form.socialRocketChat,
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
    async generateKeyPair() {
      if (!this.userGetters.getPublicAddress(this.user)) {
        await this.send({
          message: 'Please connect a MetaMask wallet first',
          type: 'bg-warning',
          icon: 'ni-alert-circle'
        });
        return;
      }

      const keyPair = nacl.box.keyPair();
      const privateKeyBytes = keyPair.secretKey;
      const publicKeyBytes = keyPair.publicKey;

      let encryptedPrivateKey = null;
      try {
        const accounts = await window.ethereum.request({
          method: 'eth_requestAccounts'
        });

        const key = await window.ethereum.request({
          method: 'eth_getEncryptionPublicKey',
          params: [accounts[0]]
        });

        encryptedPrivateKey = JSON.stringify(encrypt(
          key,
          {data: privateKeyBytes.toString('hex')},
          'x25519-xsalsa20-poly1305'
        ));
      } catch {
        await this.send({
          message: 'Public key access is required',
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
        return;
      }

      await this.updateUser({
        user: {
          publicKey: encodeBase64(publicKeyBytes),
          encryptedPrivateKey: encryptedPrivateKey
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
      const privateKeyStr = await window.ethereum.request({
        method: 'eth_decrypt',
        params: [this.form.encryptedPrivateKey, window.ethereum.selectedAddress]
      });

      const privateKey = encodeBase64(new Uint8Array(privateKeyStr.split(',').map((item) => parseInt(item))));
      // eslint-disable-next-line camelcase
      const keyJson = JSON.stringify({public_key: this.form.publicKey, private_key: privateKey});
      this.downloadFile(new Blob([keyJson], {type: 'application/json'}), 'numerbay.json');
    }
  },
  setup() {
    const {user, isAuthenticated, loading: userLoading, updateUser, error: userError} = useUser();
    const {send} = useUiNotification();

    const resetForm = () => ({
      username: userGetters.getUsername(user.value),
      email: userGetters.getEmailAddress(user.value),
      socialRocketChat: userGetters.getSocialRocketChat(user.value),
      socialLinkedIn: userGetters.getSocialLinkedIn(user.value),
      socialTwitter: userGetters.getSocialTwitter(user.value),
      socialWebsite: userGetters.getSocialWebsite(user.value),
      // publicAddress: userGetters.getPublicAddress(user.value),
      // nonce: userGetters.getNonce(user.value),
      publicKey: user.value?.public_key,
      encryptedPrivateKey: user.value?.encrypted_private_key
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
