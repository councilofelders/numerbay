<template>
  <ValidationObserver v-slot="{ handleSubmit, reset }">
    <p class="message">
      You can create API Key in the
      <SfLink class="message__link" href="https://numer.ai/account" target="_blank">Numerai Account</SfLink>
      page. Make sure it has at least <b>View user info</b> permission. NumerBay only uses essential information to verify model ownership.
    </p>
    <form class="form" @submit.prevent="handleSubmit(submitForm(reset))">
      <ValidationProvider rules="required|min:2" v-slot="{ errors }" class="form__element">
        <SfInput
          v-model="form.numeraiApiKeyPublicId"
          name="numeraiApiKeyPublicId"
          label="Numerai API Key Public Id"
          required
          :disabled="loading"
          :valid="!errors[0]"
          :errorMessage="errors[0]"
        />
      </ValidationProvider>
      <ValidationProvider rules="required|min:2" v-slot="{ errors }" class="form__element">
        <SfInput
          v-model="form.numeraiApiKeySecret"
          name="numeraiApiKeySecret"
          label="Numerai API Key Secret"
          type="password"
          required
          :disabled="loading"
          :valid="!errors[0]"
          :errorMessage="errors[0]"
        />
      </ValidationProvider>
      <div v-if="error.updateUser">
        {{ error.updateUser }}
      </div>
      <div v-if="loading">
        <SfLoader :class="{ loader: loading }" :loading="loading"></SfLoader>
        Checking API key, please wait...
      </div>
      <SfButton class="form__button" :disabled="loading">{{ $t('Save') }}</SfButton>
    </form>
  </ValidationObserver>
</template>

<script>
import { ref } from '@vue/composition-api';
import { ValidationProvider, ValidationObserver } from 'vee-validate';
import { useUser, userGetters } from '@vue-storefront/numerbay';
import { SfInput, SfButton, SfLink, SfLoader } from '@storefront-ui/vue';

export default {
  name: 'NumeraiApiForm',

  components: {
    SfInput,
    SfButton,
    SfLink,
    SfLoader,
    ValidationProvider,
    ValidationObserver
  },

  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  setup(_, { emit }) {
    const { user, error, loading } = useUser();

    // const error = reactive({
    //   updateUser: null
    // });
    //
    // const resetErrorValues = () => {
    //   error.updateUser = null;
    // };

    const resetForm = () => ({
      numeraiApiKeyPublicId: userGetters.getNumeraiApiKeyPublicId(user.value)
    });

    const form = ref(resetForm());

    const submitForm = (resetValidationFn) => {
      return () => {
        const onComplete = () => {
          form.value = resetForm();
          resetValidationFn();
          // resetErrorValues();
        };

        const onError = () => {
          // TODO: Handle error
        };

        emit('submit', { form, onComplete, onError });
      };
    };

    return {
      form,
      error,
      loading,
      submitForm
    };
  }
};
</script>

<style lang='scss' scoped>
.message {
  margin: 0 0 var(--spacer-xl) 0;
  font: var(--font-weight--light) var(--font-size--base) / 1.6 var(--font-family--primary);
  &__link {
    color: var(--c-primary);
    font-weight: var(--font-weight--medium);
    font-family: var(--font-family--primary);
    font-size: var(--font-size--base);
    text-decoration: none;
    &:hover {
      color: var(--c-text);
    }
  }
}
.form {
  &__element {
    display: block;
    margin: 0 0 var(--spacer-lg) 0;
  }
  &__button {
    display: block;
    width: 100%;
    @include for-desktop {
      width: 17.5rem;
    }
  }
  &__horizontal {
    @include for-desktop {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
    }
    .form__element {
      @include for-desktop {
        flex: 1;
        margin-right: var(--spacer-2xl);
      }

      &:last-child {
        margin-right: 0;
      }
    }
  }
}
</style>
