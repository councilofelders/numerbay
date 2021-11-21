<template>
  <div>
    <SfHeader
      class="sf-header--has-mobile-search"
      :class="{'header-on-top': isSearchOpen}"
      :isNavVisible="isMobileMenuOpen"
    >
      <template #logo>
        <nuxt-link :to="localePath('/')" class="sf-header__logo">
          <SfImage src="/icons/Numerai-Logo-Icon.png" alt="Vue Storefront Next" class="sf-header__logo-image"/>
        </nuxt-link>
      </template>
      <template #navigation>
        <HeaderNavigation :isMobile="isMobile" />
        <!--<SfHeaderNavigationItem class="nav-item" v-e2e="'app-header-url_numerai'" label="Numerai" :link="localePath('/c/numerai')"/>
        <SfHeaderNavigationItem class="nav-item"  v-e2e="'app-header-url_signals'" label="Signals" :link="localePath('/c/signals')" />
        <SfHeaderNavigationItem class="nav-item"  v-e2e="'app-header-url_onlyfams'" label="OnlyFams" :link="localePath('/c/onlyfams')" />-->
      </template>
      <template #aside>
<!--        <LocaleSelector class="smartphone-only" />--><span></span>
      </template>
      <template #header-icons>
        <div class="sf-header__icons">
          <SfButton
            name="app-header-account"
            v-e2e="'app-header-account'"
            class="sf-button--pure sf-header__action"
            @click="handleAccountClick"
          >
            <SfIcon
              :icon="accountIcon"
              size="1.25rem"
            />
          </SfButton>
          <SfButton
            class="sf-button--pure sf-header__action"
            @click="toggleWishlistSidebar"
          >
            <SfIcon
              class="sf-header__icon"
              icon="heart"
              size="1.25rem"
            />
          </SfButton>
          <!--<SfButton
            v-e2e="'app-header-cart'"
            class="sf-button&#45;&#45;pure sf-header__action"
            @click="toggleCartSidebar"
          >
            <SfIcon
              class="sf-header__icon"
              icon="empty_cart"
              size="1.25rem"
            />
            <SfBadge v-if="cartTotalItems" class="sf-badge&#45;&#45;number cart-badge">{{cartTotalItems}}</SfBadge>
          </SfButton>-->
        </div>
      </template>
      <template #search>
        <SfSearchBar
          ref="searchBarRef"
          :placeholder="$t('Search for items')"
          aria-label="Search"
          class="sf-header__search"
          :value="term"
          @input="handleSearch"
          @keydown.enter="handleSearch($event)"
          @focus="isSearchOpen = true"
          @keydown.esc="closeSearch"
          v-click-outside="closeSearch"
        >
          <template #icon>
            <SfButton
              v-if="!!term"
              class="sf-search-bar__button sf-button--pure"
              @click="closeOrFocusSearchBar"
            >
              <span class="sf-search-bar__icon">
                <SfIcon color="var(--c-text)" size="18px" icon="cross" />
              </span>
            </SfButton>
            <SfButton
              v-else
              class="sf-search-bar__button sf-button--pure"
              @click="isSearchOpen ? isSearchOpen = false : isSearchOpen = true"
            >
              <span class="sf-search-bar__icon">
                <SfIcon color="var(--c-text)" size="20px" icon="search" />
              </span>
            </SfButton>
          </template>
        </SfSearchBar>
      </template>
    </SfHeader>
    <SearchResults :visible="isSearchOpen" :result="result" @close="closeSearch" @removeSearchResults="removeSearchResults" />
    <SfOverlay :visible="isSearchOpen" />
  </div>
</template>

<script>
import { SfHeader, SfImage, SfIcon, SfButton, SfBadge, SfSearchBar, SfOverlay, SfMenuItem, SfLink } from '@storefront-ui/vue';
import { useUiState } from '~/composables';
import { useCart, useWishlist, useFacet, useUser, cartGetters, categoryGetters } from '@vue-storefront/numerbay';
import { computed, ref, onBeforeUnmount, watch } from '@vue/composition-api';
import { onSSR } from '@vue-storefront/core';
import { useUiHelpers } from '~/composables';
import LocaleSelector from './LocaleSelector';
import SearchResults from '~/components/SearchResults';
import HeaderNavigation from './HeaderNavigation';
import { clickOutside } from '@storefront-ui/vue/src/utilities/directives/click-outside/click-outside-directive.js';
import {
  mapMobileObserver,
  unMapMobileObserver
} from '@storefront-ui/vue/src/utilities/mobile-observer.js';
import debounce from 'lodash.debounce';

export default {
  components: {
    SfHeader,
    SfImage,
    LocaleSelector,
    SfIcon,
    SfButton,
    SfBadge,
    SfSearchBar,
    SearchResults,
    SfOverlay,
    SfMenuItem,
    SfLink,
    HeaderNavigation
  },
  directives: { clickOutside },
  setup(props, { root }) {
    const { toggleCartSidebar, toggleWishlistSidebar, toggleLoginModal, isMobileMenuOpen } = useUiState();
    const { setTermForUrl, getFacetsFromURL } = useUiHelpers();
    const { isAuthenticated, load: loadUser } = useUser();
    const { cart, load: loadCart } = useCart();
    const { load: loadWishlist } = useWishlist();
    const {
      result: searchResult,
      search: productsSearch
      // loading: productsLoading,
    } = useFacet('AppHeader:Products');
    // const {
    //   categories: categoryList,
    //   search: categoriesListSearch,
    // } = useCategory('AppHeader:CategoryList');

    const term = ref(getFacetsFromURL().phrase);
    const isSearchOpen = ref(false);
    const searchBarRef = ref(null);
    const result = ref(null);

    const cartTotalItems = computed(() => {
      const count = cartGetters.getTotalItems(cart.value);
      return count ? count.toString() : null;
    });

    const accountIcon = computed(() => isAuthenticated.value ? 'profile_fill' : 'profile');

    const handleAccountClick = async () => {
      if (isAuthenticated.value) {
        return root.$router.push('/my-account');
      }

      toggleLoginModal();
    };

    onSSR(async () => {
      await loadUser();
      await loadCart();
      if (isAuthenticated.value) {
        await loadWishlist();
      }
    });

    const closeSearch = () => {
      if (!isSearchOpen.value) return;

      term.value = '';
      isSearchOpen.value = false;
    };

    const handleSearch = debounce(async (paramValue) => {
      term.value = !paramValue.target ? paramValue : paramValue.target.value;
      await Promise.all([
        productsSearch({
          categorySlug: 'all',
          itemsPerPage: 12,
          term: term.value
        })
        // categoriesSearch({
        //   term: term.value,
        // }),
      ]);

      result.value = {
        products: searchResult.value?.data?.products,
        categories: categoryGetters.getTree(searchResult.value?.data?.categories[0])
      };
    }, 1000);

    const isMobile = ref(mapMobileObserver().isMobile.get());

    const closeOrFocusSearchBar = () => {
      if (isMobile.value) {
        return closeSearch();
      } else {
        term.value = '';
        return searchBarRef.value.$el.children[0].focus();
      }
    };

    watch(() => term.value, (newVal, oldVal) => {
      const shouldSearchBeOpened = (!isMobile.value && term.value.length > 0) && ((!oldVal && newVal) || (newVal.length !== oldVal.length && isSearchOpen.value === false));
      if (shouldSearchBeOpened) {
        isSearchOpen.value = true;
      }
    });

    const removeSearchResults = () => {
      result.value = null;
    };

    onBeforeUnmount(() => {
      unMapMobileObserver();
    });

    return {
      accountIcon,
      cartTotalItems,
      handleAccountClick,
      toggleCartSidebar,
      toggleWishlistSidebar,
      setTermForUrl,
      term,
      isSearchOpen,
      closeSearch,
      handleSearch,
      result,
      closeOrFocusSearchBar,
      searchBarRef,
      isMobile,
      isMobileMenuOpen,
      removeSearchResults
    };
  }
};
</script>

<style lang="scss" scoped>
.sf-header {
  --header-padding:  var(--spacer-sm);
  @include for-desktop {
    --header-padding: 0;
  }
  &__logo-image {
      height: 100%;
  }
}
.header-on-top {
  z-index: 2;
}
.nav-item {
  --header-navigation-item-margin: 0 var(--spacer-base);
  .sf-header-navigation-item__item--mobile {
    display: none;
  }
  @include for-mobile {
    //--header-navigation-item-menu-item-margin: 0;
  }
}

.cart-badge {
  position: absolute;
  bottom: 40%;
  left: 40%;
}
</style>
