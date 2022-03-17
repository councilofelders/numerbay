<template>
  <div class="page-wrap">
    <!-- header  -->
    <header class="header-section has-header-main bg-pattern-3">
        <!-- Header main -->
        <HeaderMain></HeaderMain>
        <!-- hero -->
        <AuthorHero avatarSize="avatar-3"></AuthorHero>
    </header>
    <Nuxt :key="$route.fullPath"/>
    <Notification/>
    <!-- Footer  -->
    <Footer classname="bg-dark on-dark"></Footer>
  </div><!-- end page-wrap -->
</template>
