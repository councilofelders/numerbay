<template>
  <div>
    <div class="highlighted highlighted--total">
      <SfProperty
        name="Order ID"
        :value="orderGetters.getId(order)"
        class="sf-property--full-width property"
      />
      <SfProperty
        name="Product"
        :value="orderGetters.getItemSku(orderGetters.getProduct(order))"
        class="sf-property--full-width property"
      />
      <SfProperty
        name="Round"
        :value="orderGetters.getRound(order)"
        class="sf-property--full-width property"
      />
      <SfProperty
        name="Date"
        :value="orderGetters.getDate(order)"
        class="sf-property--full-width property"
      />
      <SfProperty
        name="Buyer"
        :value="orderGetters.getBuyer(order)"
        class="sf-property--full-width property"
      />
      <SfProperty
        name="From Address"
        :value="orderGetters.getFromAddress(order)"
        class="sf-property--full-width property"
      />
      <SfProperty
        name="To Address"
        class="sf-property--full-width property"
      >
        <template #value>
          <span class="sf-property__value">
            {{orderGetters.getToAddress(order)}}
          <SfButton
              v-if="withCopyButtons"
              class="sf-button--text"
              @click="copyToClipboard(orderGetters.getToAddress(order))"
          >
            Copy
          </SfButton>
          </span>
        </template>
      </SfProperty>
      <SfProperty
        name="Total"
        class="sf-property--full-width property"
      >
        <template #value>
          <span class="sf-property__value">
            {{orderGetters.getFormattedPrice(order, withCurrency=true, decimals=4)}}
          <SfButton
              v-if="withCopyButtons"
              class="sf-button--text"
              @click="copyToClipboard(orderGetters.getPrice(order))"
          >
            Copy
          </SfButton>
          </span>
        </template>
      </SfProperty>
      <SfProperty
        name="Transaction Hash"
        class="sf-property--full-width property"
      >
        <template #value>
          <span class="sf-property__value" v-if="orderGetters.getTransactionHash(order)" >
            <SfInput :value="orderGetters.getTransactionHash(order)" class="sf-input--outline"></SfInput>
          </span>
          <span class="sf-property__value" v-else>
            waiting
          </span>
        </template>
      </SfProperty>
      <SfProperty
        name="Status"
        :value="orderGetters.getStatus(order)"
        class="sf-property--full-width property"
      />
    </div>
    <SfTable class="orders" v-if="artifacts && artifacts.data">
      <SfTableHeading>
        <SfTableHeader
          v-for="tableHeader in tableHeaders"
          :key="tableHeader"
          >{{ tableHeader }}</SfTableHeader>
        <!--<SfTableHeader class="orders__element&#45;&#45;right">
          <span class="smartphone-only">{{ $t('Download') }}</span>
          <SfButton
            class="desktop-only sf-button&#45;&#45;text orders__download-all"
            @click="downloadOrders()"
          >
            {{ $t('Download all') }}
          </SfButton>
        </SfTableHeader>-->
      </SfTableHeading>
      <SfTableRow v-for="artifact in artifacts.data" :key="artifactGetters.getId(artifact)">
        <SfTableData>{{ artifactGetters.getId(artifact) }}</SfTableData>
        <SfTableData>{{ artifactGetters.getObjectName(artifact) }}</SfTableData>
        <SfTableData>{{ artifactGetters.getObjectSize(artifact) }}</SfTableData>
        <SfTableData class="orders__view orders__element--right">
          <SfLoader :class="{ loader: loading }" :loading="loading">
            <SfButton class="sf-button--text" @click="download(artifact)">
              {{ $t('Download') }}
            </SfButton>
          </SfLoader>
        </SfTableData>
      </SfTableRow>
    </SfTable>
  </div>
</template>

<script>
import {SfProperty, SfIcon, SfButton, SfInput, SfTable, SfLoader} from '@storefront-ui/vue';
import { orderGetters, artifactGetters, useProductArtifact } from '@vue-storefront/numerbay';
import {computed} from '@vue/composition-api';

export default {
  name: 'OrderInfoPanel',
  components: {
    SfProperty,
    SfIcon,
    SfButton,
    SfInput,
    SfTable,
    SfLoader
  },
  props: {
    order: {
      default: null
    },
    withCopyButtons: {
      default: false
    }
  },
  methods: {
    async copyToClipboard(text) {
      try {
        await this.$copyText(text);
      } catch (e) {
        console.error('Copy failed: ', e);
      }
    },
    async download(artifact) {
      const downloadUrl = await this.downloadArtifact({productId: this.order.product.id, artifactId: artifact.id});
      const filename = downloadUrl.split('/').pop().split('#')[0].split('?')[0];
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      link.click();
      // console.log('downloadUrl', downloadUrl);
      // axios.get(downloadUrl, { responseType: 'blob', headers: {'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/octet-stream'} })
      //   .then(response => {
      //     const filename = downloadUrl.split('/').pop().split('#')[0].split('?')[0];
      //     const blob = new Blob([response.data], { type: 'application/pdf' });
      //     const link = document.createElement('a');
      //     link.href = URL.createObjectURL(blob);
      //     link.download = filename;
      //     link.click();
      //     URL.revokeObjectURL(link.href);
      //   }).catch(console.error);
    }
  },
  // eslint-disable-next-line no-unused-vars,@typescript-eslint/explicit-module-boundary-types,@typescript-eslint/no-unused-vars
  setup(props, { emit }) {
    const { artifacts, search, downloadArtifact, loading } = useProductArtifact(`${props.order.product.id}`);
    search({ productId: props.order.product.id });

    const tableHeaders = [
      'Artifact ID',
      'Name',
      'Size',
      'Action'
    ];

    return {
      tableHeaders,
      artifacts: computed(() => artifacts ? artifacts.value : null),
      loading,
      downloadArtifact,
      orderGetters,
      artifactGetters
    };
  }

};
</script>

<style lang="scss" scoped>
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
