<template>
    <router-link :class="classname" :to="link">{{ text }}</router-link>
</template>

<script>
export default {
  name: 'ButtonLink',
  props: ['text', 'classname', 'link']
}
</script>
