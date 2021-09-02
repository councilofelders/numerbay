<template>
  <SfTabs :open-tab="1">
    <SfTab title="Numerai API">
      <NumeraiApiForm @submit="updateNumeraiApiKeyData" />
    </SfTab>
  </SfTabs>
</template>

<script>
import { extend } from 'vee-validate';
import { required, min, confirmed } from 'vee-validate/dist/rules';
import { SfTabs, SfInput, SfButton } from '@storefront-ui/vue';
import {useNumerai, useUser} from '@vue-storefront/numerbay';
import NumeraiApiForm from '../../components/MyAccount/NumeraiApiForm';

extend('required', {
  ...required,
  message: 'This field is required'
});

extend('min', {
  ...min,
  message: 'The field should have at least {length} characters'
});

extend('confirmed', {
  ...confirmed,
  message: 'Passwords don\'t match'
});

export default {
  name: 'NumeraiApi',

  components: {
    SfTabs,
    SfInput,
    SfButton,
    NumeraiApiForm
  },

  setup() {
    const { updateUser } = useUser();
    const { getModels: getNumeraiModels } = useNumerai('my-listings');

    const formHandler = async (fn, onComplete, onError) => {
      try {
        const data = await fn();
        await onComplete(data);
      } catch (error) {
        onError(error);
      }
    };

    const updateNumeraiApiKeyData = ({ form, onComplete, onError }) => {
      formHandler(() => updateUser({ user: form.value }), async () => {
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

    return {
      updateNumeraiApiKeyData
    };
  }
};
</script>

<style lang='scss' scoped>
.message,
.notice {
  font-family: var(--font-family--primary);
  line-height: 1.6;
}
.message {
  margin: 0 0 var(--spacer-xl) 0;
  font-size: var(--font-size--base);
  &__label {
    font-weight: 400;
  }
}
.notice {
  margin: var(--spacer-lg) 0 0 0;
  font-size: var(--font-size--sm);
}

</style>
