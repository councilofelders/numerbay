<template>
    <div class="row g-gs justify-content-center">
        <div class="col-10 col-sm-6 col-lg-3" v-for="item in SectionData.howItWorkData.howItWorkListThree" :key="item.id">
            <div class="card-hiw card-hiw-s3">
                <div class="d-flex align-items-center mb-3">
                    <span :class="item.icon"></span>
                    <h5>{{ item.title }}</h5>
                </div>
                <p class="card-text-s1" v-html="item.content"></p>
            </div>
        </div><!-- end col -->
    </div><!-- end row -->
</template>
<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js'

export default {
  name: 'HowItWorkItem',
  data () {
    return {
      SectionData
    }
  }
}
</script>