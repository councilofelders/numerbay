<template>
  <nuxt-link :class="classname" :to="link">{{ text }}</nuxt-link>
</template>

<script>
export default {
  name: 'ButtonLink',
  props: ['text', 'classname', 'link']
}
</script>
