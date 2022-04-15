<template>
  <nav class="header-menu menu nav">
    <!-- menu list -->
    <MenuList></MenuList>
    <!-- header btn -->
    <ul class="menu-btns menu-btns-2">
      <li class="d-none d-lg-inline-block dropdown">
        <button type="button" class="icon-btn icon-btn-s1" data-bs-toggle="dropdown"><em class="ni ni-user"></em>
        </button>
        <ul class="dropdown-menu card-generic card-generic-s3 dropdown-menu-end mt-2">
          <li><h6 class="dropdown-header">Hello {{ username }}!</h6></li>
          <li>
            <router-link class="dropdown-item card-generic-item" to="/account"><em class="ni ni-setting me-2"></em>Account
              Settings
            </router-link>
          </li>
          <li><a class="dropdown-item card-generic-item" href="https://docs.numerbay.ai/" target="_blank"><em
            class="ni ni-question-alt me-2"></em>Docs</a></li>
          <li><a href="#" class="dropdown-item card-generic-item theme-toggler" title="Toggle Dark/Light mode"><em
            class="ni ni-moon me-2"></em> Dark Mode</a></li>
          <li>
            <hr class="dropdown-divider">
          </li>
          <li>
            <button class="dropdown-item card-generic-item" @click="onLogout"><em class="ni ni-power me-2"></em>Logout
            </button>
          </li>
        </ul>
      </li>
    </ul>
  </nav><!-- .header-menu -->
</template>

<script>
// @ is an alias to /src
import MenuList from '@/components/common/MenuList.vue';

// Composables
import {computed} from '@vue/composition-api';
import {useUser} from '@vue-storefront/numerbay';

export default {
  name: 'MenuTwo',
  props: ['classname'],
  components: {
    MenuList
  },
  mounted() {

    /*  ==========================================
      Dark/Light mode configaration
    ========================================== */
    function themeSwitcher(selector) {
      const themeToggler = document.querySelectorAll(selector);
      if (themeToggler.length > 0) {
        themeToggler.forEach(item => {
          item.addEventListener('click', (e) => {
            e.preventDefault();
            document.body.classList.toggle('dark-mode');
            if (document.body.classList.contains('dark-mode')) {
              localStorage.setItem('website_theme', 'dark-mode');
            } else {
              localStorage.setItem('website_theme', 'default');
            }
          });
        });
      }

      function retrieveTheme() {
        const theme = localStorage.getItem('website_theme');
        if (theme !== null) {
          document.body.classList.remove('default', 'dark-mode');
          document.body.classList.add(theme);
        }
      }

      retrieveTheme();

      if (window) {
        window.addEventListener('storage', () => {
          retrieveTheme();
        }, false);
      }
    }

    themeSwitcher('.theme-toggler');
  },
  methods: {
    async onLogout() {
      await this.logout();
      await this.$router.push('/');
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
