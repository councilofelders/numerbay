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
        name="Rounds"
        :value="`${orderGetters.getRound(order)}-${parseInt(orderGetters.getRound(order))+parseInt(orderGetters.getItemQty(order))-1}`"
        class="sf-property--full-width property"
        v-if="orderGetters.getProduct(order).category.is_per_round && parseInt(orderGetters.getItemQty(order)) > 1"
      />
      <SfProperty
        name="Round"
        :value="orderGetters.getRound(order)"
        class="sf-property--full-width property"
        v-else
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
        name="Submit to Model"
        :value="orderGetters.getSubmitModelName(order)"
        class="sf-property--full-width property"
      />
      <SfProperty
        name="From Address"
        :value="orderGetters.getFromAddress(order)"
        class="sf-property--full-width property"
      >
        <template #value="{props}">
          <span class="sf-property__value">
            <span class="desktop-only">{{props.value}}</span>
            <span class="smartphone-only">{{`${props.value.slice(0, 2)}...${props.value.slice(-10, -1)}`}}</span>
          </span>
        </template>
      </SfProperty>
      <SfProperty
        name="To Address"
        :value="orderGetters.getToAddress(order)"
        class="sf-property--full-width property"
      >
        <template #value="{props}">
          <span class="sf-property__value">
            <span class="desktop-only">{{props.value}}</span>
            <span class="smartphone-only">{{`${props.value.slice(0, 2)}...${props.value.slice(-10, -1)}`}}</span>
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
            <SfLink :href="`https://etherscan.io/tx/${orderGetters.getTransactionHash(order)}`" target="_blank" class="desktop-only">{{orderGetters.getTransactionHash(order)}}</SfLink>
            <SfLink :href="`https://etherscan.io/tx/${orderGetters.getTransactionHash(order)}`" target="_blank" class="smartphone-only">{{`${orderGetters.getTransactionHash(order).slice(0, 2)}...${orderGetters.getTransactionHash(order).slice(-12, -1)}`}}</SfLink>
          </span>
          <span class="sf-property__value" v-else>
            waiting
          </span>
        </template>
      </SfProperty>
      <SfProperty
        name="Order Status"
        :value="orderGetters.getStatus(order)"
        class="sf-property--full-width property"
      />
      <SfProperty
        v-if="orderGetters.getStatus(order) === 'confirmed'"
        name="Submission Status"
        :value="orderGetters.getSubmissionStatus(order)"
        class="sf-property--full-width property"
      />
      <SfProperty
        v-if="orderGetters.getStatus(order) === 'confirmed'"
        name="Stake Limit"
        :value="orderGetters.getStakeLimit(order)"
        class="sf-property--full-width property"
      />
    </div>
    <SfTable class="orders" v-if="artifacts && orderGetters.getStatus(order)=='confirmed' && !order.buyer_public_key">
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
      <SfTableRow v-if="artifacts && artifacts.total===0">Please wait for the seller to upload artifacts after the round opens</SfTableRow>
      <SfTableRow v-for="artifact in artifacts.data" :key="artifactGetters.getId(artifact)">
        <SfTableData>{{ artifactGetters.getId(artifact) }}</SfTableData>
        <SfTableData><span style="word-break: break-all;">{{ artifactGetters.getObjectName(artifact) }}</span></SfTableData>
        <SfTableData>{{ artifactGetters.getDescription(artifact) }}</SfTableData>
        <SfTableData class="orders__view orders__element--right">
          <SfLoader :class="{ loader: loading }" :loading="loading">
            <span class="artifact-actions">
              <SfButton class="sf-button--text action__element" @click="download(artifact)" v-if="order.mode === 'file'">
                {{ $t('Download') }}
              </SfButton>
              <SfButton class="sf-button--text action__element" @click="submit(artifact)" v-if="!!artifact && !!artifact.object_name && !!order.submit_model_id">
                {{ $t('Submit') }}
              </SfButton>
            </span>
          </SfLoader>
        </SfTableData>
      </SfTableRow>
    </SfTable>

    <SfTable class="orders" v-if="orderArtifacts && orderGetters.getStatus(order)=='confirmed' && !!order.buyer_public_key">
      <SfTableHeading>
        <SfTableHeader
          v-for="tableHeader in ['Name', 'Action']"
          :key="tableHeader"
          >{{ tableHeader }}</SfTableHeader>
      </SfTableHeading>
      <SfTableRow v-if="orderArtifacts && orderArtifacts.total===0">Please wait for the seller to upload artifacts after the round opens</SfTableRow>
      <SfTableRow v-for="artifact in orderArtifacts.data" :key="artifactGetters.getId(artifact)">
        <SfTableData><span style="word-break: break-all;">{{ artifactGetters.getObjectName(artifact) }}</span></SfTableData>
        <SfTableData class="orders__view orders__element--right">
          <SfLoader :class="{ loader: loading }" :loading="loading">
            <span class="artifact-actions" v-if="!downloadingArtifacts.includes(artifactGetters.getId(artifact)) && !decryptingArtifacts.includes(artifactGetters.getId(artifact))">
              <SfButton class="sf-button--text action__element" @click="downloadAndDecrypt(artifact)" v-if="order.mode === 'file'">
                {{ $t('Download') }}
              </SfButton>
              <SfButton class="sf-button--text action__element" @click="submit(artifact)" v-if="!!artifact && !!artifact.object_name && !!order.submit_model_id">
                {{ $t('Submit') }}
              </SfButton>
            </span>
            <span class="artifact-actions" v-else>
              <span v-if="downloadingArtifacts.includes(artifactGetters.getId(artifact))" style="display: flex;" class="action__element"><SfLoader class="loader" :loading="true"/>Downloading {{ (downloadingProgress[artifact.id] || 0).toFixed(1)}}%</span>
              <span v-if="decryptingArtifacts.includes(artifactGetters.getId(artifact))" style="display: flex;" class="action__element"><SfLoader class="loader" :loading="true"/>Decrypting</span>
            </span>
          </SfLoader>
        </SfTableData>
      </SfTableRow>
    </SfTable>
  </div>
</template>

<script>
import { SfButton, SfLink, SfLoader, SfProperty, SfTable } from '@storefront-ui/vue';
import { artifactGetters, orderGetters, useOrderArtifact, useProductArtifact } from '@vue-storefront/numerbay';
import { computed, ref } from '@vue/composition-api';
import axios from 'axios';
import { decodeBase64 } from 'tweetnacl-util';
import nacl from 'tweetnacl';
import { useUiNotification } from '~/composables';
nacl.sealedbox = require('tweetnacl-sealedbox-js');

// decryption
function readfile(file) {
  // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
  return new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.onload = () => {
      resolve(fr.result);
    };
    fr.readAsArrayBuffer(file);
  });
}

export default {
  name: 'OrderInfoPanel',
  components: {
    SfProperty,
    SfButton,
    SfTable,
    SfLoader,
    SfLink
  },
  props: {
    order: {
      default: null
    },
    publicKey: {
      default: null
    },
    encryptedPrivateKey: {
      default: null
    },
    withCopyButtons: {
      default: false
    }
  },
  data() {
    return {
      downloadingProgress: {}
    };
  },
  methods: {
    onProgress(artifact, progress) {
      this.$set(this.downloadingProgress, artifact.id, progress);
    },
    async copyToClipboard(text) {
      try {
        await this.$copyText(text);
      } catch (e) {
        console.error('Copy failed: ', e);
      }
    },
    async download(artifact) {
      if (!artifact.object_name && artifact.url) {
        window.open(artifact.url, '_blank');
        return;
      }

      const downloadUrl = await this.downloadArtifact({productId: this.order.product.id, artifactId: artifact.id});
      if (this.orderArtifactError.downloadArtifact) {
        this.send({
          message: this.orderArtifactError.downloadArtifact.message,
          type: 'danger'
        });
        return;
      }

      const filename = downloadUrl.split('/').pop().split('#')[0].split('?')[0];
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      link.click();
    },
    async decryptfile(objFile) {
      const cipherbytes = await readfile(objFile)
        .catch((err) => {
          console.error(err);
        });

      const privateKeyStr = await window.ethereum.request({
        method: 'eth_decrypt',
        params: [this.encryptedPrivateKey, window.ethereum.selectedAddress]
      });

      const privateKey = new Uint8Array(privateKeyStr.split(',').map((item) => parseInt(item)));

      const plaintextbytes = nacl.sealedbox.open(new Uint8Array(cipherbytes), decodeBase64(this.publicKey), privateKey);

      if (!plaintextbytes) {
        console.log('Error decrypting file.');
      }

      console.log('ciphertext decrypted');

      const blob = new Blob([plaintextbytes], {type: 'application/download'});
      const blobUrl = URL.createObjectURL(blob);

      // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
      return new Promise((resolve, reject) => {
        resolve(blobUrl);
      });
    },
    async downloadAndDecrypt(artifact) {
      if (!artifact.object_name && artifact.url) {
        window.open(artifact.url, '_blank');
        return;
      }
      this.activeArtifact = artifact;
      const downloadUrl = await this.downloadOrderArtifact({artifactId: artifact.id});
      this.activeArtifact = null;
      if (this.error.downloadArtifact) {
        this.send({
          message: this.error.downloadArtifact.message,
          type: 'danger'
        });
        return;
      }

      this.downloadingArtifacts.push(artifact.id);
      axios.get(downloadUrl, {
        responseType: 'blob',
        headers: {'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/octet-stream'},
        onDownloadProgress: progressEvent => {
          const total = parseFloat(progressEvent.total);
          const current = parseFloat(progressEvent.loaded);
          const percentCompleted = current / total * 100;
          this.onProgress(artifact, percentCompleted);
        }
      })
        .then(response => {
          const filename = downloadUrl.split('/').pop().split('#')[0].split('?')[0];
          const blob = new Blob([response.data]);
          const file = new File([blob], filename);
          this.downloadingArtifacts = this.downloadingArtifacts.filter((id)=>id !== artifact.id);
          this.decryptingArtifacts.push(artifact.id);
          this.decryptfile(file).then((blobUrl) => {
            const link = document.createElement('a');
            link.href = blobUrl;
            link.download = filename;
            link.click();
            URL.revokeObjectURL(link.href);
          }).catch((e)=>{
            console.error(e);
          }).finally(()=>{
            this.decryptingArtifacts = this.decryptingArtifacts.filter((id)=>id !== artifact.id);
          });
        }).catch((e)=>{
          console.error(e);
        }).finally(()=>{
          this.downloadingArtifacts = this.downloadingArtifacts.filter((id)=>id !== artifact.id);
          this.downloadingProgress[artifact.id] = 0;
        });
    },
    async submit(artifact) {
      await this.submitArtifact({orderId: this.order.id, artifactId: artifact.id});
      if (this.error.submitArtifact) {
        this.send({
          message: this.error.submitArtifact.message,
          type: 'danger'
        });
      }
    }
  },
  // eslint-disable-next-line no-unused-vars,@typescript-eslint/explicit-module-boundary-types,@typescript-eslint/no-unused-vars
  setup(props, { emit }) {
    const { artifacts, search, downloadArtifact, submitArtifact, loading, error } = useProductArtifact(`${props.order.product.id}`);
    const { artifacts: orderArtifacts, search: searchOrderArtifacts, downloadArtifact: downloadOrderArtifact,
      submitArtifact: submitOrderArtifact, loading: orderArtifactLoading, error: orderArtifactError } = useOrderArtifact(`${props.order.id}`);
    const { send } = useUiNotification();

    search({ productId: props.order.product.id });
    searchOrderArtifacts({ orderId: props.order.id });

    const downloadingArtifacts = ref([]);
    const decryptingArtifacts = ref([]);

    const tableHeaders = [
      'Artifact ID',
      'Name',
      'Description',
      // 'Size',
      'Action'
    ];

    return {
      tableHeaders,
      artifacts: computed(() => artifacts ? artifacts.value : null),
      orderArtifacts: computed(() => orderArtifacts ? orderArtifacts.value : null),
      loading,
      orderArtifactLoading,
      error,
      orderArtifactError,
      send,
      downloadArtifact,
      downloadOrderArtifact,
      submitArtifact,
      submitOrderArtifact,
      orderGetters,
      artifactGetters,
      downloadingArtifacts,
      decryptingArtifacts
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
.artifact-actions {
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
