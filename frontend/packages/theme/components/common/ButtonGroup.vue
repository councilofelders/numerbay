<template>
  <ul :class="classname" class="btns-group">
    <li v-for="(btn, i) in btns" :key="i">
      <router-link :class="btn.btnClass" :to="btn.path" class="btn">
        {{ btn.title }}
        <span v-if="istext" class="d-none d-xl-inline-block">{{ btn.titleTwo }}</span>
      </router-link>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'ButtonGroup',
  props: ['btns', 'istext', 'classname']
}
</script>
