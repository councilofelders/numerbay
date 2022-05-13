<template>
  <router-link :class="classname" class="logo-link" to="/">
    <img :src="require('@/images/logo-black.png')" alt="logo" class="logo-dark logo-img">
    <img :src="require('@/images/logo-white.png')" alt="logo" class="logo-light logo-img">
    <h4 class="d-inline-block align-middle">NumerBay</h4>
  </router-link>
</template>
<script>

export default {
  name: 'LogoLink',
  props: ['classname']
};
</script>
