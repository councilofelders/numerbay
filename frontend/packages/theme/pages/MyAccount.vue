<template>
  <div id="my-account">
    <SfBreadcrumbs
      class="breadcrumbs desktop-only"
      :breadcrumbs="breadcrumbs"
    >
      <template #link="{breadcrumb}">
        <router-link :to="breadcrumb.route.link" class="sf-breadcrumbs__breadcrumb">
          {{ breadcrumb.text }}
        </router-link>
      </template>
    </SfBreadcrumbs>
    <SfContentPages
      v-e2e="'my-account-content-pages'"
      title="My Account"
      :active="activePage"
      class="my-account"
      @click:change="changeActivePage"
    >
      <SfContentCategory title="Account">
        <SfContentPage title="My profile">
          <MyProfile />
        </SfContentPage>
        <SfContentPage title="Numerai API">
          <NumeraiApi />
        </SfContentPage>
        <SfContentPage title="Log out" />
      </SfContentCategory>
      <SfContentCategory title="Seller">
        <SfContentPage title="My listings">
          <MyListings />
        </SfContentPage>
        <SfContentPage title="Sales history">
          <SalesHistory />
        </SfContentPage>
      </SfContentCategory>

      <SfContentCategory title="Buyer">
        <SfContentPage title="Order history">
          <OrderHistory />
        </SfContentPage>

        <!--<SfContentPage title="My reviews">
          <MyReviews />
        </SfContentPage>-->
      </SfContentCategory>
    </SfContentPages>
  </div>
</template>
<script>
import { SfBreadcrumbs, SfContentPages } from '@storefront-ui/vue';
import { computed } from '@vue/composition-api';
import { useUser } from '@vue-storefront/numerbay';
import MyProfile from './MyAccount/MyProfile';
import NumeraiApi from './MyAccount/NumeraiApi';
import MyListings from './MyAccount/MyListings';
import SalesHistory from './MyAccount/SalesHistory';
import OrderHistory from './MyAccount/OrderHistory';
import {Logger} from '@vue-storefront/core';

export default {
  name: 'MyAccount',
  components: {
    SfBreadcrumbs,
    SfContentPages,
    MyProfile,
    NumeraiApi,
    MyListings,
    SalesHistory,
    OrderHistory
  },
  middleware: [
    'is-authenticated'
  ],
  setup(props, context) {
    const { $router, $route } = context.root;
    const { logout, disconnectWeb3Modal } = useUser();
    const activePage = computed(() => {
      const { pageName } = $route.params;

      if (pageName) {
        if (pageName === 'numerai-api') return 'Numerai API';
        return (pageName.charAt(0).toUpperCase() + pageName.slice(1)).replace('-', ' ');
      }

      return 'My profile';
    });

    const changeActivePage = async (title) => {
      if (title === 'Log out') {
        await logout();
        // log out of metamask
        try {
          await disconnectWeb3Modal();
        } catch (e) {
          Logger.error(e);
        }
        $router.push('/');
        return;
      }

      $router.push(`/my-account/${(title || '').toLowerCase().replace(' ', '-')}`);
    };

    return { changeActivePage, activePage };
  },

  data() {
    return {
      breadcrumbs: [
        {
          text: 'Home',
          route: { link: '/' }
        },
        {
          text: 'My Account',
          route: { link: '#' }
        }
      ]
    };
  }
};
</script>

<style lang='scss' scoped>
#my-account {
  box-sizing: border-box;
  @include for-desktop {
    max-width: 1240px;
    margin: 0 auto;
  }
}
.my-account {
  @include for-mobile {
    --content-pages-sidebar-category-title-font-weight: var(
      --font-weight--normal
    );
    --content-pages-sidebar-category-title-margin: var(--spacer-sm)
      var(--spacer-sm) var(--spacer-sm) var(--spacer-base);
  }
  @include for-desktop {
    --content-pages-sidebar-category-title-margin: var(--spacer-xl) 0 0 0;
  }
}
.breadcrumbs {
  margin: var(--spacer-base) 0 var(--spacer-lg);
}
</style>
