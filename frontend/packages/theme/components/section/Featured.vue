/* eslint-disable no-undef */
<template>
  <section class="section-space-b feature-section">
    <div class="container">
      <!-- section heading -->
      <SectionHeading classname="text-center" :text="SectionData.featuredData.title"
                      :content="SectionData.featuredData.content" isMargin="mb-3"></SectionHeading>
      <div class="row g-gs">
        <div class="col-sm-6 col-md-6 col-lg-3" v-for="item in []" :key="item.id">
          <router-link :to="item.path" class="card card-full">
            <img :src="item.img" class="card-img-top" alt="featured miage">
            <div class="card-body p-4">
              <h5 class="card-title">{{ item.title }}</h5>
              <p class="small">{{ item.content }}</p>
            </div><!-- end card-body -->
          </router-link><!-- end card -->
        </div><!-- end col -->
      </div>
    </div><!-- .container -->
  </section><!-- end featured-creator-section -->
</template>
<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

export default {
  name: 'Featured',
  data() {
    return {
      SectionData
    };
  }
};
</script>
