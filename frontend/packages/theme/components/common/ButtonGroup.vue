<template>
    <ul class="btns-group" :class="classname">
        <li v-for="(btn, i) in btns" :key="i">
            <router-link :to="btn.path" class="btn" :class="btn.btnClass">
                {{ btn.title }}
                <span class="d-none d-xl-inline-block" v-if="istext">{{ btn.titleTwo }}</span>
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
