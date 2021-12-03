<template>
  <SfTabs :open-tab="1">
    <SfTab title="Numerai API">
      <NumeraiApiForm @submit="updateNumeraiApiKeyData" />
    </SfTab>
  </SfTabs>
</template>

<script>
import { SfTabs } from '@storefront-ui/vue';
import { useNumerai, useUser } from '@vue-storefront/numerbay';
import NumeraiApiForm from '../../components/MyAccount/NumeraiApiForm';

export default {
  name: 'NumeraiApi',

  components: {
    SfTabs,
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
</style>
