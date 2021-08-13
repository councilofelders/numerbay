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
import { SfFooter, SfList, SfImage, SfMenuItem } from '@storefront-ui/vue';

export default {
  components: {
    SfFooter,
    SfList,
    SfImage,
    SfMenuItem
  },
  computed: {
    links () {
      return {
        aboutNumerbay: {
          name: 'About NumerBay',
          children: [
            { name: 'Sponsor: Numerai Council of Elders', link: '#' }
          ]
        },
        officialNumerai: {
          name: 'Official Numerai',
          children: [
            { name: 'Numerai', clickHandler: () => window.open('https://numer.ai/', '_blank') },
            { name: 'Signals', clickHandler: () => window.open('https://signals.numer.ai/', '_blank') }
          ]
        }
      };
    }
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
