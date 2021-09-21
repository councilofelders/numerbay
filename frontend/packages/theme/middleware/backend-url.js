
export default async ({ app }) => {
  app.$config._app.backendURL = `${!process.env.VUE_APP_DOMAIN_DEV || process.env.VUE_APP_DOMAIN_DEV === 'backend' ? 'http' : 'https'}://${process.env.VUE_APP_DOMAIN_DEV || 'localhost'}`;
};
