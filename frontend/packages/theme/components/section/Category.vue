<template>
  <section class="category-section" :class="classname">
    <div class="container">
      <!-- section heading -->
      <SectionHeading classname="text-center" :text="SectionData.categoryData.title"
                      :content="SectionData.categoryData.content" isMargin="mb-3"></SectionHeading>
      <div class="row g-gs">
        <div class="col-lg-4 col-6" v-for="item in SectionData.categoryData.categoryList" :key="item.id">
          <router-link :to="item.path" class="card card-cat text-center h-100" :class="item.class">
            <div class="card-body card-body-s1">
              <span :class="item.icon"></span>
              <h5 class="card-cat-title">{{ item.title }}</h5>
            </div>
          </router-link>
        </div><!-- end col -->
      </div><!-- end row -->
    </div><!-- end container -->
  </section><!-- end category-section -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

export default {
  name: 'Category',
  props: ['classname'],
  data() {
    return {
      SectionData
    };
  }
};
</script>
