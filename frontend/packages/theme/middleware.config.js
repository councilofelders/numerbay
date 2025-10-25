module.exports = {
  integrations: {
    numerbay: {
      location: '@vue-storefront/numerbay-api/server',
      configuration: {
        api: {
          url: process.env.VUE_APP_API_URL || 'http://localhost:8091/api/v1/'
        }
      }
    }
  }
};
