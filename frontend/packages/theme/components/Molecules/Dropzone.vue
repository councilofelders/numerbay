<template>
  <div :id="id" ref="dropzoneElement" :class="{ 'vue-dropzone dropzone': includeStyling }">
    <div v-if="useCustomSlot" class="dz-message">
      <slot>Drop files here to upload</slot>
    </div>
  </div>
</template>

<script>
let component = {};

if (process.browser) {
  const Dropzone = require('dropzone').Dropzone;
  const {generateSignedUrl} = require('../../plugins/gcs');
  Dropzone.autoDiscover = false;
  component = {
    props: {
      id: {
        type: String,
        required: true,
        default: 'dropzone'
      },
      options: {
        type: Object,
        required: true
      },
      includeStyling: {
        type: Boolean,
        default: true,
        required: false
      },
      awss3: {
        type: Object,
        required: false,
        default: null
      },
      destroyDropzone: {
        type: Boolean,
        default: true,
        required: false
      },
      duplicateCheck: {
        type: Boolean,
        default: false,
        required: false
      },
      useCustomSlot: {
        type: Boolean,
        default: true,
        required: false
      },
      confirm: {
        type: Function,
        default: null,
        required: false
      }
    },
    computed: {
      // s3DropZoneSettings extend the regular options param that someone passes through
      // so things like acceptedFiles should just work
      s3DropZoneSettings() {
        const normalSettings = this.dropzoneSettings;
        // eslint-disable-next-line @typescript-eslint/no-this-alias
        const that = this;
        const s3Settings = {
          method: 'PUT',
          parallelUploads: 1,
          uploadMultiple: false,
          paramName: 'file',
          autoProcessQueue: false,
          sending (file, xhr) {
            const _send = xhr.send;
            xhr.send = () => {
              _send.call(xhr, file);
            };
          },
          async accept(file, done) {
            // eslint-disable-next-line no-use-before-define
            if (vm.isS3) {
              // eslint-disable-next-line no-use-before-define
              const incFile = vm.awss3.includeFile === true;
              // eslint-disable-next-line no-use-before-define
              const signed = await generateSignedUrl(that.awss3.signingURL, file, incFile, vm.awss3);
              // eslint-disable-next-line no-use-before-define
              vm.setOption('headers', {
                'Content-Type': 'application/octet-stream'
                // 'x-amz-acl': 'public-read'
              });
              file.artifactId = signed.id;
              // eslint-disable-next-line no-use-before-define
              vm.setOption('url', signed.url);
              done();
              // eslint-disable-next-line no-use-before-define
              setTimeout(() => vm.dropzone.processFile(file));
            }
          }
        };
        Object.keys(s3Settings).forEach((key) => {
          normalSettings[key] = s3Settings[key];
        }, this);
        // eslint-disable-next-line @typescript-eslint/no-this-alias,consistent-this
        const vm = this;
        return normalSettings;
      },
      dropzoneSettings() {
        const defaultValues = {
          thumbnailWidth: 200,
          thumbnailHeight: 200
        };
        Object.keys(this.options).forEach((key) => {
          defaultValues[key] = this.options[key];
        }, this);
        // eslint-disable-next-line @typescript-eslint/no-this-alias,consistent-this,no-unused-vars,@typescript-eslint/no-unused-vars
        const vm = this;
        return defaultValues;
      },
      isS3 () {
        return this.awss3 !== null;
      }
    },
    mounted() {
      if (this.$isServer && this.hasBeenMounted) {
        return;
      }
      this.hasBeenMounted = true;
      if (this.confirm) {
        Dropzone.confirm = this.confirm;
      }
      this.dropzone = new Dropzone(
        this.$refs.dropzoneElement,
        this.isS3 ? this.s3DropZoneSettings : this.dropzoneSettings
      );
      // eslint-disable-next-line @typescript-eslint/no-this-alias,consistent-this
      const vm = this;
      this.dropzone.on('thumbnail', (file, dataUrl) => {
        vm.$emit('vdropzone-thumbnail', file, dataUrl);
      });
      this.dropzone.on('addedfile', async (file) => {
        let isDuplicate = false;
        if (vm.duplicateCheck) {
          if (this.files.length) {
            let _i;
            let _len;
            for (_i = 0, _len = this.files.length; _i < _len - 1; _i++) {
              // eslint-disable-next-line max-depth
              if (
                this.files[_i].name === file.name &&
                this.files[_i].size === file.size &&
                this.files[_i].lastModified ===
                  file.lastModified
              ) {
                this.removeFile(file);
                // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
                isDuplicate = true;
                vm.$emit('vdropzone-duplicate-file', file);
              }
            }
          }
        }
        vm.$emit('vdropzone-file-added', file);
      });
      this.dropzone.on('addedfiles', (files) => {
        vm.$emit('vdropzone-files-added', files);
      });
      this.dropzone.on('removedfile', (file) => {
        vm.$emit('vdropzone-removed-file', file);
        if (file.manuallyAdded && vm.dropzone.options.maxFiles !== null) {
          vm.dropzone.options.maxFiles++;
        }
      });
      this.dropzone.on('success', (file, response) => {
        vm.$emit('vdropzone-success', file, response);
      });
      this.dropzone.on('successmultiple', (file, response) => {
        vm.$emit('vdropzone-success-multiple', file, response);
      });
      this.dropzone.on('error', (file, message, xhr) => {
        vm.$emit('vdropzone-error', file, message, xhr);
      });
      this.dropzone.on('errormultiple', (files, message, xhr) => {
        vm.$emit('vdropzone-error-multiple', files, message, xhr);
      });
      this.dropzone.on('sending', (file, xhr, formData) => {
        vm.$emit('vdropzone-sending', file, xhr, formData);
      });
      this.dropzone.on('sendingmultiple', (file, xhr, formData) => {
        vm.$emit('vdropzone-sending-multiple', file, xhr, formData);
      });
      this.dropzone.on('complete', (file) => {
        vm.$emit('vdropzone-complete', file);
      });
      this.dropzone.on('completemultiple', (files) => {
        vm.$emit('vdropzone-complete-multiple', files);
      });
      this.dropzone.on('canceled', (file) => {
        vm.$emit('vdropzone-canceled', file);
      });
      this.dropzone.on('canceledmultiple', (files) => {
        vm.$emit('vdropzone-canceled-multiple', files);
      });
      this.dropzone.on('maxfilesreached', (files) => {
        vm.$emit('vdropzone-max-files-reached', files);
      });
      this.dropzone.on('maxfilesexceeded', (file) => {
        vm.$emit('vdropzone-max-files-exceeded', file);
      });
      this.dropzone.on('processing', async (file) => {
        vm.$emit('vdropzone-processing', file);
      });
      this.dropzone.on('processingmultiple', (files) => {
        vm.$emit('vdropzone-processing-multiple', files);
      });
      this.dropzone.on('uploadprogress', (file, progress, bytesSent) => {
        vm.$emit('vdropzone-upload-progress', file, progress, bytesSent);
      });
      this.dropzone.on('totaluploadprogress', (
        totaluploadprogress,
        totalBytes,
        totalBytesSent
      ) => {
        vm.$emit(
          'vdropzone-total-upload-progress',
          totaluploadprogress,
          totalBytes,
          totalBytesSent
        );
      });
      this.dropzone.on('reset', () => {
        vm.$emit('vdropzone-reset');
      });
      this.dropzone.on('queuecomplete', () => {
        vm.$emit('vdropzone-queue-complete');
      });
      this.dropzone.on('drop', (event) => {
        vm.$emit('vdropzone-drop', event);
      });
      this.dropzone.on('dragstart', (event) => {
        vm.$emit('vdropzone-drag-start', event);
      });
      this.dropzone.on('dragend', (event) => {
        vm.$emit('vdropzone-drag-end', event);
      });
      this.dropzone.on('dragenter', (event) => {
        vm.$emit('vdropzone-drag-enter', event);
      });
      this.dropzone.on('dragover', (event) => {
        vm.$emit('vdropzone-drag-over', event);
      });
      this.dropzone.on('dragleave', (event) => {
        vm.$emit('vdropzone-drag-leave', event);
      });
      vm.$emit('vdropzone-mounted');
    },
    beforeDestroy() {
      if (this.destroyDropzone) this.dropzone.destroy();
    },
    methods: {
      manuallyAddFile(file, fileUrl) {
        file.manuallyAdded = true;
        this.dropzone.emit('addedfile', file);
        let containsImageFileType = false;
        const supportedThumbnailTypes = ['.svg', '.png', '.jpg', 'jpeg', '.gif', '.webp', 'image/'];
        if (supportedThumbnailTypes.filter(s => fileUrl.toLowerCase().indexOf(s) > -1).length > 0) {
          containsImageFileType = true;
        }
        if (
          this.dropzone.options.createImageThumbnails &&
          containsImageFileType &&
          file.size <= this.dropzone.options.maxThumbnailFilesize * 1024 * 1024
        ) {
          fileUrl && this.dropzone.emit('thumbnail', file, fileUrl);
          const thumbnails = file.previewElement.querySelectorAll(
            '[data-dz-thumbnail]'
          );
          for (let i = 0; i < thumbnails.length; i++) {
            thumbnails[i].style.width =
              this.dropzoneSettings.thumbnailWidth + 'px';
            thumbnails[i].style.height =
              this.dropzoneSettings.thumbnailHeight + 'px';
            thumbnails[i].classList.add('vdManualThumbnail');
          }
        }
        this.dropzone.emit('complete', file);
        if (this.dropzone.options.maxFiles) this.dropzone.options.maxFiles--;
        file.accepted = true;
        this.dropzone.files.push(file);
        this.$emit('vdropzone-file-added-manually', file);
      },
      setOption(option, value) {
        this.dropzone.options[option] = value;
      },
      removeAllFiles(bool) {
        this.dropzone.removeAllFiles(bool);
      },
      processQueue() {
        const dropzoneEle = this.dropzone;
        this.dropzone.processQueue();
        this.dropzone.on('success', () => {
          dropzoneEle.options.autoProcessQueue = true;
        });
        this.dropzone.on('queuecomplete', () => {
          dropzoneEle.options.autoProcessQueue = false;
        });
      },
      init() {
        return this.dropzone.init();
      },
      destroy() {
        return this.dropzone.destroy();
      },
      updateTotalUploadProgress() {
        return this.dropzone.updateTotalUploadProgress();
      },
      getFallbackForm() {
        return this.dropzone.getFallbackForm();
      },
      getExistingFallback() {
        return this.dropzone.getExistingFallback();
      },
      setupEventListeners() {
        return this.dropzone.setupEventListeners();
      },
      removeEventListeners() {
        return this.dropzone.removeEventListeners();
      },
      disable() {
        return this.dropzone.disable();
      },
      enable() {
        return this.dropzone.enable();
      },
      filesize(size) {
        return this.dropzone.filesize(size);
      },
      accept(file, done) {
        return this.dropzone.accept(file, done);
      },
      addFile(file) {
        return this.dropzone.addFile(file);
      },
      removeFile(file) {
        this.dropzone.removeFile(file);
      },
      getAcceptedFiles() {
        return this.dropzone.getAcceptedFiles();
      },
      getRejectedFiles() {
        return this.dropzone.getRejectedFiles();
      },
      getFilesWithStatus() {
        return this.dropzone.getFilesWithStatus();
      },
      getQueuedFiles() {
        return this.dropzone.getQueuedFiles();
      },
      getUploadingFiles() {
        return this.dropzone.getUploadingFiles();
      },
      getAddedFiles() {
        return this.dropzone.getAddedFiles();
      },
      getActiveFiles() {
        return this.dropzone.getActiveFiles();
      }
    }
  };
}

component.name = 'dropzone';
component.props = component.props || ['useCustomSlot', 'includeStyling'];
component.render = (createElement) => {
  // eslint-disable-next-line consistent-this
  const that = this._self;
  // Fyi vue-dropzone doesn't currently support automatic detection, see https://github.com/rowanwins/vue-dropzone/issues/488
  const hasChildren = this.$slots.default && this.$slots.default.length;
  const useSlot = this.useCustomSlot === '' || this.useCustomSlot === true || hasChildren;
  const vnodes = useSlot
    ? [createElement('div', { staticClass: 'dz-message' }, this.$slots.default)]
    : this.$slots.default;

  // Default: true
  const includeStyling = this.$props.includeStyling !== false;

  return createElement('div', {
    props: that.props,
    attrs: {
      // NB! Empty class string required to avoid internal fallback defaulting
      class: includeStyling ? 'vue-dropzone dropzone' : '',
      id: that.id || ''
    },
    ref: 'dropzoneElement'
  }, vnodes);
};

module.exports = component;
</script>

<style lang="scss">
.vue-dropzone {
  border: 2px solid #e5e5e5;
  font-family: "Arial", sans-serif;
  letter-spacing: 0.2px;
  color: #777;
  transition: 0.2s linear;
}
.vue-dropzone:hover {
  background-color: #f6f6f6;
}
.vue-dropzone > i {
  color: #ccc;
}
.vue-dropzone > .dz-preview .dz-image {
  border-radius: 0;
  width: 100%;
  height: 100%;
}
.vue-dropzone > .dz-preview .dz-image img:not([src]) {
  width: 200px;
  height: 200px;
}
.vue-dropzone > .dz-preview .dz-image:hover img {
  transform: none;
  -webkit-filter: none;
}
.vue-dropzone > .dz-preview .dz-details {
  bottom: 0;
  top: 0;
  color: white;
  background-color: var(--c-primary) !important;
  transition: opacity 0.2s linear;
  text-align: left;
}
.vue-dropzone > .dz-preview .dz-details .dz-filename {
  word-break: break-all !important;
  white-space: normal !important;
}
.vue-dropzone > .dz-preview .dz-details .dz-filename span,
.vue-dropzone > .dz-preview .dz-details .dz-size span {
  background-color: transparent;
}
.vue-dropzone > .dz-preview .dz-details .dz-filename:not(:hover) span {
  border: none;
}
.vue-dropzone > .dz-preview .dz-details .dz-filename:hover span {
  background-color: transparent;
  border: none;
}
.vue-dropzone > .dz-preview .dz-progress .dz-upload {
  background: #cccccc;
}
.vue-dropzone > .dz-preview .dz-remove {
  position: absolute;
  z-index: 30;
  color: white;
  margin-left: 15px;
  padding: 10px;
  top: inherit;
  bottom: 15px;
  border: 2px white solid;
  text-decoration: none;
  text-transform: uppercase;
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 1.1px;
  opacity: 0;
}
.vue-dropzone > .dz-preview:hover .dz-remove {
  opacity: 1;
}
.vue-dropzone > .dz-preview .dz-success-mark,
.vue-dropzone > .dz-preview .dz-error-mark {
  margin-left: auto;
  margin-top: auto;
  width: 100%;
  top: 35%;
  left: 0;
}
.vue-dropzone > .dz-preview .dz-success-mark svg,
.vue-dropzone > .dz-preview .dz-error-mark svg {
  margin-left: auto;
  margin-right: auto;
}
.vue-dropzone > .dz-preview .dz-error-message {
  margin-left: auto;
  margin-right: auto;
  left: 0;
  width: 100%;
  text-align: center;
}
.vue-dropzone > .dz-preview .dz-error-message:after {
  display: none;
}
.vue-dropzone > .dz-preview .vdManualThumbnail {
  object-fit: cover;
}
</style>
