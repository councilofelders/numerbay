<template>
  <div class="col-lg-9 ps-xl-5">
    <div class="user-panel-title-box">
      <div class="d-flex">
        <h3>Numerai Settings</h3>
        <div class="ms-auto d-flex">
          <span class="my-auto me-2">Last sync: {{ userGetters.getNumeraiLastSyncDate(user) }}</span>
          <button class="icon-btn" title="Sync with Numerai" :disabled="userLoading" @click="sync"><em
            class="ni ni-reload" v-if="!userLoading"></em><span class="spinner-border spinner-border-sm" role="status"
                                                                v-else></span></button>
        </div>
      </div>
    </div><!-- end user-panel-title-box -->
    <div class="profile-setting-panel-wrap">
      <p class="fs-14 mb-3">You must connect your Numerai account via API in order to trade on NumerBay.</p>
      <p class="fs-14 mb-3">You can create API Key in the <a href="https://numer.ai/account" target="_blank"><strong>Numerai
        Account</strong></a> page. Make sure it has at least <strong>View user info</strong> permission. NumerBay only
        uses essential information to verify model ownership.</p>
      <div class="row mt-4">
        <div class="col-lg-6"><p class="fs-14"><strong>View user info</strong>: <strong class="text-success"
                                                                                        v-if="user.numerai_api_key_can_read_user_info">Granted</strong><strong
          class="text-warning" v-else>Restricted</strong></p></div>
        <div class="col-lg-6"><p class="fs-14"><strong>View submission info</strong>: <strong class="text-success"
                                                                                              v-if="user.numerai_api_key_can_read_submission_info">Granted</strong><strong
          class="text-warning" v-else>Restricted</strong></p></div>
      </div>
      <div class="row">
        <div class="col-lg-6"><p class="fs-14"><strong>Upload submissions</strong>: <strong class="text-success"
                                                                                            v-if="user.numerai_api_key_can_upload_submission">Granted</strong><strong
          class="text-warning" v-else>Restricted</strong></p></div>
        <div class="col-lg-6 mb-3"><p class="fs-14 mb-3"><strong>Adjust stake</strong>: <strong class="text-success"
                                                                                                v-if="user.numerai_api_key_can_stake">Granted</strong><strong
          class="text-warning" v-else>Restricted</strong></p></div>
      </div>
      <ValidationObserver v-slot="{ handleSubmit, reset }">
        <ValidationProvider rules="required|min:2" v-slot="{ errors }" slim>
          <div class="mb-3">
            <label for="numeraiApiKeyPublicId" class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Numerai
              API Key Public Id</label>
            <input type="text" id="numeraiApiKeyPublicId" class="form-control form-control-s1"
                   :class="!errors[0] ? '' : 'is-invalid'" v-model="form.numeraiApiKeyPublicId">
            <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
          </div>
        </ValidationProvider>
        <!--        <div class="mb-3">
                    <label for="oldPassword" class="form-label">Old Password</label>
                    <div class="position-relative">
                        <input type="password" class="form-control form-control-s1" id="oldPassword" placeholder="Old password">
                        <a href="oldPassword" class="password-toggle" title="Toggle show/hide pasword">
                            <em class="password-shown ni ni-eye-off"></em>
                            <em class="password-hidden ni ni-eye"></em>
                        </a>
                    </div>
                </div>-->
        <ValidationProvider rules="required|min:2" v-slot="{ errors }" slim>
          <div class="mb-3">
            <label for="numeraiApiKeySecret" class="form-label" :class="{ 'text-danger': Boolean(errors[0]) }">Numerai
              API Key Secret</label>
            <div class="position-relative">
              <input type="password" id="numeraiApiKeySecret" class="form-control form-control-s1"
                     :class="!errors[0] ? '' : 'is-invalid'" v-model="form.numeraiApiKeySecret">
              <a href="numeraiApiKeySecret" class="password-toggle" :class="!errors[0] ? '' : 'text-danger'"
                 title="Toggle show/hide pasword">
                <em class="password-shown ni ni-eye-off"></em>
                <em class="password-hidden ni ni-eye"></em>
              </a>
              <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
            </div>
          </div>
        </ValidationProvider>
        <button class="btn btn-dark mt-3 d-flex justify-content-center" type="button"
                @click="handleSubmit(submitForm(reset))" :disabled="userLoading">
          <span v-if="userLoading"><span class="spinner-border spinner-border-sm me-2"
                                         role="status"></span>Saving...</span>
          <span v-else>Save</span>
        </button>
      </ValidationObserver>
      <!--        <hr class="my-4">-->
      <!--        <p class="fs-13">If your encounter errors. Please contact <a href="contact" class="btn-link">support</a></p>-->
    </div><!-- end profile-setting-panel-wrap-->
  </div><!-- end col-lg-8 -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

// Composables
import {ref} from '@vue/composition-api';
import {useNumerai, useUser, userGetters} from '@vue-storefront/numerbay';
import {useUiNotification} from '~/composables';

export default {
  name: 'NumeraiSettingSection',
  data() {
    return {
      SectionData,
      selected: 'Select a Country',
      options: [
        'Select a Country',
        'Afghanistan',
        'Åland Islands',
        'Albania',
        'American Samoa',
        'United States of America',
        'Uruguay',
        'Uzbekistan'
      ]
    };
  },
  methods: {
    async onSave() {
      await this.updateUser({
        user: {
          numeraiApiKeyPublicId: this.form.numeraiApiKeyPublicId,
          numeraiApiKeySecret: this.form.numeraiApiKeySecret
        }
      });
      this.form = this.resetForm();
      await this.getNumeraiModels();
    },
    async sync() {
      await this.syncUserNumerai();
    }
  },
  mounted() {

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
  setup() {
    const {user, isAuthenticated, loading: userLoading, updateUser, syncUserNumerai, error: userError} = useUser();
    const {getModels: getNumeraiModels} = useNumerai('account');
    const {send} = useUiNotification();

    const resetForm = () => ({
      numeraiApiKeyPublicId: userGetters.getNumeraiApiKeyPublicId(user.value)
    });

    const form = ref(resetForm());

    const formHandler = async (fn, onComplete, onError) => {
      try {
        const data = await fn();
        await onComplete(data);
      } catch (error) {
        onError(error);
      }
    };

    const updateNumeraiApiKeyData = ({form, onComplete, onError}) => {
      formHandler(() => updateUser({user: form.value}), async () => {
        onComplete();
        await getNumeraiModels();
        // const hasUserErrors = userError.value.updateUser;
        // if (hasUserErrors) {
        //   return;
        // }
        // await toggleNumeraiApiForm();
      }, async () => {
        onError();
      });
    };

    const submitForm = (resetValidationFn) => {
      return () => {
        const onComplete = () => {
          form.value = resetForm();
          resetValidationFn();
          if (userError.value.updateUser) {
            send({
              message: userError.value.updateUser.message,
              type: 'bg-danger',
              icon: 'ni-alert-circle'
            });
          } else {
            send({
              message: 'Successfully updated Numerai API Key',
              type: 'bg-success',
              icon: 'ni-check'
            });
          }
        };

        const onError = () => {
          // TODO: Handle error
        };

        updateNumeraiApiKeyData({form, onComplete, onError});
      };
    };

    return {
      form,
      user,
      userLoading,
      resetForm,
      getNumeraiModels,
      updateUser,
      syncUserNumerai,
      userGetters,
      submitForm,
      send
    };
  }
};
</script>
