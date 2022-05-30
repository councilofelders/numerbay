<template>
  <section class="login-section section-space-b pt-4 pt-md-5 mt-md-3">
    <div class="container">
      <div class="row align-items-center justify-content-center">
        <div class="col-lg-6 mb-5 mb-lg-0 d-none d-lg-block">
          <img :src="SectionData.loginData.img" alt="" class="img-fluid">
        </div><!-- end col-lg-6 -->
        <div class="col-lg-6">
          <div class="section-head-sm">
            <h2 class="mb-1">{{ SectionData.loginData.title }}</h2>
            <p>{{ SectionData.loginData.subTitle }}</p>
          </div>
          <ValidationObserver v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(handleLogin)">
              <ValidationProvider v-slot="{ errors }" rules="required|min:2">
                <div class="form-floating mb-4">
                  <input id="username" v-model="form.username" :class="!errors[0] ? '' : 'is-invalid border-danger'"
                         class="form-control" placeholder="username">
                  <label :class="{ 'text-danger': Boolean(errors[0]) }" for="username">Username</label>
                  <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                </div><!-- end form-floating -->
              </ValidationProvider>
              <ValidationProvider v-slot="{ errors }" rules="required|min:6">
                <div class="form-floating mb-4">
                  <input id="password" v-model="form.password"
                         :class="!errors[0] ? '' : 'is-invalid border-danger'" class="form-control password" placeholder="Password"
                         type="password">
                  <label :class="{ 'text-danger': Boolean(errors[0]) }" for="password">Password</label>
                  <a :class="!errors[0] ? '' : 'text-danger'" class="password-toggle" href="password"
                     title="Toggle show/hide pasword">
                    <em class="password-shown ni ni-eye-off"></em>
                    <em class="password-hidden ni ni-eye"></em>
                  </a>
                  <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                </div><!-- end form-floating -->
              </ValidationProvider>
              <button :disabled="loading" class="btn btn-dark btn-full d-flex justify-content-center" type="submit">
                <span v-if="loading"><span class="spinner-border spinner-border-sm me-2" role="status"></span>Logging In...</span>
                <span v-else>{{ SectionData.loginData.btnText }}</span>
              </button>
            </form>
          </ValidationObserver>
        </div><!-- end col-lg-6 -->
      </div><!-- end row -->
    </div><!-- end container -->
  </section>
</template>
<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

// Composables
import {reactive, ref} from '@vue/composition-api';
import {useUser} from '@vue-storefront/numerbay';
import {useUiNotification} from '~/composables';

export default {
  name: 'LoginSection',
  data() {
    return {
      SectionData
    };
  },
  mounted() {

    /*  ======== Show/Hide passoword ======== */
    function showHidePassword(selector) {
      const elem = document.querySelectorAll(selector);
      if (elem.length > 0) {
        elem.forEach(item => {
          item.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.getElementById(item.getAttribute('href'));
            if (target.type === 'password') {
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
  setup(props, context) {
    const form = ref({});
    // const createAccount = ref(false);
    // const rememberMe = ref(false);
    const {login, loading, setUser, error: userError} = useUser();
    const {send} = useUiNotification();

    const error = reactive({
      login: null,
      register: null
    });

    const resetErrorValues = () => {
      error.login = null;
      error.register = null;
    };

    const handleUserErrors = () => {
      const hasUserErrors = userError.value.login;
      if (hasUserErrors) {
        send({
          message: userError.value.login?.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
        return true;
      }
      return false;
    };

    const handleForm = (fn) => async () => {
      resetErrorValues();
      await fn({user: form.value});
      const hasErrors = handleUserErrors();
      if (hasErrors) {
        return;
      }
      context.root.$router.push('/account');
    };

    const handleLogin = async () => handleForm(login)();

    return {
      form,
      userError,
      setUser,
      loading,
      handleLogin,
    };
  }
};
</script>
