<template>
<div class="page-wrap">
    <!-- create -->
    <section class="create-section section-space-b pt-4 pt-md-5 mt-md-4">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="section-head-sm">
                        <router-link :to="`/listings`" class="btn-link fw-semibold"><em class="ni ni-arrow-left"></em> My listings</router-link>
                        <h1 class="mt-2">Manage artifacts</h1>
                    </div>
                </div><!-- end col -->
                <div class="col-lg-8">
                    <form action="#" class="form-create mb-5 mb-lg-0">
                        <div class="form-item mb-4">
                            <h5 class="mb-3">Upload file</h5>
                            <client-only>
                              <multiple-dropzone :key="componentKey" id="foo" ref="foo" :options="dropzoneOptions" :awss3="gcs" :destroyDropzone="false"
                                v-on:vdropzone-error="s3UploadError"
                                v-on:vdropzone-success="s3UploadSuccess"
                                v-on:vdropzone-total-upload-progress="s3TotalUploadProgress"
                                v-on:vdropzone-queue-complete="s3UploadAllComplete"
                                v-on:vdropzone-removed-file="onRemove"
                                v-on:vdropzone-file-added="onFileAdd"
                              >
                                <p class="file-name mb-4" id="file-name">An encrypted copy will be added for each active order<br/>Allowed extentions: {{this.dropzoneOptions.acceptedFiles}}.</p>
                                <input id="file-upload" class="file-upload-input" data-target="file-name" type="file" hidden>
                                <label class="input-label btn btn-dark">Choose File</label>
                              </multiple-dropzone>
                            </client-only>
                        </div><!-- end form-item -->
                        <div class="table-responsive">
                            <table class="table mb-0 table-s2">
                                <thead class="fs-14">
                                    <tr>
                                        <th scope="col" v-for="(list, i) in [
                                          'Upload',
                                          '#',
                                          'Buyer',
                                          'Mode',
                                          'Files Uploaded',
                                          'Numerai Submission'
                                        ]" :key="i">{{ list }}</th>
                                    </tr>
                                </thead>
                                <tbody class="fs-13">
                                    <tr v-if="!orders || orders.length===0"><td colspan="3" class="text-secondary">No active sale order to upload for</td></tr>
                                    <tr v-for="order in orders" :key="orderGetters.getId(order)">
                                        <th scope="row">
                                          <div class="form-check form-switch form-switch-s1">
                                            <input class="form-check-input" type="checkbox"
                                                   @change="toggleUploadOrder(orderGetters.getId(order))"
                                                   :checked="Boolean(uploadOrders && uploadOrders.includes(orderGetters.getId(order)))"
                                                   :name="String(orderGetters.getId(order))"
                                                   :key="orderGetters.getId(order)">
                                          </div>
                                        </th>
                                        <th scope="row"><a href="javascript:void(0);" @click="toggleModal(order)" title="Click for details">{{ orderGetters.getId(order) }}<span v-if="!order.buyer_public_key">&nbsp;(Unencrypted)</span></a></th>
                                        <td>{{ orderGetters.getBuyer(order) }}</td>
                                        <td>{{ order.mode }}</td>
                                        <td>{{ (!order.buyer_public_key) ? filterActiveArtifacts(artifacts.data).length : getUniqueActiveOrderArtifacts(order).length}} / {{getMaxOrderArtifactsCount() }}</td>
                                        <td><span class="badge fw-medium" :class="getSubmissionStatusTextClass(order)">{{ orderGetters.getSubmissionStatus(order) }}</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div><!-- end table-responsive -->
                        <div class="table-responsive mt-4">
                            <table class="table mb-0 table-s2" v-if="artifacts">
                                <thead class="fs-14">
                                    <tr>
                                        <th scope="col" v-for="(list, i) in [
                                          '#',
                                          'File Name',
                                          'State',
                                          'Recipient',
                                          'Action'
                                        ]" :key="i">{{ list }}</th>
                                    </tr>
                                </thead>
                                <tbody class="fs-13">
                                    <tr v-if="(!getAllOrderArtifacts() || getAllOrderArtifacts().length===0) && (!artifacts.data || artifacts.data.length===0)"><td colspan="3" class="text-secondary">Please upload artifacts after the round opens</td></tr>
                                    <tr v-for="artifact in getAllOrderArtifacts()" :key="artifactGetters.getId(artifact)">
                                        <th scope="row">{{ artifact.order_id }}</th>
                                      <td><span class="text-break" style="white-space: normal;"><a href="javascript:void(0);" title="Download not available">{{ artifactGetters.getObjectName(artifact) }}</a></span></td>
                                        <td><span class="badge fw-medium" :class="getStatusTextClass(artifact)">{{ artifact.state }}</span></td>
                                        <td>{{ artifact.is_numerai_direct ? 'Numerai' : 'Buyer' }}</td>
                                        <td>
                                          <div class="d-flex justify-content-between">
                                            <button class="icon-btn ms-auto" title="Delete" @click="onManualRemoveOrderArtifact(artifact)" :disabled="(componentLoading || productArtifactLoading) && isActiveArtifact(artifact)">
                                              <span class="spinner-border spinner-border-sm text-secondary" role="status" v-if="(componentLoading || productArtifactLoading) && isActiveArtifact(artifact)"></span>
                                              <em class="ni ni-trash" v-else></em>
                                            </button>
                                          </div>
                                        </td>
                                    </tr>
                                    <tr v-for="artifact in artifacts.data" :key="artifactGetters.getId(artifact)">
                                        <th scope="row">{{ artifact.order_id }}</th>
                                      <td><span class="text-break" style="white-space: normal;"><a href="javascript:void(0);" @click="download(artifact)" :title="`Download ${artifactGetters.getObjectName(artifact)}`">{{ artifactGetters.getObjectName(artifact) }}</a></span></td>
                                        <td><span class="badge fw-medium" :class="getStatusTextClass(artifact)">{{ artifact.state }}</span></td>
                                        <td></td>
                                        <td>
                                          <div class="d-flex justify-content-between">
                                            <button class="icon-btn ms-auto" title="Delete" @click="onManualRemove(artifact)" :disabled="(componentLoading || productArtifactLoading) && isActiveArtifact(artifact)">
                                              <span class="spinner-border spinner-border-sm text-secondary" role="status" v-if="(componentLoading || productArtifactLoading) && isActiveArtifact(artifact)"></span>
                                              <em class="ni ni-trash" v-else></em>
                                            </button>
                                          </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div><!-- end table-responsive -->
                    </form>
                </div><!-- endn col -->
            </div><!-- row-->
            <OrderInfoModal :order="currentOrder" modelId="orderInfoModal" ref="orderInfoModal"></OrderInfoModal>
        </div><!-- container -->
    </section><!-- create-section -->
</div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import MultipleDropzone from '../components/common/MultipleDropzone';
import SectionData from '@/store/store.js';

// Composables
import {
  artifactGetters,
  orderGetters,
  productGetters,
  useOrderArtifact,
  useProduct,
  useProductArtifact,
  useUserOrder
} from '@vue-storefront/numerbay';
import { computed, ref } from '@vue/composition-api';
import { Logger } from '@vue-storefront/core';
import { useUiNotification } from '~/composables';

import { decodeBase64 } from 'tweetnacl-util';
import nacl from 'tweetnacl';
nacl.sealedbox = require('tweetnacl-sealedbox-js');

import 'nuxt-dropzone/dropzone.css';
import {generateSignedUrl} from '../plugins/gcs';

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
  name: 'ManageArtifacts',
  middleware: [
    'is-authenticated'
  ],
  components: {
    MultipleDropzone
  },
  data () {
    return {
      SectionData,
      currentOrder: {},
      modal: null,
      uploadOrders: [],
      componentKey: 0,
      componentLoading: false,
      gcs: {},
      // See https://rowanwins.github.io/vue-dropzone/docs/dist/index.html#/props
      dropzoneOptions: {
        url: this.generateUploadUrl,
        method: 'put',
        addRemoveLinks: true,
        timeout: 600000,
        // parallelUploads: 1,
        createImageThumbnails: false,
        maxFilesize: 2000,
        acceptedFiles: '.txt,.csv,.parquet,.zip,.ipynb',
        headers: {
          'Content-Type': 'application/octet-stream'
        }
      }
    };
  },
  computed: {
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
    toggleModal(order) {
      this.currentOrder = order;
      this.$refs.orderInfoModal.show();
    },
    generateUploadUrl(file) {
      const signedUrlPromise = generateSignedUrl(file[0].isUnencrypted ? this.gcs.unencryptedSigningURL : this.gcs.signingURL, this.gcs.params, file[0]).then((signed)=>{
        if (signed.error) {
          const {send} = useUiNotification();
          send({
            message: signed.detail,
            type: 'bg-danger',
            icon: 'ni-alert-circle'
          });
        }
        // eslint-disable-next-line no-use-before-define
        this.$refs.foo.setOption('headers', {
          'Content-Type': 'application/octet-stream'
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
      // this.activeArtifact = artifact;
      // this.activeArtifacts.push(artifact.id);
      const downloadUrl = await this.downloadArtifact({productId: artifact.product_id, artifactId: artifact.id});
      // this.activeArtifact = null;
      // this.activeArtifacts = this.activeArtifacts.filter((id)=>id !== artifact.id);
      if (this.error.downloadArtifact) {
        this.send({
          message: this.error.downloadArtifact.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
        return;
      }

      const filename = downloadUrl.split('/').pop().split('#')[0].split('?')[0];
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      link.click();
    },
    async onManualRemove(artifact) {
      this.activeArtifact = artifact;
      this.activeArtifacts.push(artifact.id);
      this.componentLoading = true;
      try {
        this.$refs.foo.disable();
        await this.deleteArtifact({productId: this.id, artifactId: artifact.id}).then(() => {
          if (this.error.deleteArtifact) {
            this.send({
              message: this.error.deleteArtifact.message,
              type: 'bg-danger',
              icon: 'ni-alert-circle'
            });
          }
        });
        this.componentKey += 1;
        await this.productArtifactSearch({ productId: this.id });
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
          this.uploadOrders.push(this.orderGetters.getId(order));
        }
      }
      if (this.uploadOrders.length === 0) {
        this.uploadOrders = this.orders.map(o=>this.orderGetters.getId(o));
      }
    },
    filterActiveArtifacts(artifacts) {
      if (!artifacts) {
        return [];
      }
      return artifacts.filter(a=>a.state === 'active');
    },
    getUniqueActiveOrderArtifacts(order) {
      if (!order?.artifacts) {
        return [];
      }
      if (order.mode === 'file') {
        return order.artifacts.filter(a=>!a.is_numerai_direct).filter(a=>a.state === 'active');
      } else {
        return order.artifacts.filter(a=>a.state === 'active');
      }
    },
    isPendingUpload(order) {
      if (order.buyer_public_key) {
        return (this.getOrderArtifacts(order).length === 0) || this.getUniqueActiveOrderArtifacts(order).length < this.getMaxOrderArtifactsCount();
      } else {
        return !this.artifacts?.total || this.artifacts?.total < this.getMaxOrderArtifactsCount();
      }
    },
    getOrderArtifacts(order) {
      return this.orders.filter(o=>(o.id === order.id)).map(o=>o.artifacts).flat() || [];
    },
    getMaxOrderArtifactsCount() {
      return Math.max.apply(null, this.orders.map(o=>this.getUniqueActiveOrderArtifacts(o)?.length));
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
        // this.$refs.foo.dropzone.updateTotalUploadProgress();
        this.$refs.foo.dropzone.emit('removedfile', file);
        if (this.productGetters.getUseEncryption(this.product) && (!this.orders || this.orders.length === 0)) {
          this.send({
            message: 'Upload cancelled, no active order to upload for',
            type: 'bg-warning',
            icon: 'ni-alert-circle'
          });
          return;
        }
        let hasUnencrypted = !this.productGetters.getUseEncryption(this.product);
        for (const order of this.filterUploadOrders(this.orders)) {
          // if (!order.buyer_public_key) {
          //   continue;
          // }
          if (order.buyer_public_key) {
            if (order.submit_model_id) {
              // direct submission to numerai
              const newFile2 = new File([file], file.name);
              newFile2.isSubtask = true;
              newFile2.isNumeraiDirect = true;
              newFile2.orderId = order.id;
              this.$refs.foo.addFile(newFile2);
            }

            if (order.mode === 'file') {
              encryptfile(file, order.buyer_public_key).then((newFile) => {
                newFile.isSubtask = true;
                newFile.orderId = order.id;
                this.$refs.foo.addFile(newFile);
              });
            }
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
          type: 'bg-danger',
          icon: 'ni-alert-circle'
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
    async s3TotalUploadProgress(progress) {
      if (progress === 100) {
        this.componentLoading = true;
      }
    },
    async s3UploadAllComplete() {
      // if (this.componentLoading) {
      //   try {
      //     this.$refs.foo.disable();
      //     this.componentKey += 1;
      //     await this.productArtifactSearch({ productId: this.id });
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
        response = await this.$root.context.$vsf.$numerbay.api.validateArtifactUpload({productId: this.id, artifactId: file.artifactId});
      } else {
        response = await this.$root.context.$vsf.$numerbay.api.validateOrderArtifactUpload({artifactId: file.artifactId});
      }
      Logger.debug('response: ', response);
      await this.productArtifactSearch({ productId: this.id });
      await this.orderSearch({ role: 'seller', filters: { active: true, product: {in: [this.id]}} });
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
            productId: this.id,
            artifactId: file.artifactId
          }).then(() => {
            if (this.error.deleteArtifact) {
              this.send({
                message: this.error.deleteArtifact.message,
                type: 'bg-danger',
                icon: 'ni-alert-circle'
              });
            }
          });
          this.componentKey += 1;
          await this.productArtifactSearch({productId: this.id});
        } else {
          await this.deleteOrderArtifact({artifactId: file.artifactId}).then(() => {
            if (this.orderArtifactError.deleteArtifact) {
              this.send({
                message: this.orderArtifactError.deleteArtifact.message,
                type: 'bg-danger',
                icon: 'ni-alert-circle'
              });
            }
          });
          this.componentKey += 1;
          await this.productArtifactSearch({productId: this.id});
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
              type: 'bg-danger',
              icon: 'ni-alert-circle'
            });
          }
        });
        this.componentKey += 1;
        await this.orderSearch({ role: 'seller', filters: { active: true, product: {in: [this.id]}} });
      } finally {
        this.$refs.foo.enable();
        this.componentLoading = false;
        this.activeArtifact = null;
        this.activeArtifacts = this.activeArtifacts.filter((id)=>id !== artifact.id);
      }
    }
  },
  mounted () {
    this.gcs = {
      unencryptedSigningURL: this.$root.context.$vsf.$numerbay.api.getArtifactUploadUrl,
      signingURL: this.$root.context.$vsf.$numerbay.api.getOrderArtifactUploadUrl,
      params: {
        productId: this.id
      },
      headers: {
        Authorization: `Bearer ${this.$cookies.get('nb-token')}`
        // 'Cache-Control': 'no-cache'
      },
      sendFileToServer: false,
      withCredentials: false
    };
  },
  setup(props, context) {
    const id = parseInt(context.root.$route.params.id);
    const { products, search: productSearch } = useProduct(`manage-artifacts-${id}`);
    const { artifacts, search: productArtifactSearch, createArtifact, downloadArtifact, deleteArtifact, loading: productArtifactLoading, error } = useProductArtifact(`${id}`);
    const { downloadArtifact: downloadOrderArtifact, deleteArtifact: deleteOrderArtifact, loading: orderArtifactLoading, error: orderArtifactError } = useOrderArtifact(`${id}`);
    const { orders, search: orderSearch, loading: orderLoading } = useUserOrder(`${id}`);
    const { send } = useUiNotification();

    productSearch({ id: id });
    productArtifactSearch({ productId: id });
    orderSearch({ role: 'seller', filters: {active: true, product: {in: [id]}} });

    const isManualFormOpen = ref(false);
    const activeArtifact = ref(null);
    const activeArtifacts = ref([]);

    const resetForm = () => ({
      url: null,
      description: null
    });
    const form = ref(resetForm());

    const getStatusTextClass = (artifact) => {
      const status = artifact?.state;
      switch (status) {
        case 'failed':
          return 'bg-danger';
        case 'pending':
          return 'bg-warning';
        case 'active':
          return 'bg-success';
        default:
          return '';
      }
    };

    const getSubmissionStatusTextClass = (order) => {
      const status = orderGetters.getSubmissionStatus(order);
      switch (status) {
        case 'failed':
          return 'bg-danger';
        case 'queued':
          return 'bg-warning';
        case 'completed':
          return 'bg-success';
        default:
          return '';
      }
    };

    return {
      id,
      product: computed(() => products.value?.data ? products.value.data[0] : null),
      artifacts: computed(() => artifacts ? artifacts.value : null),
      orders: computed(() => orders?.value?.data ? orders.value.data : []),
      createArtifact,
      downloadArtifact,
      downloadOrderArtifact,
      deleteArtifact,
      deleteOrderArtifact,
      productArtifactLoading,
      orderLoading,
      orderArtifactLoading,
      error,
      orderArtifactError,
      productArtifactSearch,
      activeArtifact,
      activeArtifacts,
      isManualFormOpen,
      form,
      orderGetters,
      productGetters,
      artifactGetters,
      orderSearch,
      resetForm,
      getStatusTextClass,
      getSubmissionStatusTextClass,
      send
    };
  }
};
</script>

<style lang="scss" scoped>
</style>
