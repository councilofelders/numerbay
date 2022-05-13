<template>
  <div class="header-menu-action d-flex">
    <div class="header-search-mobile dropdown mx-2 d-none d-xl-none d-lg-flex">
      <a class="icon-btn" data-bs-toggle="dropdown" href="#">
        <em class="ni ni-search"></em>
      </a>
      <div class="dropdown-menu dropdown-menu-end card-generic">
        <div class="input-group">
          <input class="form-control form-control-s1" placeholder="Search item here..." type="search">
          <a class="btn btn-sm btn-outline-secondary" href="#"><em class="ni ni-search"></em></a>
        </div>
      </div>
    </div><!-- end header-search-mobile -->
    <a class="icon-btn d-none d-xl-none d-lg-grid" href="wallet.html">
      <em class="ni ni-wallet"></em>
    </a>
  </div><!-- end -->
</template>
<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js'

export default {
  name: 'HeaderAction',
  data() {
    return {
      SectionData
    }
  }
}
</script>
