<template>
  <SfTabs :open-tab="1">
    <SfTab title="Numerai dashboard">
      <SfButton class="sf-button color-secondary" @click="openWindow(iframe.src);" :disabled="!iframe.loaded">Open in New Window</SfButton>
      <LazyHydrate when-visible>
        <SfLoader :class="{ loading: !iframe.loaded }" :loading="!iframe.loaded"  class="desktop-only">
          <iframe width="100%" height="747" :src="iframe.src" frameborder="0" allowFullScreen="true" v-if="iframe.loaded" class="desktop-only"></iframe>
        </SfLoader>
      </LazyHydrate>
    </SfTab>
  </SfTabs>
</template>

<script>
import {
  SfLoader,
  SfTabs,
  SfTable,
  SfButton,
  SfProperty,
  SfLink,
  SfNotification
} from '@storefront-ui/vue';
import LazyHydrate from 'vue-lazy-hydration';
import NumeraiApiForm from '../../components/MyAccount/NumeraiApiForm';
import ArtifactPanel from '../../components/Molecules/ArtifactPanel';
import axios from 'axios';

export default {
  name: 'NumeraiDashboard',
  components: {
    LazyHydrate,
    SfLoader,
    SfTabs,
    SfTable,
    SfButton,
    SfProperty,
    SfLink,
    SfNotification,
    NumeraiApiForm,
    ArtifactPanel
  },
  data() {
    return {
      iframe: {
        src: '',
        loaded: false
      }
    };
  },
  mounted() {
    axios.get('https://raw.githubusercontent.com/jos1977/numerai_statistics/main/ClassicDashboardLink.txt').then((response) => {
      this.iframe.src = response.data;
      this.iframe.loaded = true;
    });
  },
  methods: {
    openWindow(link) {
      window.open(link);
    }
  }
};
</script>

<style lang='scss' scoped>
</style>
