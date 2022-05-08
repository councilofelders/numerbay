<template>
  <ul class="menu-list ms-lg-auto">
    <li class="menu-item">
      <nuxt-link to="/" class="menu-link menu-toggle">Home</nuxt-link>
    </li>
    <li class="menu-item has-sub">
      <nuxt-link to="/explore/numerai-predictions" class="menu-link menu-toggle">Numerai</nuxt-link>
      <div class="menu-sub">
        <ul class="menu-list">
          <li class="menu-item">
            <nuxt-link to="/explore/numerai-predictions" class="menu-link">Predictions</nuxt-link>
          </li>
          <li class="menu-item">
            <nuxt-link to="/explore/numerai-models" class="menu-link">Models</nuxt-link>
          </li>
        </ul>
      </div>
    </li>
    <li class="menu-item has-sub">
      <nuxt-link to="/explore/signals-predictions" class="menu-link menu-toggle">Signals</nuxt-link>
      <div class="menu-sub">
        <ul class="menu-list">
          <li class="menu-item">
            <nuxt-link to="/explore/signals-predictions" class="menu-link">Predictions</nuxt-link>
          </li>
          <li class="menu-item">
            <nuxt-link to="/explore/signals-data" class="menu-link">Data</nuxt-link>
          </li>
        </ul>
      </div>
    </li>
    <li class="menu-item">
      <a href="https://docs.numerbay.ai/" target="_blank" class="menu-link">Docs</a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'MenuList'
};
</script>
