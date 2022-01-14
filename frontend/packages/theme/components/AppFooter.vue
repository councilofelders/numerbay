<template>
  <SfFooter :column="4" multiple class="footer">
    <SfFooterColumn
      v-for="linkGroup in links"
      :key="linkGroup.name"
      :title="$t(linkGroup.name)"
    >
      <SfList>
        <SfListItem v-for="link in linkGroup.children" :key="link.name">
          <router-link v-if="link.link" :to="link.link" exact>
            <SfMenuItem class="sf-footer__menu-item" :label="$t(link.name)" />
          </router-link>
          <SfMenuItem
            v-else-if="link.clickHandler"
            class="sf-footer__menu-item"
            :label="$t(link.name)"
            @click="link.clickHandler"
          />
        </SfListItem>
      </SfList>
    </SfFooterColumn>
  </SfFooter>
</template>

<script>
import { SfFooter, SfImage, SfList, SfMenuItem } from '@storefront-ui/vue';
import axios from 'axios';

export default {
  components: {
    SfFooter,
    SfList,
    SfImage,
    SfMenuItem
  },
  data() {
    return {
      qeDashboardUrl: null
    };
  },
  computed: {
    links () {
      return {
        aboutNumerbay: {
          name: 'About NumerBay',
          children: [
            { name: 'Maintainer: Numerai Community', link: '#' },
            { name: 'Sponsor: Numerai Council of Elders', link: '#' },
            { name: 'Logo: Numerai, 2022', link: '#' }
          ]
        },
        api: {
          name: 'NumerBay Docs',
          children: [
            { name: 'Tutorials and Docs', clickHandler: () => window.open('https://docs.numerbay.ai/', '_blank') },
            { name: 'Python Client Reference', clickHandler: () => window.open('https://docs.numerbay.ai/docs/reference/numerbay', '_blank') }
          ]
        },
        officialNumerai: {
          name: 'Official Numerai',
          children: [
            { name: 'Numerai', clickHandler: () => window.open('https://numer.ai/', '_blank') },
            { name: 'Signals', clickHandler: () => window.open('https://signals.numer.ai/', '_blank') },
            { name: 'Forum', clickHandler: () => window.open('https://forum.numer.ai/', '_blank') },
            { name: 'RocketChat', clickHandler: () => window.open('https://community.numer.ai/', '_blank') }
          ]
        },
        community: {
          name: 'Numerai Community',
          children: [
            { name: 'CoE Wallet', clickHandler: () => window.open('https://gnosis-safe.io/app/#/safes/0xF58B7c28DAF13926329ef0c74FA3f7258f5A9131/', '_blank') },
            { name: 'Dashboard by @QE', clickHandler: () => window.open(this.qeDashboardUrl, '_blank') },
            { name: 'Newsletter by @Aventurine', clickHandler: () => window.open('https://coenumerainewsletter.substack.com/', '_blank') }
          ]
        }
      };
    }
  },
  mounted() { // dynamic iframe
    axios.get('https://raw.githubusercontent.com/jos1977/numerai_statistics/main/ClassicDashboardLink.txt').then((response) => {
      this.qeDashboardUrl = response.data;
    });
  }
};
</script>

<style lang="scss">

.footer {
  margin-bottom: 3.75rem;
  @include for-desktop {
    margin-bottom: 0;
  }
  &__socials {
    display: flex;
    justify-content: space-between;
    margin: 0 auto var(--spacer-lg);
    padding: var(--spacer-base) var(--spacer-xl);
    @include for-desktop {
      justify-content: flex-start;
      padding: var(--spacer-xs) 0;
      margin: 0 auto;
    }
  }
  &__social-image {
    margin: 0 var(--spacer-2xs) 0 0;
  }
}
.sf-footer {
  @include for-desktop {
    border-top: var(--spacer-xs) solid var(--c-primary);
    padding-bottom: 0;
    margin-top: var(--spacer-2xl);
  }
  &__container {
    margin: var(--spacer-sm);
    @include for-desktop {
      max-width: 69rem;
      margin: 0 auto;
    }
  }
}
</style>
