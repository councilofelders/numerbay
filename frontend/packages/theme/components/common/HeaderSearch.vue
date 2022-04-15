<template>
  <div class="header-search-form" :class="classname">
    <input type="search" class="form-control form-control-s1" placeholder="Search item here..." v-model="searchTerm"
           @keydown.enter="handleSearch">
  </div>
</template>
<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

export default {
  name: 'HeaderSearch',
  props: ['classname'],
  methods: {
    handleSearch() {
      this.$router.push({path: '/explore/all', query: {term: this.searchTerm}});
    }
  },
  data() {
    return {
      SectionData,
      searchTerm: this.$route.query.term
    };
  }
};
</script>
