<template>
    <div class="section-head" :class="classname">
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
