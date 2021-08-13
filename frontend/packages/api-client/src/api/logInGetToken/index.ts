import { CustomQuery } from '@vue-storefront/core';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function logInGetToken(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('login/access-token', context.config.api.url);

  // Add parameters passed from composable as post query (x-www-form-urlencoded)
  const postParams = new URLSearchParams();
  postParams.append('username', params.username);
  postParams.append('password', params.password);

  // Use axios to send a POST request
  const { data } = await context.client.post(url.href, postParams).catch((error) => {
    if (error.response) {
      error.response.data.error = error.response.status;
      return error.response;
    }
  });

  if (data?.access_token) {
    await context.config.auth.onTokenChange(data.access_token);
  }

  // Return data from the API
  return data;
}

