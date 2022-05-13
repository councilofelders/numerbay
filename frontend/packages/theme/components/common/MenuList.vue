<template>
  <ul class="menu-list ms-lg-auto">
    <li class="menu-item">
      <nuxt-link class="menu-link menu-toggle" to="/">Home</nuxt-link>
    </li>
    <li class="menu-item has-sub">
      <nuxt-link class="menu-link menu-toggle" to="/explore/numerai-predictions">Numerai</nuxt-link>
      <div class="menu-sub">
        <ul class="menu-list">
          <li class="menu-item">
            <nuxt-link class="menu-link" to="/explore/numerai-predictions">Predictions</nuxt-link>
          </li>
          <li class="menu-item">
            <nuxt-link class="menu-link" to="/explore/numerai-models">Models</nuxt-link>
          </li>
        </ul>
      </div>
    </li>
    <li class="menu-item has-sub">
      <nuxt-link class="menu-link menu-toggle" to="/explore/signals-predictions">Signals</nuxt-link>
      <div class="menu-sub">
        <ul class="menu-list">
          <li class="menu-item">
            <nuxt-link class="menu-link" to="/explore/signals-predictions">Predictions</nuxt-link>
          </li>
          <li class="menu-item">
            <nuxt-link class="menu-link" to="/explore/signals-data">Data</nuxt-link>
          </li>
        </ul>
      </div>
    </li>
    <li class="menu-item">
      <a class="menu-link" href="https://docs.numerbay.ai/" target="_blank">Docs</a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'MenuList'
};
</script>
