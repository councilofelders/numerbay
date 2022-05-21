const path = require('path');

export function getRoutes(themeDir = __dirname) {
  return [
    {
      path: '/',
      component: path.resolve(themeDir, 'pages/Home.vue')
    },
    {
      path: '/stats',
      component: path.resolve(themeDir, 'pages/Stats.vue')
    },
    {
      path: '/product/:id(\\d+)',
      name: 'ProductDetailsByID',
      component: path.resolve(themeDir, 'pages/ProductDetails.vue'),
      props: true
    },
    {
      path: '/product/:category/:name',
      name: 'ProductDetailsByFullName',
      component: path.resolve(themeDir, 'pages/ProductDetails.vue'),
      props: true
    },
    {
      path: '/p/:id(\\d+)', redirect: '/product/:id'
    },
    {
      path: '/p/:id(\\d+)/:slug', redirect: '/product/:id'
    },
    {
      path: '/explore',
      redirect: '/explore/all'
    },
    {
      path: '/c/:slug_1/:slug_2?/:slug_3?/:slug_4?/:slug_5?',
      redirect: '/explore/:slug_1/:slug_2?/:slug_3?/:slug_4?/:slug_5?'
    },
    {
      path: '/explore/:slug_1/:slug_2?/:slug_3?/:slug_4?/:slug_5?',
      name: 'explore',
      component: path.resolve(themeDir, 'pages/Explore.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: path.resolve(themeDir, 'pages/Login.vue')
    },
    {
      path: '/login-v2',
      name: 'login v2',
      component: path.resolve(themeDir, 'pages/Login-v2.vue'),
      props: true
    },
    {
      path: '/listings',
      name: 'listings',
      component: path.resolve(themeDir, 'pages/Listings.vue')
    },
    {
      path: '/create-listing',
      name: 'create-listing',
      component: path.resolve(themeDir, 'pages/CreateListing.vue')
    },
    {
      path: '/edit-listing/:id(\\d+)',
      name: 'edit-listing',
      component: path.resolve(themeDir, 'pages/CreateListing.vue'),
      props: true
    },
    {
      path: '/manage-artifacts/:id(\\d+)',
      name: 'manage-artifacts',
      component: path.resolve(themeDir, 'pages/ManageArtifacts.vue'),
      props: true
    },
    {
      path: '/purchases',
      name: 'purchases',
      component: path.resolve(themeDir, 'pages/Purchases.vue')
    },
    {
      path: '/sales',
      name: 'sales',
      component: path.resolve(themeDir, 'pages/Sales.vue')
    },
    {
      path: '/account',
      name: 'account',
      component: path.resolve(themeDir, 'pages/Account.vue')
    },
    {
      path: '/numerai-settings',
      name: 'numerai-settings',
      component: path.resolve(themeDir, 'pages/NumeraiSettings.vue')
    },
    {
      path: '/polls',
      name: 'polls',
      component: path.resolve(themeDir, 'pages/Polls.vue')
    },
    {
      path: '/create-poll',
      name: 'create-poll',
      component: path.resolve(themeDir, 'pages/CreatePoll.vue')
    },
    {
      path: '/edit-poll/:id',
      name: 'edit-poll',
      component: path.resolve(themeDir, 'pages/CreatePoll.vue'),
      props: true
    },
    {
      path: '/vote/:id',
      name: 'vote',
      component: path.resolve(themeDir, 'pages/Vote.vue')
    },
    {
      path: '/coupons',
      name: 'coupons',
      component: path.resolve(themeDir, 'pages/Coupons.vue')
    },
    {
      path: '/create-coupon',
      name: 'create-coupon',
      component: path.resolve(themeDir, 'pages/CreateCoupon.vue')
    },
  ];
}
