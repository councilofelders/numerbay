<template>
  <div class="highlighted highlighted--total">
    <!--<dropzone id="foo" ref="foo" :options="dropzoneOptions" :destroyDropzone="true" @vdropzone-error="onUploadError" v-on:vdropzone-sending="onSending"></dropzone>-->
<!--    <SfLoader :class="{ loader: componentLoading }" :loading="componentLoading">-->
      <dropzone :key="componentKey" id="foo" ref="foo" :options="dropzoneOptions" :awss3="gcs" :destroyDropzone="false"
        v-on:vdropzone-error="s3UploadError"
        v-on:vdropzone-success="s3UploadSuccess"
        v-on:vdropzone-removed-file="onRemove"
      >
        Drop files here to upload<br/>Allowed extentions: {{this.dropzoneOptions.acceptedFiles}}<br/>File names are obfuscated on upload
      </dropzone>
<!--    </SfLoader>-->
<!--    v-on:vdropzone-sending="onSending"-->
  </div>
</template>

<script>
import { SfProperty, SfIcon, SfButton, SfInput, SfLoader } from '@storefront-ui/vue';
import { orderGetters, useProductArtifact } from '@vue-storefront/numerbay';
// import { authHeaders } from '@vue-storefront/numerbay-api/src/api/utils';
import Dropzone from '../../components/Molecules/Dropzone';
import 'nuxt-dropzone/dropzone.css';
import {computed} from '@vue/composition-api';
import {Logger} from '@vue-storefront/core';

export default {
  name: 'ArtifactPanel',
  components: {
    SfProperty,
    SfIcon,
    SfButton,
    SfInput,
    SfLoader,
    Dropzone
  },
  data() {
    // eslint-disable-next-line @typescript-eslint/no-this-alias,consistent-this
    const vm = this;
    return {
      componentKey: 0,
      componentLoading: false,
      gcs: {
        signingURL: `http://${process.env.VUE_APP_DOMAIN_DEV || 'localhost'}/backend-api/v1/products/${vm.product.id}/artifacts/generate-upload-url`,
        params: {},
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
        url: 'https://httpbin.org/post', // placeholder url
        method: 'put',
        addRemoveLinks: true,
        timeout: 300000,
        parallelUploads: 1,
        createImageThumbnails: false,
        maxFilesize: 200,
        acceptedFiles: '.txt,.csv,.parquet,.zip,.ipynb,.docx',
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
    }
  },
  watch: {
    artifacts(artifacts) {
      Logger.debug('artifact changed watch', artifacts);
      if (artifacts) {
        // this.$refs.foo.removeAllFiles(true);
        for (const artifact of artifacts.data) {
          const file = { name: artifact.object_name, artifactId: artifact.id, size: artifact.object_size }; // , type: "image/png"
          const url = '';
          this.$refs.foo.manuallyAddFile(file, url);
        }
      }
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
    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    async s3UploadSuccess(response) {
      Logger.debug('Upload success', this.product.id);
      this.componentLoading = true;
      try {
        this.$refs.foo.disable();
        this.componentKey += 1;
        await this.search({ productId: this.product.id });
      } finally {
        this.$refs.foo.enable();
        this.componentLoading = false;
      }
    },
    s3UploadError(errorMessage) {
      Logger.error('s3 error', errorMessage);
    },
    // async onCancel(file, error, xhr) {
    //   Logger.debug('onCancel', file, error, xhr);
    //   await this.deleteArtifact({productId: this.product.id, artifactId: file.artifactId});
    // },
    async onRemove(file, error, xhr) {
      Logger.debug('onRemove', file, error, xhr);
      await this.deleteArtifact({productId: this.product.id, artifactId: file.artifactId});
    }
  },
  async mounted() {
    // Logger.debug('artifacts', this.artifacts)
    //
    // var file = { size: 123, name: "Icon", type: "image/png" };
    // var url = "https://myvizo.com/img/logo_sm.png";
    // this.$refs.foo.manuallyAddFile(file, url);
  },
  // eslint-disable-next-line no-unused-vars,@typescript-eslint/explicit-module-boundary-types,@typescript-eslint/no-unused-vars
  setup(props, { emit, root }) {
    const { artifacts, search, deleteArtifact, loading } = useProductArtifact(`${props.product.id}`);

    search({ productId: props.product.id });

    return {
      artifacts: computed(() => artifacts ? artifacts.value : null),
      deleteArtifact,
      loading,
      search,
      orderGetters
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
