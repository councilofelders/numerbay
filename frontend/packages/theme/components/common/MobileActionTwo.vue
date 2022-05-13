/* eslint-disable no-unused-expressions */
/* eslint-disable no-unused-expressions */
<template>
  <div class="header-mobile-action">
    <div class="header-search-mobile dropdown me-2">
      <a class="icon-btn" data-bs-toggle="dropdown" href="javascript:void(0)" @click="toggleMobileSearchDropdown"><em
        class="ni ni-search"></em></a>
      <div :class="showMobileSearchDropdown? 'show' : ''" class="dropdown-menu dropdown-menu-end card-generic">
        <div class="input-group">
          <input v-model="searchTerm" class="form-control form-control-s1" placeholder="Search item here..."
                 type="search" @keydown.enter="handleSearch">
          <a class="btn btn-sm btn-outline-secondary" href="javascript:void(0)" @click="handleSearch"><em
            class="ni ni-search"></em></a>
        </div>
      </div>
    </div><!-- end header-search-mobile -->
    <div class="header-mobile-user-menu me-2">
      <button class="icon-btn" data-bs-toggle="dropdown" type="button"><em class="ni ni-user"></em></button>
      <ul class="dropdown-menu card-generic card-generic-s3 dropdown-menu-end mt-2">
        <li><h6 class="dropdown-header">Hello {{ username }}!</h6></li>
        <li>
          <router-link class="dropdown-item card-generic-item" to="/account"><em class="ni ni-setting me-2"></em>Account
            Settings
          </router-link>
        </li>
        <li><a class="dropdown-item card-generic-item" href="https://docs.numerbay.ai/" target="_blank"><em
          class="ni ni-question-alt me-2"></em>Docs</a></li>
        <li><a class="dropdown-item card-generic-item theme-toggler" href="#" title="Toggle Dark/Light mode"><em
          class="ni ni-moon me-2"></em> Dark Mode</a></li>
        <li>
          <hr class="dropdown-divider">
        </li>
        <li>
          <button class="dropdown-item card-generic-item" @click="onLogout"><em class="ni ni-power me-2"></em>Logout
          </button>
        </li>
      </ul>
    </div><!-- end hheader-mobile-user-menu -->
    <div class="header-toggle">
      <button class="menu-toggler">
        <em class="menu-on menu-icon ni ni-menu"></em>
        <em class="menu-off menu-icon ni ni-cross"></em>
      </button>
    </div><!-- .header-toggle -->
  </div><!-- end header-mobile-action -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component

// Composables
import {computed} from '@vue/composition-api';
import {useUser} from '@vue-storefront/numerbay';

export default {
  name: 'MobileAction',
  data() {
    return {
      showMobileSearchDropdown: false,
      searchTerm: this.$route.query.term
    };
  },
  mounted() {
    // slideUp
    const slideUp = (target, duration = 500) => {
      target.style.transitionProperty = 'height, margin, padding';
      target.style.transitionDuration = duration + 'ms';
      target.style.boxSizing = 'border-box';
      target.style.height = target.offsetHeight + 'px';
      // eslint-disable-next-line no-unused-expressions
      target.offsetHeight;
      target.style.overflow = 'hidden';
      target.style.height = 0;
      target.style.paddingTop = 0;
      target.style.paddingBottom = 0;
      target.style.marginTop = 0;
      target.style.marginBottom = 0;
      window.setTimeout(() => {
        target.style.display = 'none';
        target.style.removeProperty('height');
        target.style.removeProperty('padding-top');
        target.style.removeProperty('padding-bottom');
        target.style.removeProperty('margin-top');
        target.style.removeProperty('margin-bottom');
        target.style.removeProperty('overflow');
        target.style.removeProperty('transition-duration');
        target.style.removeProperty('transition-property');
      }, duration);
    };
    // slideDown
    const slideDown = (target, duration = 500) => {
      target.style.removeProperty('display');
      let display = window.getComputedStyle(target).display;
      if (display === 'none') display = 'block';
      target.style.display = display;
      const height = target.offsetHeight;
      target.style.overflow = 'hidden';
      target.style.height = 0;
      target.style.paddingTop = 0;
      target.style.paddingBottom = 0;
      target.style.marginTop = 0;
      target.style.marginBottom = 0;
      // eslint-disable-next-line no-unused-expressions
      target.offsetHeight;
      target.style.boxSizing = 'border-box';
      target.style.transitionProperty = 'height, margin, padding';
      target.style.transitionDuration = duration + 'ms';
      target.style.height = height + 'px';
      target.style.removeProperty('padding-top');
      target.style.removeProperty('padding-bottom');
      target.style.removeProperty('margin-top');
      target.style.removeProperty('margin-bottom');
      window.setTimeout(() => {
        target.style.removeProperty('height');
        target.style.removeProperty('overflow');
        target.style.removeProperty('transition-duration');
        target.style.removeProperty('transition-property');
      }, duration);
    };
    // slideToggle
    // eslint-disable-next-line no-unused-vars
    const slideToggle = (target, duration = 500) => {
      if (window.getComputedStyle(target).display === 'none') {
        return slideDown(target, duration);
      } else {
        return slideUp(target, duration);
      }
    };
    // variables for menu
    const _navbar = 'header-menu';
    // eslint-disable-next-line camelcase
    const _navbar_toggle = 'menu-toggler';
    // eslint-disable-next-line camelcase
    const _navbar_active = 'active';
    // eslint-disable-next-line camelcase
    const _navbar_fixed = 'has-fixed';
    // eslint-disable-next-line camelcase
    const _navbar_mobile = 'mobile-menu';
    // eslint-disable-next-line camelcase
    const _navbar_break = 992;
    // eslint-disable-next-line camelcase
    const _menu_toggle = 'menu-toggle';
    // eslint-disable-next-line camelcase
    const _menu_sub = 'menu-sub';
    // eslint-disable-next-line camelcase
    const _menu_active = 'active';

    const navbar = document.querySelector('.' + _navbar);
    // eslint-disable-next-line camelcase
    const navbar_toggle = document.querySelector('.' + _navbar_toggle);
    // eslint-disable-next-line camelcase
    const menu_toggle = document.querySelectorAll('.' + _menu_toggle);

    // Toggle Dropdown Menu
    function toggleDropdown(parent, subMenu, _active) {
      if (!parent.classList.contains(_active)) {
        parent.classList.add(_active);
        // eslint-disable-next-line no-undef
        slideDown(subMenu);
      } else {
        parent.classList.remove(_active);
        // eslint-disable-next-line no-undef
        slideUp(subMenu);
      }
    }

    // Close Dropdown Menu Siblings
    function closeDropdownSiblings(siblings, menu, _sub, _active) {
      Array.from(siblings).forEach(item => {
        if (item.classList.contains(_active) && !menu.classList.contains(_active)) {
          item.classList.remove(_active);
          Array.from(item.children).forEach(subItem => {
            if (subItem.classList.contains(_sub)) {
              // eslint-disable-next-line no-undef
              slideUp(subItem);
            }
          });
        }
      });
    }

    // Dropdown Menu
    function menuDropdown(toggle, _sub, _active) {
      toggle.forEach(item => {
        item.addEventListener('click', function (e) {
          e.preventDefault();
          const itemParent = item.parentElement;
          const itemSibling = item.nextElementSibling;
          const itemParentSiblings = item.parentElement.parentElement.children;
          closeDropdownSiblings(itemParentSiblings, itemParent, _sub, _active);
          toggleDropdown(itemParent, itemSibling, _active);
        });
      });
    }

    // Dropdown Menu Init
    menuDropdown(menu_toggle, _menu_sub, _menu_active);

    // mobile nav class add/remove
    function mobileNavInit() {
      // eslint-disable-next-line camelcase
      if (window.innerWidth <= _navbar_break) {
        navbar.classList.add(_navbar_mobile);
      }
    }

    mobileNavInit();

    function mobileNavResize() {
      // eslint-disable-next-line camelcase
      if (window.innerWidth <= _navbar_break) {
        navbar.classList.add(_navbar_mobile);
      } else {
        navbar.classList.remove(_navbar_mobile, _navbar_active);
        navbar_toggle.classList.remove(_navbar_active);
      }
    }

    window.addEventListener('resize', function () {
      mobileNavResize();
    });

    /*  =======================================================
  Mobile nav toggle
========================================================== */
    function mobileNavToggle() {
      navbar_toggle.classList.toggle(_navbar_active);
      navbar.classList.toggle(_navbar_active);
    }

    // eslint-disable-next-line camelcase
    if (navbar_toggle) {
      navbar_toggle.addEventListener('click', function () {
        mobileNavToggle();
      });
    }

    /*  =======================================================
  Mobile Remove / close nav when overlay is clicked
========================================================== */
    function navOutSideClick(event) {
      // eslint-disable-next-line camelcase
      if (event.target !== navbar && event.target !== navbar_toggle &&
        // eslint-disable-next-line camelcase
        event.target.closest('.' + _navbar) == null && event.target.closest('.' + _navbar_toggle) == null) {
        // eslint-disable-next-line camelcase
        if (navbar_toggle) {
          navbar_toggle.classList.remove(_navbar_active);
        }
        navbar.classList.remove(_navbar_active);
      }
    }

    document.addEventListener('click', function (event) {
      navOutSideClick(event);
    });

    /*  =======================================================
  Sticky navbar on scroll down
========================================================== */
    function stickyMenu(selector) {
      const elem = document.querySelectorAll(selector);
      if (elem.length > 0) {
        elem.forEach(item => {
          // eslint-disable-next-line camelcase
          const _item_offset = item.offsetTop;
          window.addEventListener('scroll', function () {
            // eslint-disable-next-line camelcase
            if (window.scrollY > _item_offset) {
              item.classList.add(_navbar_fixed);
            } else {
              item.classList.remove(_navbar_fixed);
            }
          });
        });
      }
    }

    stickyMenu('.is-sticky');

  },
  methods: {
    async onLogout() {
      await this.logout();
      await this.$router.push('/');
    },
    toggleMobileSearchDropdown() {
      this.showMobileSearchDropdown = !this.showMobileSearchDropdown;
    },
    handleSearch() {
      this.toggleMobileSearchDropdown();
      this.$router.push({path: '/explore/all', query: {term: this.searchTerm?.trim()}});
    }
  },
  setup() {
    const {user, logout, disconnectWeb3Modal} = useUser();

    return {
      user,
      username: computed(() => user.value ? user.value.username : ''),
      logout,
      disconnectWeb3Modal
    };
  }
};
</script>
