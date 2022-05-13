<template>
  <nav class="header-menu menu nav">
    <!-- menu list -->
    <MenuList></MenuList>
    <!-- header btn -->
    <ul class="menu-btns">
      <li>
        <ButtonLink :class="classname" :text="SectionData.headerData.btnText" classname="btn"
                    link="/login-v2"></ButtonLink>
      </li>
      <li>
        <ThemeSwitcher></ThemeSwitcher>
      </li>
    </ul>
  </nav><!-- .header-menu -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

// @ is an alias to /src
import MenuList from '@/components/common/MenuList.vue';

export default {
  name: 'Menu',
  props: ['classname'],
  components: {
    MenuList
  },
  data() {
    return {
      SectionData
    };
  }
};
</script>
