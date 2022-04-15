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
              <ValidationProvider rules="required|min:2" v-slot="{ errors }">
                <div class="form-floating mb-4">
                  <input class="form-control" :class="!errors[0] ? '' : 'is-invalid border-danger'" id="username"
                         placeholder="username" v-model="form.username">
                  <label for="username" :class="{ 'text-danger': Boolean(errors[0]) }">Username</label>
                  <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                </div><!-- end form-floating -->
              </ValidationProvider>
              <ValidationProvider rules="required|min:6" v-slot="{ errors }">
                <div class="form-floating mb-4">
                  <input type="password" class="form-control password"
                         :class="!errors[0] ? '' : 'is-invalid border-danger'" id="password" placeholder="Password"
                         v-model="form.password">
                  <label for="password" :class="{ 'text-danger': Boolean(errors[0]) }">Password</label>
                  <a href="password" class="password-toggle" :class="!errors[0] ? '' : 'text-danger'"
                     title="Toggle show/hide pasword">
                    <em class="password-shown ni ni-eye-off"></em>
                    <em class="password-hidden ni ni-eye"></em>
                  </a>
                  <div class="text-danger fade" :class="{ 'show': Boolean(errors[0]) }">{{ errors[0] }}</div>
                </div><!-- end form-floating -->
              </ValidationProvider>
              <button class="btn btn-dark btn-full d-flex justify-content-center" type="submit" :disabled="loading">
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

    const error = reactive({
      login: null,
      register: null
    });

    const resetErrorValues = () => {
      error.login = null;
      error.register = null;
    };

    const handleUserErrors = () => {
      const hasUserErrors = userError.value.register || userError.value.login;
      if (hasUserErrors) {
        error.login = userError.value.login?.message;
        error.register = userError.value.register?.message;
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

    // const handleRegister = async () => handleForm(register)();

    const handleLogin = async () => handleForm(login)();

    return {
      form,
      userError,
      setUser,
      loading,
      handleLogin
    };
  }
};
</script>
