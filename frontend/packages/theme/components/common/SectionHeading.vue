<template>
  <div :class="classname" class="section-head">
    <h2 :class="isMargin" v-html="text"></h2>
    <p v-if="content">{{ content }}</p>
  </div><!-- end section-head -->
</template>
<script>

export default {
  name: 'SectionHeading',
  props: ['text', 'content', 'isMargin', 'classname']
}
</script>
