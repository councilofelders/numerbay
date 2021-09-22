
export default async ({ app }) => {
  const backendURL = process.env.VUE_APP_DOMAIN_DEV;
  if (backendURL) {
    const scheme = !backendURL || backendURL === 'backend' || backendURL === 'localhost' ? 'http' : 'https';
    app.$config._app.backendURL = `${scheme}://${backendURL || 'localhost'}`;
    console.log('backendURL', backendURL);
  }
};
