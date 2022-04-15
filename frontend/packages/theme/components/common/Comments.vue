<template>
  <ul class="comments">
    <li v-for="item in []" :key="item.id">
      <div class="comment">
        <div class="avatar flex-shrink-0 me-3">
          <img :src="item.img" alt="">
        </div>
        <div class="comment-body">
          <div class="d-flex align-items-center justify-content-between">
            <div class="me-2">
              <h5 class="comment-title">{{ item.title }}</h5>
              <span class="comment-meta">{{ item.date }}</span>
            </div>
            <a class="btn-link comment-replay-btn" href="#"><em class="ni ni-reply"></em> {{ item.btnText }} </a>
          </div>
          <p class="comment-desc mt-2">{{ item.content }}</p>
        </div><!-- end comment-body -->
      </div><!-- end comment -->
      <ul>
        <li v-for="replyItem in item.replyList" :key="replyItem.id">
          <div class="comment">
            <div class="avatar flex-shrink-0 me-3">
              <img :src="replyItem.img" alt="">
            </div>
            <div class="comment-body">
              <div class="d-flex align-items-center justify-content-between">
                <div class="me-2">
                  <h5 class="comment-title">{{ replyItem.title }}</h5>
                  <span class="comment-meta">{{ replyItem.date }}</span>
                </div>
                <a class="btn-link comment-replay-btn" href="#"><em class="ni ni-reply"></em> {{ replyItem.btnText }}
                </a>
              </div>
              <p class="comment-desc mt-2">{{ replyItem.content }}</p>
            </div><!-- end comment-body -->
          </div><!-- end comment -->
        </li>
      </ul>
    </li>
  </ul>
</template>
<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

export default {
  name: 'Comments',
  data() {
    return {
      SectionData
    };
  }
};
</script>
