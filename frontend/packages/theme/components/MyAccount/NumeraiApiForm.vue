<template>
  <ValidationObserver v-slot="{ handleSubmit, reset }">
    <p class="message">
      You can create API Key in the
      <SfLink class="message__link" href="https://numer.ai/account" target="_blank">Numerai Account</SfLink>
      page. Make sure it has at least <b>View user info</b> permission. NumerBay only uses essential information to verify model ownership.
      <!--<SfButton class="sf-button&#45;&#45;text" title="Which permissions do I need?"><SfIcon icon="question_mark" class="color-blue-primary"></SfIcon></SfButton>-->
    </p>
    <div class="numerai-api-permissions">
      <SfProperty name="View user info" class="sf-property--without-suffix">
        <template #value>
          <span class="sf-property__value">
            <SfIcon icon="check" class="color-green-primary" v-if="user.numerai_api_key_can_read_user_info"></SfIcon>
            <SfIcon icon="cross" class="size-xxs color-red-primary" v-else></SfIcon>
          </span>
        </template>
      </SfProperty>
      <SfProperty name="View submission info" class="sf-property--without-suffix">
        <template #value>
          <span class="sf-property__value">
            <SfIcon icon="check" class="color-green-primary" v-if="user.numerai_api_key_can_read_submission_info"></SfIcon>
            <SfIcon icon="cross" class="size-xxs color-red-primary" v-else></SfIcon>
          </span>
        </template>
      </SfProperty>
      <SfProperty name="Upload submissions" class="sf-property--without-suffix">
        <template #value>
          <span class="sf-property__value">
            <SfIcon icon="check" class="color-green-primary" v-if="user.numerai_api_key_can_upload_submission"></SfIcon>
            <SfIcon icon="cross" class="size-xxs color-red-primary" v-else></SfIcon>
          </span>
        </template>
      </SfProperty>
      <SfProperty name="Stake" class="sf-property--without-suffix">
        <template #value>
          <span class="sf-property__value">
            <SfIcon icon="check" class="color-green-primary" v-if="user.numerai_api_key_can_stake"></SfIcon>
            <SfIcon icon="cross" class="size-xxs color-red-primary" v-else></SfIcon>
          </span>
        </template>
      </SfProperty>
    </div>
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
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
import { useUser, userGetters } from '@vue-storefront/numerbay';
import { useUiNotification } from '~/composables';
import { SfInput, SfButton, SfLink, SfLoader, SfIcon, SfProperty, SfDivider } from '@storefront-ui/vue';
import { min, required } from 'vee-validate/dist/rules';

extend('required', {
  ...required,
  message: 'This field is required'
});

extend('min', {
  ...min,
  message: 'The field should have at least {length} characters'
});

export default {
  name: 'NumeraiApiForm',

  components: {
    SfInput,
    SfButton,
    SfLink,
    SfLoader,
    SfIcon,
    SfProperty,
    SfDivider,
    ValidationProvider,
    ValidationObserver
  },

  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  setup(_, { emit }) {
    const { user, error, loading } = useUser();
    const { send } = useUiNotification();

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
          if (error.value.updateUser) {
            send({
              message: error.value.updateUser.message,
              type: 'danger'
            });
          } else {
            send({
              message: 'Successfully updated Numerai API Key',
              type: 'success',
              icon: 'check'
            });
          }
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
      user,
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
.numerai-api-permissions {
  @include for-desktop {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin: 0 0 var(--spacer-xl) 0;
  }
}
</style>
