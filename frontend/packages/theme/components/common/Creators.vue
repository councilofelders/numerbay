<template>
  <div class="row g-gs">
    <div class="col-lg-4 col-sm-6" v-for="item in []" :key="item.id">
      <div class="card card-creator-s1">
        <div class="card-body">
          <router-link :to="item.path" class="avatar avatar-1 flex-shrink-0">
            <img :src="item.img" alt="avatar">
          </router-link>
          <div class="flex-grow-1">
            <router-link :to="item.path" class="text-black fw-semibold">{{ item.title }}</router-link>
            <span class="d-block fw-medium">{{ item.subTitle }}</span>
          </div>
        </div>
      </div><!-- end card -->
    </div><!-- end col-lg-4 -->
  </div><!-- row -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

export default {
  name: 'Creators',
  data() {
    return {
      SectionData
    };
  }
};
</script>
