module.exports = {
  integrations: {
    numerbay: {
      location: '@vue-storefront/numerbay-api/server',
      configuration: {
        api: {
          url: `http://${process.env.VUE_APP_DOMAIN_DEV || 'localhost'}/backend-api/v1/`
        }
      }
    }
  }
};
