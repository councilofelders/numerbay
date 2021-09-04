<template>
  <SfTabs :open-tab="1">
    <SfTab title="My listings">
      <div>
        <div class="top-buttons">
          <SfButton class="sf-button--primary" @click="handleListingClick()" :disabled="!!numeraiError.getModels || !user.numerai_api_key_public_id || numeraiLoading || userLoading">
            {{ $t('New Listing') }}
          </SfButton>
          <SfButton class="sf-button" :class="!user.numerai_api_key_public_id?'color-primary':'color-secondary'" @click="toggleNumeraiApiForm()" :disabled="numeraiLoading || userLoading">
            {{ !user.numerai_api_key_public_id?$t('Set Numerai API Key'):$t('Change Numerai API Key') }}
          </SfButton>
        </div>
        <div v-if="isNumeraiApiFormOpen">
          <NumeraiApiForm @submit="updateNumeraiApiKeyData" />
        </div>
        <p class="message" v-if="numeraiError.getModels">
          {{ numeraiError.getModels }}
        </p>
        <div v-if="products.length === 0" class="no-orders">
          <p class="no-orders__title">{{ $t('You currently have no listings') }}</p>
        </div>
        <SfTable v-else class="orders">
          <SfTableHeading>
            <SfTableHeader
              v-for="tableHeader in tableHeaders"
              :key="tableHeader"
              >{{ tableHeader }}</SfTableHeader>
          </SfTableHeading>
          <SfTableRow v-for="product in products" :key="productGetters.getId(product)">
            <SfTableData>
              <SfLink :link="'/p/'+productGetters.getId(product)+'/'+productGetters.getSlug(product)" :style="productGetters.getIsActive(product) ? '' : 'color: var(--c-text-disabled)'">
                {{ productGetters.getName(product).toUpperCase() }}
              </SfLink>
            </SfTableData>
            <SfTableData><span :style="productGetters.getIsActive(product) ? '' : 'color: var(--c-text-disabled)'">{{ categories.find(c=>c.id === Number(productGetters.getCategoryIds(product)[0])).slug }}</span></SfTableData>
            <SfTableData><span :style="productGetters.getIsActive(product) ? '' : 'color: var(--c-text-disabled)'">{{ $n(productGetters.getPrice(product).regular, 'currency') }}</span></SfTableData>
            <SfTableData class="orders__view orders__element--right">
              <SfButton class="sf-button--text desktop-only" @click="handleListingClick(product)" :disabled="!!numeraiError.getModels || !user.numerai_api_key_public_id || numeraiLoading || userLoading">
                {{ $t('Manage') }}
              </SfButton>
            </SfTableData>
          </SfTableRow>
        </SfTable>
      </div>
    </SfTab>
  </SfTabs>
</template>

<script>
import {
  SfTabs,
  SfTable,
  SfButton,
  SfProperty,
  SfLink,
  SfNotification
} from '@storefront-ui/vue';
import { computed, ref } from '@vue/composition-api';
import { useUiState } from '~/composables';
import {
  orderGetters,
  useProduct,
  useUser,
  userGetters,
  productGetters,
  useCategory,
  useNumerai,
  useGlobals
} from '@vue-storefront/numerbay';
import { AgnosticOrderStatus } from '@vue-storefront/core';
import { onSSR } from '@vue-storefront/core';
import NumeraiApiForm from '../../components/MyAccount/NumeraiApiForm';

export default {
  name: 'MyListings',
  components: {
    SfTabs,
    SfTable,
    SfButton,
    SfProperty,
    SfLink,
    SfNotification,
    NumeraiApiForm
  },
  mounted() {
    if (this.user.numerai_api_key_public_id) {
      this.getNumeraiModels();
    }
  },
  setup() {
    const { user, updateUser, error: userError, loading: userLoading } = useUser();
    const { categories, search: categorySearch } = useCategory();
    const { getModels: getNumeraiModels, loading: numeraiLoading, error: numeraiError } = useNumerai('my-listings');
    const { getGlobals } = useGlobals();

    onSSR(async () => {
      await categorySearch(); // {slug: 'all'}
    });
    const { products, search } = useProduct('products');
    const { toggleListingModal } = useUiState();
    const currentOrder = ref(null);
    const isNumeraiApiFormOpen = ref(false);

    const toggleNumeraiApiForm = async () => {
      isNumeraiApiFormOpen.value = !isNumeraiApiFormOpen.value;
    };

    const handleListingClick = async (product) => {
      toggleListingModal(product);
    };

    onSSR(async () => {
      await search({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}});
      await getGlobals();
    });

    const tableHeaders = [
      'Product Name',
      'Category',
      'Price',
      'Action'
    ];

    const getStatusTextClass = (order) => {
      const status = orderGetters.getStatus(order);
      switch (status) {
        case AgnosticOrderStatus.Open:
          return 'text-warning';
        case AgnosticOrderStatus.Complete:
          return 'text-success';
        default:
          return '';
      }
    };

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
        const hasUserErrors = userError.value.updateUser;
        if (hasUserErrors) {
          return;
        }
        await toggleNumeraiApiForm();
      }, onError);
    };

    return {
      tableHeaders,
      numeraiLoading,
      userLoading,
      getNumeraiModels,
      user: computed(() => user?.value ? user.value : null),
      categories: computed(() => categories?.value ? categories.value : []),
      products: computed(() => products?.value?.data ? products.value.data : []),
      isNumeraiApiFormOpen,
      toggleNumeraiApiForm,
      getStatusTextClass,
      handleListingClick,
      productGetters,
      orderGetters,
      updateNumeraiApiKeyData,
      currentOrder,
      numeraiError
    };
  }
};
</script>

<style lang='scss' scoped>
.top-buttons {
  @include for-desktop {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
}
.no-orders {
  &__title {
    margin: 0 0 var(--spacer-lg) 0;
    font: var(--font-weight--normal) var(--font-size--base) / 1.6 var(--font-family--primary);
  }
  &__button {
    --button-width: 100%;
    @include for-desktop {
      --button-width: 17,5rem;
    }
  }
}
.orders {
  @include for-desktop {
    &__element {
      &--right {
        --table-column-flex: 0;
        text-align: right;
      }
    }
  }
}
.all-orders {
  --button-padding: var(--spacer-base) 0;
}
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
.product {
  &__properties {
    margin: var(--spacer-xl) 0 0 0;
  }
  &__property,
  &__action {
    font-size: var(--font-size--sm);
  }
  &__action {
    color: var(--c-gray-variant);
    font-size: var(--font-size--sm);
    margin: 0 0 var(--spacer-sm) 0;
    &:last-child {
      margin: 0;
    }
  }
  &__qty {
    color: var(--c-text);
  }
}
.products {
  --table-column-flex: 1;
  &__name {
    margin-right: var(--spacer-sm);
    @include for-desktop {
      --table-column-flex: 2;
    }
  }
}
.highlighted {
  box-sizing: border-box;
  width: 100%;
  background-color: var(--c-light);
  padding: var(--spacer-sm);
  --property-value-font-size: var(--font-size--base);
  --property-name-font-size: var(--font-size--base);
  &:last-child {
    margin-bottom: 0;
  }
  ::v-deep .sf-property__name {
    white-space: nowrap;
  }
  ::v-deep .sf-property__value {
    text-align: right;
  }
  &--total {
    margin-bottom: var(--spacer-sm);
  }
  @include for-desktop {
    padding: var(--spacer-xl);
    --property-name-font-size: var(--font-size--lg);
    --property-name-font-weight: var(--font-weight--medium);
    --property-value-font-size: var(--font-size--lg);
    --property-value-font-weight: var(--font-weight--semibold);
  }
}

</style>
