<template>
  <div :class="classnameTwo" class="hero-wrap sub-header">
    <div class="container">
      <div class="hero-content text-center py-0">
        <h1 :class="classname">{{ title }}</h1>
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb breadcrumb-s1 justify-content-center mt-3 mb-0">
            <li class="breadcrumb-item">
              <router-link to="/">Home</router-link>
            </li>
            <li v-for="(list, i) in lists" :key="i" class="breadcrumb-item">
              {{ list.title }}
            </li>
          </ol>
        </nav>
      </div><!-- hero-content -->
    </div><!-- .container-->
  </div><!-- end hero-wrap -->
</template>

<script>

export default {
  name: 'HeroFour',
  props: ['title', 'lists', 'classname', 'classnameTwo'],
}
</script>
