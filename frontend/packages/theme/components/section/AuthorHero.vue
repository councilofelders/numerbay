<template>
  <div class="hero-wrap sub-header">
    <div class="overlay"></div>
    <div class="container">
      <div class="hero-content py-0 d-flex align-items-center">
        <div class="author-hero-content-wrap d-flex flex-wrap justify-content-between ms-3 flex-grow-1">
          <div class="author-hero-content me-3">
            <h4 class="hero-author-title mb-1 text-white">{{ username }}</h4>
          </div><!-- author-hero-conetent -->
        </div><!-- author-hero-content -->
      </div><!-- hero-content -->
    </div><!-- .container-->
  </div><!-- end hero-wrap -->
</template>

<script>
// Composables
import {computed} from '@vue/composition-api';
import {useUser} from '@vue-storefront/numerbay';

export default {
  name: 'AuthorHero',
  setup() {
    const {user} = useUser();

    return {
      username: computed(() => user.value ? user.value.username : '')
    };
  }
};
</script>
