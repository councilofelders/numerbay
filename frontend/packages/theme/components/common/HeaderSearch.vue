<template>
  <div :class="classname" class="header-search-form">
    <input v-model="searchTerm" class="form-control form-control-s1" placeholder="Search item here..." type="search"
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
