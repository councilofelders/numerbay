<template>
  <SfTabs :open-tab="1">
    <SfTab title="My listings">
      <div v-if="currentListing">
        <SfButton class="sf-button--text all-listings" @click="currentListing = null">All Listings</SfButton>
        <ArtifactPanel :product="currentListing" :orders="getFilteredOrders(currentListing)"></ArtifactPanel>
        <SfTable class="orders">
          <SfTableHeading>
            <SfTableHeader>Order ID</SfTableHeader>
            <SfTableHeader>Round(s)</SfTableHeader>
            <SfTableHeader>Buyer</SfTableHeader>
            <SfTableHeader>Amount</SfTableHeader>
            <SfTableHeader>Status</SfTableHeader>
            <SfTableHeader>Action</SfTableHeader>
          </SfTableHeading>
          <SfTableRow v-for="order in getFilteredOrders(currentListing)" :key="orderGetters.getId(order)">
            <SfTableData>{{ orderGetters.getId(order) }}</SfTableData>
            <SfTableData v-if="orderGetters.getProduct(order).category.is_per_round && parseInt(orderGetters.getItemQty(order)) > 1">{{ `${orderGetters.getRound(order)}-${parseInt(orderGetters.getRound(order))+parseInt(orderGetters.getItemQty(order))-1}` }}</SfTableData>
            <SfTableData v-else>{{ orderGetters.getRound(order) }}</SfTableData>
            <SfTableData>{{ orderGetters.getBuyer(order) }}</SfTableData>
            <SfTableData>{{ orderGetters.getFormattedPrice(order, withCurrency=true, decimals=4) }}</SfTableData>
            <SfTableData>
              <span :class="getStatusTextClass(order)">{{ orderGetters.getStatus(order) }}</span>
            </SfTableData>
<!--            <SfTableData>-->
<!--              <span :class="getSubmissionStatusTextClass(order)">{{ orderGetters.getSubmissionStatus(order) }}</span>-->
<!--            </SfTableData>-->
            <SfTableData class="orders__view orders__element--right">
              <!--<SfButton class="sf-button&#45;&#45;text smartphone-only" @click="downloadOrder(order)">
                {{ $t('Download') }}
              </SfButton>-->
<!--              <SfButton class="sf-button&#45;&#45;text" @click="currentOrder = order">
                {{ $t('View details') }}
              </SfButton>-->
            </SfTableData>
            <SfTableRow v-for="artifact in order.artifacts" :key="artifactGetters.getId(artifact)">
              <SfTableData><span style="word-break: break-all;">{{ artifactGetters.getObjectName(artifact) }}</span></SfTableData>
              <SfTableData>
                <SfLoader :class="{ loader: componentLoading && !!activeArtifact && activeArtifact.id===artifact.id }" :loading="componentLoading && !!activeArtifact && activeArtifact.id===artifact.id">
                  <SfInput :value="artifact.description" style="margin-right: 10px" label="Description" :disabled="(componentLoading || loading) && !!activeArtifact" @input="(value)=>{artifact.description=value; activeArtifact=artifact}"/>
      <!--             @input="(value)=>(formEdit=(()=>handleEdit(value, product, artifact)))"-->
                </SfLoader>
              </SfTableData>
      <!--        <SfTableData>{{ artifactGetters.getObjectSize(artifact) }}</SfTableData>-->
              <SfTableData class="orders__view orders__element--right">
                <SfLoader :class="{ loader: loading && !!activeArtifact && activeArtifact.id===artifact.id }" :loading="loading && activeArtifact && activeArtifact.id===artifact.id">
                  <span class="artifact-actions" v-if="!!activeArtifact && activeArtifact.id===artifact.id">
                    <SfLoader :class="{ loader: loading }" :loading="loading">
                      <SfButton class="sf-button--text" @click="handleEdit(product, activeArtifact)">
                        {{ $t('Save') }}
                      </SfButton>
                    </SfLoader>
                  </span>
                  <span class="artifact-actions" v-else>
                    <SfButton class="sf-button--text action__element" :disabled="(componentLoading || loading) && !!activeArtifact" @click="download(artifact)">
                      {{ $t('Download') }}
                    </SfButton>
                    <SfButton class="sf-button--text action__element" :disabled="(componentLoading || loading) && !!activeArtifact" @click="onManualRemove(artifact)">
                      {{ $t('Delete') }}
                    </SfButton>
                  </span>
                </SfLoader>
              </SfTableData>
            </SfTableRow>
          </SfTableRow>
        </SfTable>
      </div>
      <div v-else>
        <div class="top-buttons">
          <SfButton class="sf-button--primary" @click="handleListingClick()" :disabled="!!numeraiError.getModels || !userGetters.getNumeraiApiKeyPublicId(user) || numeraiLoading || userLoading">
            {{ $t('New Listing') }}
          </SfButton>
          <SfButton class="sf-button" v-if="!userGetters.getNumeraiApiKeyPublicId(user)" :class="!userGetters.getNumeraiApiKeyPublicId(user)?'color-primary':'color-secondary'" @click="$router.push('/my-account/numerai-api')" :disabled="numeraiLoading || userLoading">
            {{ !userGetters.getNumeraiApiKeyPublicId(user)?$t('Set Numerai API Key'):$t('Change Numerai API Key') }}
          </SfButton>
        </div>
        <p class="message" v-if="numeraiError.getModels">
          {{ numeraiError.getModels }}
        </p>
        <div v-if="products.length === 0" class="no-listings">
          <p class="no-listings__title">{{ $t('You currently have no listings') }}</p>
        </div>
        <SfTable v-else class="listings">
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
            <SfTableData><span :style="productGetters.getIsActive(product) ? '' : 'color: var(--c-text-disabled)'">{{ productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, 0), true) }}</span></SfTableData>
            <SfTableData class="listings__view listings__element--right">
              <div class="listing-actions">
                <SfButton class="sf-button--text action__element" @click="currentListing = product" v-if="!!productGetters.getOrderedOptions(product) && productGetters.getOrderedOptions(product).filter((p)=>p.is_on_platform).length > 0" :disabled="!!numeraiError.getModels || !userGetters.getNumeraiApiKeyPublicId(user) || numeraiLoading || userLoading">
                  {{ $t('Artifacts') }}
                </SfButton>
                <SfButton class="sf-button--text action__element" @click="handleListingClick(product)" :disabled="!!numeraiError.getModels || !userGetters.getNumeraiApiKeyPublicId(user) || numeraiLoading || userLoading">
                  {{ $t('Edit') }}
                </SfButton>
              </div>
            </SfTableData>
          </SfTableRow>
        </SfTable>
      </div>
    </SfTab>
  </SfTabs>
</template>

<script>
import {
  SfButton,
  SfLink,
  SfNotification,
  SfProperty,
  SfTable,
  SfTabs
} from '@storefront-ui/vue';
import {
  artifactGetters,
  orderGetters,
  productGetters,
  useCategory,
  useGlobals,
  useNumerai,
  useOrderArtifact,
  useProduct,
  useUser,
  useUserOrder,
  userGetters
} from '@vue-storefront/numerbay';
import { computed, ref } from '@vue/composition-api';
import { AgnosticOrderStatus } from '@vue-storefront/core';
import ArtifactPanel from '../../components/Molecules/ArtifactPanel';
import NumeraiApiForm from '../../components/MyAccount/NumeraiApiForm';
import { onSSR } from '@vue-storefront/core';
import { useUiState } from '~/composables';

export default {
  name: 'MyListings',
  components: {
    SfTabs,
    SfTable,
    SfButton,
    SfProperty,
    SfLink,
    SfNotification,
    NumeraiApiForm,
    ArtifactPanel
  },
  methods: {
    getFilteredOrders(product) {
      if (product) {
        return this.orders.filter((o)=>o?.product?.id === product?.id);
      }
      return [];
    },
    async onManualRemove(artifact) {
      await this.deleteArtifact({artifactId: artifact.id});
    }
  },
  mounted() {
    if (this.userGetters.getNumeraiApiKeyPublicId(this.user)) {
      this.getNumeraiModels();
    }
  },
  setup() {
    const { user, loading: userLoading } = useUser();
    const { deleteArtifact } = useOrderArtifact('my-listings');
    const { categories, search: categorySearch } = useCategory();
    const { getModels: getNumeraiModels, loading: numeraiLoading, error: numeraiError } = useNumerai('my-listings');
    const { getGlobals } = useGlobals();

    onSSR(async () => {
      await categorySearch(); // {slug: 'all'}
    });
    const { products, search } = useProduct('products');
    const { orders, search: orderSearch } = useUserOrder('order-history');
    const { toggleListingModal } = useUiState();
    const currentListing = ref(null);

    const handleListingClick = async (product) => {
      toggleListingModal(product);
    };

    onSSR(async () => {
      await search({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
      await getGlobals();
      await orderSearch({ role: 'seller' });
    });

    const tableHeaders = [
      'Product Name',
      'Category',
      'Default Price',
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

    return {
      tableHeaders,
      numeraiLoading,
      userLoading,
      getNumeraiModels,
      user: computed(() => user?.value ? user.value : null),
      categories: computed(() => categories?.value ? categories.value : []),
      products: computed(() => products?.value?.data ? products.value.data : []),
      orders: computed(() => orders?.value?.data ? orders.value.data : []),
      getStatusTextClass,
      handleListingClick,
      artifactGetters,
      userGetters,
      productGetters,
      orderGetters,
      currentListing,
      numeraiError,
      deleteArtifact
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
.no-listings {
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
.listings {
  @include for-desktop {
    &__element {
      &--right {
        --table-column-flex: 0;
        text-align: right;
      }
    }
  }
}
.all-listings {
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
.listing-actions {
  display: flex; flex-direction: row;
  .action__element {
    @include for-desktop {
      flex: 1;
      margin-left: var(--spacer-2xs);
      margin-right: var(--spacer-2xs);
    }

    &:last-child {
      margin-right: 0;
    }
  }
}
</style>
