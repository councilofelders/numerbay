<template>
  <ul class="menu-list ms-lg-auto">
    <li class="menu-item">
      <router-link to="/" class="menu-link menu-toggle">Home</router-link>
    </li>
    <li class="menu-item has-sub">
      <router-link to="/explore/numerai" class="menu-link menu-toggle">Explore</router-link>
      <div class="menu-sub">
        <ul class="menu-list">
          <li class="menu-item">
            <router-link to="/explore/numerai" class="menu-link">Numerai</router-link>
          </li>
          <li class="menu-item">
            <router-link to="/explore/signals" class="menu-link">Signals</router-link>
          </li>
          <li class="menu-item">
            <router-link to="/explore/onlyfams" class="menu-link">OnlyFams</router-link>
          </li>
        </ul>
      </div>
    </li>
  </ul>
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

export default {
  name: 'MenuList',
  data() {
    return {
      SectionData
    };
  }
};
</script>
