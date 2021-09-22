<template>
  <div>
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
    <div class="top-buttons">
      <SfButton class="sf-button color-secondary" @click="isManualFormOpen = !isManualFormOpen" :disabled="loading">
        {{ $t('Manually Add URL') }}
      </SfButton>
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
        <SfTableData><span style="word-break: break-all;">{{ artifactGetters.getObjectName(artifact) }}</span></SfTableData>
        <SfTableData>
          <SfLoader :class="{ loader: componentLoading }" :loading="componentLoading">
            <SfInput :value="artifact.description" style="margin-right: 10px" label="Description" @input="(value)=>handleEdit(value, product, artifact)"/>
          </SfLoader>
        </SfTableData>
        <SfTableData>{{ artifactGetters.getObjectSize(artifact) }}</SfTableData>
        <SfTableData class="orders__view orders__element--right">
          <SfLoader :class="{ loader: loading }" :loading="loading">
            <span>
              <SfButton class="sf-button--text" @click="onManualRemove(artifact)">
                {{ $t('Delete') }}
              </SfButton>
            </span>
          </SfLoader>
        </SfTableData>
      </SfTableRow>
      <SfTableRow :key="'new'" v-if="isManualFormOpen">
        <SfTableData></SfTableData>
        <SfTableData>
          <ValidationObserver v-slot="{ handleSubmit }">
            <ValidationProvider rules="url" v-slot="{ errors }">
              <SfInput v-model="form.url"
                       style="margin-right: 10px"
                       label="URL"
                       type="url"
                       :valid="!errors[0]"
                      :errorMessage="errors[0]"
                       @change="encodeURL"></SfInput>
            </ValidationProvider>
          </ValidationObserver>
        </SfTableData>
        <SfTableData><SfInput v-model="form.description" style="margin-right: 10px" label="Description"></SfInput></SfTableData>
        <SfTableData></SfTableData>
        <SfTableData class="orders__view orders__element--right">
          <SfLoader :class="{ loader: loading }" :loading="loading">
            <SfButton class="sf-button--text" @click="handleNew">
              {{ $t('Save') }}
            </SfButton>
          </SfLoader>
        </SfTableData>
      </SfTableRow>
    </SfTable>
  </div>
</template>

<script>
import { SfProperty, SfIcon, SfButton, SfInput, SfLoader, SfTable } from '@storefront-ui/vue';
import {
  orderGetters,
  artifactGetters,
  useProductArtifact
} from '@vue-storefront/numerbay';
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
// import { authHeaders } from '@vue-storefront/numerbay-api/src/api/utils';
import Dropzone from '../../components/Molecules/Dropzone';
import 'nuxt-dropzone/dropzone.css';
import {computed, ref} from '@vue/composition-api';
import {Logger} from '@vue-storefront/core';
import debounce from 'lodash.debounce';

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

export default {
  name: 'ArtifactPanel',
  components: {
    SfProperty,
    SfIcon,
    SfButton,
    SfInput,
    SfLoader,
    SfTable,
    Dropzone,
    ValidationProvider,
    ValidationObserver
  },
  data() {
    // eslint-disable-next-line @typescript-eslint/no-this-alias,consistent-this
    const vm = this;
    console.log(`${vm.$root.$config._app.backendURL}/backend-api/v1/products/${vm.product.id}/artifacts/generate-upload-url`);
    return {
      componentKey: 0,
      componentLoading: false,
      gcs: {
        signingURL: vm.$root.context.$vsf.$numerbay.api.getArtifactUploadUrl,
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
        url: 'https://httpbin.org/post', // placeholder url
        method: 'put',
        addRemoveLinks: true,
        timeout: 300000,
        parallelUploads: 1,
        createImageThumbnails: false,
        maxFilesize: 200,
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
    }
  },
  watch: {
    artifacts(artifacts) {
      Logger.debug('artifact changed watch', artifacts);
      if (artifacts) {
        // this.$refs.foo.removeAllFiles(true);
        for (const artifact of artifacts.data) {
          if (artifact.object_name) {
            const file = { name: artifact.object_name, artifactId: artifact.id, size: artifact.object_size };
            const url = '';
            this.$refs.foo.manuallyAddFile(file, url);
          }
        }
      }
    }
  },
  methods: {
    encodeURL() {
      if (this.form.url) {
        this.form.url = encodeURI(decodeURI(this.form.url));
      }
    },
    async handleEdit(value, product, artifact) {
      const onComplete = async () => {
        this.componentLoading = true;
        try {
          this.$refs.foo.disable();
          this.componentKey += 1;
          await this.search({ productId: this.product.id });
        } finally {
          this.$refs.foo.enable();
          this.componentLoading = false;
        }
      };
      await this.onArtifactEdit(value, product, artifact, onComplete);
    },
    async handleNew() {
      await this.createArtifact({productId: this.product.id, artifact: this.form});
      this.componentLoading = true;
      try {
        this.$refs.foo.disable();
        this.componentKey += 1;
        await this.search({ productId: this.product.id });
        this.form = this.resetForm();
        this.isManualFormOpen = false;
      } finally {
        this.$refs.foo.enable();
        this.componentLoading = false;
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
      await this.search({ productId: this.product.id });
    },
    async onManualRemove(artifact) {
      this.componentLoading = true;
      try {
        this.$refs.foo.disable();
        await this.deleteArtifact({productId: this.product.id, artifactId: artifact.id});
        this.componentKey += 1;
        await this.search({ productId: this.product.id });
      } finally {
        this.$refs.foo.enable();
        this.componentLoading = false;
      }
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
    const { artifacts, search, createArtifact, updateArtifact, deleteArtifact, loading } = useProductArtifact(`${props.product.id}`);

    search({ productId: props.product.id });

    const isManualFormOpen = ref(false);

    const tableHeaders = [
      'Artifact ID',
      'Name',
      'Description',
      'Size',
      'Action'
    ];

    const resetForm = () => ({
      url: null,
      description: null
    });
    const form = ref(resetForm());

    const onArtifactEdit = debounce(async (value, product, artifact, onComplete) => {
      await Promise.all([
        updateArtifact({
          productId: product.id,
          artifactId: artifact.id,
          description: value
        }),
        onComplete()
        // categoriesSearch({
        //   term: term.value,
        // }),
      ]);
      //
      // result.value = {
      //   products: searchResult.value?.data?.products,
      //   categories: categoryGetters.getTree(searchResult.value?.data?.categories[0])
      // };
    }, 1000);

    return {
      artifacts: computed(() => artifacts ? artifacts.value : null),
      createArtifact,
      deleteArtifact,
      loading,
      search,
      tableHeaders,
      isManualFormOpen,
      form,
      resetForm,
      onArtifactEdit,
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
.top-buttons {
  @include for-desktop {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
}
</style>
