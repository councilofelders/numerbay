import { CustomQuery } from '@vue-storefront/core';
import { authHeaders } from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function userSyncNumerai(context, params) {
  // Create URL object containing full endpoint URL
  const url = new URL('users/sync-numerai', context.config.api.url);
  const token = context.config.auth.onTokenRead();

  // Use axios to send a PUT request
  const { data } = await context.client.post(url.href, null, authHeaders(token)).catch((error) => {
    if (error.response) {
      error.response.data.error = error.response.status;
      return error.response;
    }
  });

  // Return data from the API
  return data;
}

