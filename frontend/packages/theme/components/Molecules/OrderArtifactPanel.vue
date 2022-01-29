<template>
  <div>
    <div class="highlighted highlighted--total">
        <multiple-dropzone :key="componentKey" id="foo" ref="foo" :options="dropzoneOptions" :awss3="gcs" :destroyDropzone="false"
          v-on:vdropzone-error="s3UploadError"
          v-on:vdropzone-success="s3UploadSuccess"
          v-on:vdropzone-total-upload-progress="s3TotalUploadProgress"
          v-on:vdropzone-queue-complete="s3UploadAllComplete"
          v-on:vdropzone-removed-file="onRemove"
          v-on:vdropzone-file-added="onFileAdd"
        >
          Drop files here to upload<br/>An encrypted copy will be added for each active order<br/>Allowed extentions: {{this.dropzoneOptions.acceptedFiles}}
        </multiple-dropzone>
    </div>

    <SfNotification
      visible
      :persistent="true"
      title=""
      message="You still have active orders for unencrypted sales, files will be not be encrypted for those orders."
      type="warning"
      v-if="hasUnencryptedOrder()"
    >
      <template #icon>
        <SfIcon
          class="sf-notification__icon"
          icon="info_shield"
          size="lg"
          color="white"
        />
      </template>
      <template #close><span></span></template>
    </SfNotification>
    <SfNotification
      visible
      :persistent="true"
      title=""
      message="Files will be encrypted in your browser before upload for each active order."
      type="success"
      v-else
    >
      <template #icon>
        <SfIcon
          class="sf-notification__icon"
          icon="safety"
          size="lg"
          color="white"
        />
      </template>
      <template #close><span></span></template>
    </SfNotification>

    <SfTable class="orders" v-if="artifacts">
      <SfTableHeading>
        <SfTableHeader>Upload for Order</SfTableHeader>
        <SfTableHeader>Buyer</SfTableHeader>
        <SfTableHeader>Files Uploaded</SfTableHeader>
      </SfTableHeading>
      <SfTableRow v-if="orders && orders.length===0">No active order to upload for</SfTableRow>
      <SfTableRow v-for="order in orders" :key="orderGetters.getId(order)" :class="isPendingUpload(order) ? 'upload-warning' : ''">
        <SfTableData>
          <div style="display: flex;">
            <SfCheckbox @change="toggleUploadOrder(orderGetters.getId(order))"
                        :selected="uploadOrders && uploadOrders.includes(orderGetters.getId(order))" :name="String(orderGetters.getId(order))"
                        :key="orderGetters.getId(order)"></SfCheckbox>&nbsp;{{ orderGetters.getId(order) }}<span v-if="!order.buyer_public_key">&nbsp;(Unencrypted)</span></div>
        </SfTableData>
        <SfTableData>{{ orderGetters.getBuyer(order) }}</SfTableData>
        <SfTableData>
          {{ (!order.buyer_public_key) ? artifacts.total : getOrderArtifacts(order).length}} / {{getMaxOrderArtifactsCount()}}
        </SfTableData>
      </SfTableRow>
    </SfTable>

    <SfTable class="orders" v-if="getAllOrderArtifacts() && orders && orders.length > 0 && artifacts">
      <SfTableHeading>
        <SfTableHeader
          v-for="tableHeader in ['Order ID', 'File Name', 'State', 'Action']"
          :key="tableHeader"
          >{{ tableHeader }}</SfTableHeader>
      </SfTableHeading>
      <SfTableRow v-if="getAllOrderArtifacts() && getAllOrderArtifacts().length===0 && (!artifacts.data || artifacts.data.length===0)">Please upload artifacts after the round opens</SfTableRow>
      <SfTableRow v-for="artifact in getAllOrderArtifacts()" :key="artifactGetters.getId(artifact)">
        <SfTableData>{{ artifact.order_id }}</SfTableData>
        <SfTableData><span style="word-break: break-all;">{{ artifactGetters.getObjectName(artifact) }}</span></SfTableData>
        <SfTableData><span :class="getStatusTextClass(artifact)">{{ artifact.state }}</span></SfTableData>
        <SfTableData class="orders__view orders__element--right">
          <SfLoader :class="{ loader: orderArtifactLoading && isActiveArtifact(artifact) }" :loading="orderArtifactLoading && isActiveArtifact(artifact)">
            <span class="artifact-actions">
              <SfButton class="sf-button--text action__element" :disabled="(componentLoading || loading) && isActiveArtifact(artifact)" @click="downloadEncrypted(artifact)">
                {{ $t('Download') }}
              </SfButton>
              <SfButton class="sf-button--text action__element" :disabled="(componentLoading || loading) && isActiveArtifact(artifact)" @click="onManualRemoveOrderArtifact(artifact)">
                {{ $t('Delete') }}
              </SfButton>
            </span>
          </SfLoader>
        </SfTableData>
      </SfTableRow>
      <SfTableRow v-for="artifact in artifacts.data" :key="artifactGetters.getId(artifact)">
        <SfTableData>(Unencrypted)</SfTableData>
        <SfTableData><span style="word-break: break-all;">{{ artifactGetters.getObjectName(artifact) }}</span></SfTableData>
        <SfTableData><span :class="getStatusTextClass(artifact)">{{ artifact.state }}</span></SfTableData>
        <SfTableData class="orders__view orders__element--right">
          <SfLoader :class="{ loader: loading && isActiveArtifact(artifact) }" :loading="loading && isActiveArtifact(artifact)">
            <span class="artifact-actions">
              <SfButton class="sf-button--text action__element" :disabled="(componentLoading || loading) && isActiveArtifact(artifact)" @click="download(artifact)">
                {{ $t('Download') }}
              </SfButton>
              <SfButton class="sf-button--text action__element" :disabled="(componentLoading || loading) && isActiveArtifact(artifact)" @click="onManualRemove(artifact)">
                {{ $t('Delete') }}
              </SfButton>
            </span>
          </SfLoader>
        </SfTableData>
      </SfTableRow>
    </SfTable>
  </div>
</template>

<script>
import { SfButton, SfCheckbox, SfIcon, SfInput, SfLoader, SfNotification, SfTable } from '@storefront-ui/vue';
import { ValidationObserver, ValidationProvider, extend } from 'vee-validate';
import {
  artifactGetters,
  orderGetters,
  useOrderArtifact,
  useProductArtifact,
  useUserOrder
} from '@vue-storefront/numerbay';
import { computed, ref } from '@vue/composition-api';
import { Logger } from '@vue-storefront/core';
import MultipleDropzone from '../../components/Molecules/MultipleDropzone';
import { useUiNotification } from '~/composables';

import { decodeBase64 } from 'tweetnacl-util';
import nacl from 'tweetnacl';
nacl.sealedbox = require('tweetnacl-sealedbox-js');

import 'nuxt-dropzone/dropzone.css';
import { generateSignedUrl } from '../../plugins/gcs';

extend('url', {
  validate: (value) => {
    if (value) {
      // eslint-disable-next-line
      return /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(value);
    }

    return false;
  },
  message: 'This must be a valid URL'
});

const readfile = (file) => {
  // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
  return new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.onload = () => {
      resolve(fr.result);
    };
    fr.readAsArrayBuffer(file);
  });
};

// const encryptfile = async (objFile, key) => {
//   const plaintextbytes = await readfile(objFile)
//     .catch((err) => {
//       console.error(err);
//     });
//
//   const cipherbytes = JSON.stringify(encrypt(
//     key,
//     { data: encodeBase64(new Uint8Array(plaintextbytes)) },
//     'x25519-xsalsa20-poly1305'
//   ));
//
//   if (!cipherbytes) {
//     console.error('Error encrypting file.');
//   }
//
//   const blob = new Blob([cipherbytes], {type: 'application/download'});
//   // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
//   return new Promise((resolve, reject) => {
//     resolve(new File([blob], objFile.name));
//   });
// };

const encryptfile = async (objFile, key) => {
  const plaintextbytes = await readfile(objFile)
    .catch((err) => {
      console.error(err);
    });

  const cipherbytes = nacl.sealedbox.seal(new Uint8Array(plaintextbytes), decodeBase64(key));

  if (!cipherbytes) {
    console.error('Error encrypting file.');
  }

  const blob = new Blob([cipherbytes], {type: 'application/download'});
  // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
  return new Promise((resolve, reject) => {
    resolve(new File([blob], objFile.name));
  });
};

export default {
  name: 'OrderArtifactPanel',
  components: {
    SfButton,
    SfCheckbox,
    SfIcon,
    SfInput,
    SfLoader,
    SfNotification,
    SfTable,
    MultipleDropzone,
    ValidationProvider,
    ValidationObserver
  },
  data() {
    // eslint-disable-next-line @typescript-eslint/no-this-alias,consistent-this
    const vm = this;
    return {
      uploadOrders: [],
      componentKey: 0,
      componentLoading: false,
      gcs: {
        unencryptedSigningURL: vm.$root.context.$vsf.$numerbay.api.getArtifactUploadUrl,
        signingURL: vm.$root.context.$vsf.$numerbay.api.getOrderArtifactUploadUrl,
        params: {
          productId: vm.product.id
        },
        headers: {
          Authorization: `Bearer ${this.$cookies.get('nb-token')}`
          // 'Cache-Control': 'no-cache'
        },
        sendFileToServer: false,
        withCredentials: false
      },
      // See https://rowanwins.github.io/vue-dropzone/docs/dist/index.html#/props
      dropzoneOptions: {
        // paramName: 'file_obj',
        // url: `http://${process.env.VUE_APP_DOMAIN_DEV || 'localhost'}/backend-api/v1/products/15/artifacts`,
        url: this.generateUploadUrl, // placeholder url
        method: 'put',
        addRemoveLinks: true,
        timeout: 600000,
        // parallelUploads: 1,
        createImageThumbnails: false,
        maxFilesize: 2000,
        acceptedFiles: '.txt,.csv,.parquet,.zip,.ipynb',
        // renameFile(file) {
        //   return file.renameFilename = `${vm.product.sku}_${'xxxxxxxx-xxxx-xxxx-xxxxxxxxxxxx'.replace(/[x]/g, () => {
        //     const random = Math.floor(Math.random() * 16);
        //     return random.toString(16);
        //   })}.${file.name.split('.').pop()}`;
        // },
        headers: {
          'Content-Type': 'application/octet-stream'
          // 'Access-Control-Request-Headers': 'Content-Type'
          // 'Access-Control-Allow-Origin': '*',
          // 'Cache-Control': 'no-cache'
          // Authorization: `Bearer ${this.$cookies.get('nb-token')}`
        }
      }
    };
  },
  props: {
    product: {
      default: null
    },
    withCopyButtons: {
      default: false
    },
    orders: {
      default: null
    }
  },
  watch: {
    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    orders(orders) {
      this.resetUploadOrders();
    },
    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    artifacts(artifacts) {
      this.resetUploadOrders();
    }
  },
  methods: {
    generateUploadUrl(file) {
      const signedUrlPromise = generateSignedUrl(file[0].isUnencrypted ? this.gcs.unencryptedSigningURL : this.gcs.signingURL, this.gcs.params, file[0]).then((signed)=>{
        if (signed.error) {
          const {send} = useUiNotification();
          send({
            message: signed.detail,
            type: 'danger'
          });
        }
        // eslint-disable-next-line no-use-before-define
        this.$refs.foo.setOption('headers', {
          'Content-Type': 'application/octet-stream'
          // 'x-amz-acl': 'public-read'
        });
        file[0].artifactId = signed.id;
        return signed.url;
      });
      return signedUrlPromise;
    },
    isActiveArtifact(artifact) {
      return this.activeArtifacts && this.activeArtifacts.includes(artifact.id);
    },
    async download(artifact) {
      if (!artifact.object_name && artifact.url) {
        window.open(artifact.url, '_blank');
        return;
      }
      this.activeArtifact = artifact;
      this.activeArtifacts.push(artifact.id);
      const downloadUrl = await this.downloadArtifact({productId: artifact.product_id, artifactId: artifact.id});
      this.activeArtifact = null;
      this.activeArtifacts = this.activeArtifacts.filter((id)=>id !== artifact.id);
      if (this.error.downloadArtifact) {
        this.send({
          message: this.error.downloadArtifact.message,
          type: 'danger'
        });
        return;
      }

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
    },
    async onManualRemove(artifact) {
      this.activeArtifact = artifact;
      this.activeArtifacts.push(artifact.id);
      this.componentLoading = true;
      try {
        this.$refs.foo.disable();
        await this.deleteArtifact({productId: this.product.id, artifactId: artifact.id}).then(() => {
          if (this.error.deleteArtifact) {
            this.send({
              message: this.error.deleteArtifact.message,
              type: 'danger'
            });
          }
        });
        this.componentKey += 1;
        await this.search({ productId: this.product.id });
      } finally {
        this.$refs.foo.enable();
        this.componentLoading = false;
        this.activeArtifact = null;
        this.activeArtifacts = this.activeArtifacts.filter((id)=>id !== artifact.id);
      }
    },
    hasUnencryptedOrder() {
      return this.orders.filter(o=>!o.buyer_public_key).length > 0;
    },
    filterUploadOrders(orders) {
      return orders.filter(o=>this.uploadOrders.includes(o.id));
    },
    toggleUploadOrder(orderId) {
      if (this.uploadOrders.includes(orderId)) {
        this.uploadOrders = this.uploadOrders.filter(id=>id !== orderId);
      } else {
        this.uploadOrders.push(orderId);
      }
    },
    resetUploadOrders() {
      this.uploadOrders = [];
      for (const order of this.orders) {
        if (this.isPendingUpload(order)) {
          // order.isSelected = [String(this.orderGetters.getId(order))];
          this.uploadOrders.push(this.orderGetters.getId(order));
        }
      }
      if (this.uploadOrders.length === 0) {
        this.uploadOrders = this.orders.map(o=>this.orderGetters.getId(o));
      }
    },
    isPendingUpload(order) {
      if (order.buyer_public_key) {
        return (this.getOrderArtifacts(order).length === 0) || this.getOrderArtifacts(order).length < this.getMaxOrderArtifactsCount();
      } else {
        return !this.artifacts?.total || this.artifacts?.total < this.getMaxOrderArtifactsCount();
      }
    },
    getOrderArtifacts(order) {
      return this.orders.filter(o=>(o.id === order.id)).map(o=>o.artifacts).flat() || [];
    },
    getMaxOrderArtifactsCount() {
      return Math.max.apply(null, this.orders.map(o=>o.artifacts?.length));
    },
    getAllOrderArtifacts() {
      return this.orders.map(o=>o.artifacts).flat();
    },
    onFileAdd(file) {
      if (!file.isSubtask) {
        // this.$refs.foo.dropzone.cancelUpload(file);
        if (file.status === 'uploading') {
          if (typeof file.xhr !== 'undefined') {
            file.xhr.abort();
          }
        } else if (
          file.status === 'added' ||
          file.status === 'queued'
        ) {
          file.status = 'canceled';
        }
        this.$refs.foo.dropzone.files = this.$refs.foo.dropzone.files.filter((f)=>f !== file).map((f)=>f);
        // console.log('this.$refs.foo.dropzone.files', JSON.stringify(this.$refs.foo.dropzone.files));
        // this.$refs.foo.dropzone.updateTotalUploadProgress();
        this.$refs.foo.dropzone.emit('removedfile', file);
        if (!this.orders || this.orders.length === 0) {
          this.send({
            message: 'Upload cancelled, no active order to upload for',
            type: 'warning'
          });
          return;
        }
        let hasUnencrypted = false;
        for (const order of this.filterUploadOrders(this.orders)) {
          // if (!order.buyer_public_key) {
          //   continue;
          // }
          if (order.buyer_public_key) {
            encryptfile(file, order.buyer_public_key).then((newFile) => {
              newFile.isSubtask = true;
              newFile.orderId = order.id;
              this.$refs.foo.addFile(newFile);
            });
          } else {
            hasUnencrypted = true;
          }
        }
        if (hasUnencrypted) {
          const newFile = new File([file], file.name);
          newFile.isSubtask = true;
          newFile.isUnencrypted = true;
          this.$refs.foo.addFile(newFile);
        }
      }
    },
    async downloadEncrypted(artifact) {
      if (!artifact.object_name && artifact.url) {
        window.open(artifact.url, '_blank');
        return;
      }
      this.activeArtifact = artifact;
      this.activeArtifacts.push(artifact.id);
      const downloadUrl = await this.downloadOrderArtifact({artifactId: artifact.id});
      this.activeArtifact = null;
      this.activeArtifacts = this.activeArtifacts.filter((id)=>id !== artifact.id);
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
    onUploadError(file, message, xhr) {
      console.error('Upload Error: ', message, file, xhr);
    },
    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    // onSending(file, xhr, formData) {
    //   Logger.debug('sending', file)
    //   const _send = xhr.send;
    //   xhr.send = () => {
    //     _send.call(xhr, file);
    //   };
    // },
    async s3TotalUploadProgress(progress) {
      if (progress === 100) {
        this.componentLoading = true;
      }
    },
    // async s3UploadProgress(file, progress, bytesSent) {
    //   // console.log(file.artifactId, progress, bytesSent);
    //   // if (progress === 100) {
    //   //   this.componentLoading = true;
    //   // }
    // },
    async s3UploadAllComplete() {
      // if (this.componentLoading) {
      //   try {
      //     this.$refs.foo.disable();
      //     this.componentKey += 1;
      //     await this.search({ productId: this.product.id });
      //     await this.orderSearch({ role: 'seller', filters: { active: true} });
      //   } finally {
      //     this.$refs.foo.enable();
      //     this.componentLoading = false;
      //   }
      // }
      this.resetUploadOrders();
    },
    async s3UploadSuccess(file) {
      Logger.debug('Upload success', file.artifactId);
      let response = null;
      if (file.isUnencrypted) {
        response = await this.$root.context.$vsf.$numerbay.api.validateArtifactUpload({productId: this.product.id, artifactId: file.artifactId});
      } else {
        response = await this.$root.context.$vsf.$numerbay.api.validateOrderArtifactUpload({artifactId: file.artifactId});
      }
      Logger.debug('response: ', response);
      await this.search({ productId: this.product.id });
      await this.orderSearch({ role: 'seller', filters: { active: true} });
      // this.resetUploadOrders();
    },
    s3UploadError(file, message, xhr) {
      Logger.error('s3 error', file, message, xhr);
    },
    async onRemove(file, error, xhr) {
      Logger.debug('onRemove', file, error, xhr);
      if (file.isSubtask) {
        if (file.isUnencrypted) {
          await this.deleteArtifact({
            productId: this.product.id,
            artifactId: file.artifactId
          }).then(() => {
            if (this.error.deleteArtifact) {
              this.send({
                message: this.error.deleteArtifact.message,
                type: 'danger'
              });
            }
          });
          this.componentKey += 1;
          await this.search({productId: this.product.id});
        } else {
          await this.deleteOrderArtifact({artifactId: file.artifactId}).then(() => {
            if (this.orderArtifactError.deleteArtifact) {
              this.send({
                message: this.orderArtifactError.deleteArtifact.message,
                type: 'danger'
              });
            }
          });
          this.componentKey += 1;
          await this.search({productId: this.product.id});
        }
      }
    },
    async onManualRemoveOrderArtifact(artifact) {
      this.activeArtifact = artifact;
      this.activeArtifacts.push(artifact.id);
      this.componentLoading = true;
      try {
        this.$refs.foo.disable();
        await this.deleteOrderArtifact({artifactId: artifact.id}).then(() => {
          if (this.orderArtifactError.deleteArtifact) {
            this.send({
              message: this.orderArtifactError.deleteArtifact.message,
              type: 'danger'
            });
          }
        });
        this.componentKey += 1;
        await this.orderSearch({ role: 'seller', filters: { active: true} });
      } finally {
        this.$refs.foo.enable();
        this.componentLoading = false;
        this.activeArtifact = null;
        this.activeArtifacts = this.activeArtifacts.filter((id)=>id !== artifact.id);
      }
    }
  },
  beforeMount() {
    this.resetUploadOrders();
    // Logger.debug('artifacts', this.artifacts)
    //
    // var file = { size: 123, name: "Icon", type: "image/png" };
    // var url = "https://myvizo.com/img/logo_sm.png";
    // this.$refs.foo.manuallyAddFile(file, url);
  },
  // eslint-disable-next-line no-unused-vars,@typescript-eslint/explicit-module-boundary-types,@typescript-eslint/no-unused-vars
  setup(props, { emit, root }) {
    const { artifacts, search, createArtifact, downloadArtifact, deleteArtifact, loading, error } = useProductArtifact(`${props.product.id}`);
    const { downloadArtifact: downloadOrderArtifact, deleteArtifact: deleteOrderArtifact, loading: orderArtifactLoading, error: orderArtifactError } = useOrderArtifact(`${props.product.id}`);
    const { search: orderSearch } = useUserOrder('my-listings');
    const { send } = useUiNotification();

    search({ productId: props.product.id });

    const isManualFormOpen = ref(false);
    const activeArtifact = ref(null);
    const activeArtifacts = ref([]);

    const tableHeaders = [
      'Artifact ID',
      'Name',
      'Description',
      // 'Size',
      'Action'
    ];

    const resetForm = () => ({
      url: null,
      description: null
    });
    const form = ref(resetForm());

    const getStatusTextClass = (artifact) => {
      const status = artifact?.state;
      switch (status) {
        case 'pending':
          return 'text-warning';
        case 'active':
          return 'text-success';
        default:
          return '';
      }
    };

    return {
      artifacts: computed(() => artifacts ? artifacts.value : null),
      createArtifact,
      downloadArtifact,
      downloadOrderArtifact,
      deleteArtifact,
      deleteOrderArtifact,
      loading,
      orderArtifactLoading,
      error,
      orderArtifactError,
      send,
      search,
      tableHeaders,
      activeArtifact,
      activeArtifacts,
      isManualFormOpen,
      form,
      resetForm,
      orderGetters,
      artifactGetters,
      orderSearch,
      getStatusTextClass
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
.top-buttons {
  @include for-desktop {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
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
.upload-warning {
  background-color: #ecc71330;
}
</style>
