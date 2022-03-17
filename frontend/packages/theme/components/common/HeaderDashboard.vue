<template>
    <div class="header-main is-sticky" :class="isTransparent">
        <div class="container">
            <div class="header-wrap">
                <!-- logo -->
                <Logo></Logo>
                <!-- mobile action -->
                <MobileActionTwo></MobileActionTwo>
                <!-- heder search -->
                <HeaderSearch class="header-search-form-s2"></HeaderSearch>
                <!-- Menu -->
                <MenuTwo classname="btn-primary"></MenuTwo>
                <div class="header-overlay"></div>
            </div><!-- .header-warp-->
        </div><!-- .container-->
    </div><!-- .header-main-->
</template>
<script>
// @ is an alias to /src
import Logo from '@/components/common/Logo.vue'
import MobileActionTwo from '@/components/common/MobileActionTwo.vue'
import HeaderSearch from '@/components/common/HeaderSearch.vue'
import MenuTwo from '@/components/common/MenuTwo.vue'

export default {
  name: 'HeaderDashboard',
  props: ['isTransparent'],
  components: {
    Logo,
    MobileActionTwo,
    HeaderSearch,
    MenuTwo
  }
}
</script>
