<template>
  <ul class="menu-list ms-lg-auto">
    <li class="menu-item">
      <router-link to="/" class="menu-link menu-toggle">Home</router-link>
    </li>
    <li class="menu-item has-sub">
      <router-link to="/explore/numerai-predictions" class="menu-link menu-toggle">Numerai</router-link>
      <div class="menu-sub">
        <ul class="menu-list">
          <li class="menu-item">
            <router-link to="/explore/numerai-predictions" class="menu-link">Predictions</router-link>
          </li>
          <li class="menu-item">
            <router-link to="/explore/numerai-models" class="menu-link">Models</router-link>
          </li>
        </ul>
      </div>
    </li>
    <li class="menu-item has-sub">
      <router-link to="/explore/signals-predictions" class="menu-link menu-toggle">Signals</router-link>
      <div class="menu-sub">
        <ul class="menu-list">
          <li class="menu-item">
            <router-link to="/explore/signals-predictions" class="menu-link">Predictions</router-link>
          </li>
          <li class="menu-item">
            <router-link to="/explore/signals-data" class="menu-link">Data</router-link>
          </li>
        </ul>
      </div>
    </li>
<!--    <li class="menu-item has-sub">
      <router-link to="/explore/onlyfams" class="menu-link menu-toggle">OnlyFams</router-link>
      <div class="menu-sub">
        <ul class="menu-list">
          <li class="menu-item">
            <router-link to="/explore/onlyfams-clothing" class="menu-link">Shirts & Hoodies</router-link>
          </li>
          <li class="menu-item">
            <router-link to="/explore/onlyfams-nft" class="menu-link">Meme NFTs</router-link>
          </li>
          <li class="menu-item">
            <router-link to="/explore/onlyfams-souvenirs" class="menu-link">Souvenir Coins</router-link>
          </li>
        </ul>
      </div>
    </li>-->
  </ul>
</template>

<script>
export default {
  name: 'MenuList'
};
</script>
