import { CustomQuery } from '@vue-storefront/core';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function signUpUser(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('users/', context.config.api.url);

  const payload = {
    username: params.username,
    password: params.password
  };

  // Use axios to send a POST request
  const { data } = await context.client.post(url.href, payload).catch((error) => {
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
