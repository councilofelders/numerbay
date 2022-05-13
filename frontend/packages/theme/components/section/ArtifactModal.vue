<template>
  <Modal :modal-id="modalId" modal-class="modal-lg" @registeredModal="modal = $event">
    <template slot="title">Artifact Files</template>
    <div class="row g-2">
      <div class="col-xl-12">
        <table v-if="artifacts && orderGetters.getStatus(order)=='confirmed' && !order.buyer_public_key"
               class="table mb-0 table-s2">
          <thead class="fs-14">
          <tr>
            <th v-for="(list, i) in [
                      'Download File',
                      'Numerai Submission'
                    ]" :key="i" scope="col">{{ list }}
            </th>
          </tr>
          </thead>
          <tbody>
          <tr v-if="!artifacts || artifacts.total===0">
            <td class="text-secondary" colspan="2">Please wait for the seller to upload artifacts after the round
              opens
            </td>
          </tr>
          <tr v-for="artifact in artifacts.data" :key="artifactGetters.getId(artifact)">
            <td>
              <span class="text-break" style="white-space: normal;">
                <a :title="`Download ${artifactGetters.getObjectName(artifact)}`" href="javascript:void(0);"
                   @click="download(artifact)">{{
                    artifactGetters.getObjectName(artifact)
                  }}</a>
                <span v-if="isActiveArtifact(artifact)" class="spinner-border spinner-border-sm text-primary"
                      role="status"></span>
              </span>
            </td>
            <td>
              <div v-if="Boolean(artifact) && !!artifact.object_name && !!order.submit_model_id"
                   class="d-flex justify-content-between">
                <button class="icon-btn ms-auto" title="Submit to Numerai" @click="submit(artifact)">
                  <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                  <em v-else class="ni ni-upload-cloud"></em>
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
        <table v-if="orderArtifacts && orderGetters.getStatus(order)=='confirmed' && Boolean(order.buyer_public_key)"
               class="table mb-0 table-s2">
          <thead class="fs-14">
          <tr>
            <th v-for="(list, i) in [
                      'Download File',
                      'Numerai Submission'
                    ]" :key="i" scope="col">{{ list }}
            </th>
          </tr>
          </thead>
          <tbody>
          <tr v-if="!orderArtifacts || orderArtifacts.total===0">
            <td class="text-secondary" colspan="2">Please wait for the seller to upload artifacts after the round
              opens
            </td>
          </tr>
          <tr v-for="artifact in orderArtifacts.data" :key="artifactGetters.getId(artifact)">
            <td>
              <span class="text-break" style="white-space: normal;">
                <a :title="`Download ${artifactGetters.getObjectName(artifact)}`" href="javascript:void(0);"
                   @click="downloadAndDecrypt(artifact)">{{
                    artifactGetters.getObjectName(artifact)
                  }}</a>
                <span v-if="isActiveArtifact(artifact)" class="spinner-border spinner-border-sm text-primary"
                      role="status"></span>
              </span>
            </td>
            <td>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Modal><!-- end modal-->
</template>
<script>
// Composables
import {artifactGetters, orderGetters, useOrderArtifact, useProductArtifact} from '@vue-storefront/numerbay';
import {computed, ref} from '@vue/composition-api';
import axios from 'axios';
import {decodeBase64} from 'tweetnacl-util';
import nacl from 'tweetnacl';
import {useUiNotification} from '~/composables';

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
  name: 'ArtifactModal',
  props: {
    modalId: {
      type: String,
      default: 'artifactModal'
    },
    order: {
      type: Object,
      default: () => ({})
    },
    publicKey: {
      type: String,
      default: null
    },
    encryptedPrivateKey: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      modal: null,
      downloadingProgress: {}
    };
  },
  methods: {
    show() {
      this.search({productId: this.order.product.id});
      this.searchOrderArtifacts({orderId: this.order.id});
      this.modal?.show();
    },
    hide() {
      this.modal?.hide();
    },
    getMetricColor(value) {
      if (value > 0) {
        return 'success';
      } else if (value < 0) {
        return 'danger';
      } else {
        return '';
      }
    },
    isActiveArtifact(artifact) {
      return this.activeArtifacts && this.activeArtifacts.includes(artifact.id);
    },
    onProgress(artifact, progress) {
      this.$set(this.downloadingProgress, artifact.id, progress);
    },
    async download(artifact) {
      this.activeArtifacts.push(artifact.id);
      try {
        if (!artifact.object_name && artifact.url) {
          window.open(artifact.url, '_blank');
          return;
        }

        const downloadUrl = await this.downloadArtifact({
          productId: this.order.product.id,
          artifactId: artifact.id
        });
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
      } finally {
        this.activeArtifacts = this.activeArtifacts.filter((id) => id !== artifact.id);
      }
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
      this.activeArtifacts.push(artifact.id);
      const downloadUrl = await this.downloadOrderArtifact({artifactId: artifact.id});
      this.activeArtifact = null;
      this.activeArtifacts = this.activeArtifacts.filter((id) => id !== artifact.id);
      if (this.orderArtifactError.downloadArtifact) {
        this.send({
          message: this.orderArtifactError.downloadArtifact.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
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
          this.downloadingArtifacts = this.downloadingArtifacts.filter((id) => id !== artifact.id);
          this.decryptingArtifacts.push(artifact.id);
          this.decryptfile(file).then((blobUrl) => {
            const link = document.createElement('a');
            link.href = blobUrl;
            link.download = filename;
            link.click();
            URL.revokeObjectURL(link.href);
          }).catch((e) => {
            console.error(e);
          }).finally(() => {
            this.decryptingArtifacts = this.decryptingArtifacts.filter((id) => id !== artifact.id);
          });
        }).catch((e) => {
        console.error(e);
      }).finally(() => {
        this.downloadingArtifacts = this.downloadingArtifacts.filter((id) => id !== artifact.id);
        this.downloadingProgress[artifact.id] = 0;
      });
    },
    async submit(artifact) {
      await this.submitArtifact({orderId: this.order.id, artifactId: artifact.id});
      if (this.error.submitArtifact) {
        this.send({
          message: this.error.submitArtifact.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
      } else {
        this.send({
          message: 'Submission queued, please wait for a minute',
          type: 'bg-success',
          icon: 'ni-check'
        });
      }
    }
  },
  beforeDestroy() {
    this.modal?.hide();
  },
  setup(props) {
    const {
      artifacts,
      search,
      downloadArtifact,
      submitArtifact,
      loading,
      error
    } = useProductArtifact(`${props.order.product.id}`);
    const {
      artifacts: orderArtifacts, search: searchOrderArtifacts, downloadArtifact: downloadOrderArtifact,
      submitArtifact: submitOrderArtifact, loading: orderArtifactLoading, error: orderArtifactError
    } = useOrderArtifact(`${props.order.id}`);
    const {send} = useUiNotification();

    search({productId: props.order.product.id});
    searchOrderArtifacts({orderId: props.order.id});

    const downloadingArtifacts = ref([]);
    const decryptingArtifacts = ref([]);
    const activeArtifacts = ref([]);

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

    return {
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
      decryptingArtifacts,
      activeArtifacts,
      getStatusTextClass,
      search,
      searchOrderArtifacts
    };
  }
};
</script>

<style lang="css" scoped>
</style>
