<template>
  <div class="header-search-form" :class="classname">
    <input type="search" class="form-control form-control-s1" placeholder="Search item here..." v-model="searchTerm"
           @keydown.enter="handleSearch">
  </div>
</template>
<script>
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
      searchTerm: this.$route.query.term
    };
  }
};
</script>
