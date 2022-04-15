<template>
  <a href="#" class="theme-toggler" title="Toggle Dark/Light mode">
        <span>
          <em class="ni ni-moon icon theme-toggler-show"></em>
          <em class="ni ni-sun icon theme-toggler-hide"></em>
        </span>
    <span class="theme-toggler-text">Dark Mode</span>
  </a>
</template>

<script>
export default {
  name: 'ThemeSwither',
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
  }
};
</script>
