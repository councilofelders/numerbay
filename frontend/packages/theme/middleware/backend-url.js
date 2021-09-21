
export default async ({ app }) => {
  const scheme = !process.env.VUE_APP_DOMAIN_DEV || process.env.VUE_APP_DOMAIN_DEV === 'backend' || process.env.VUE_APP_DOMAIN_DEV === 'localhost' ? 'http' : 'https';
  app.$config._app.backendURL = `${scheme}://${process.env.VUE_APP_DOMAIN_DEV || 'localhost'}`;
};
