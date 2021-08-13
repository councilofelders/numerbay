import { CustomQuery } from '@vue-storefront/core';
import { authHeaders } from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function getMe(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('users/me', context.config.api.url);
  const token = context.config.auth.onTokenRead();
  const { data } = await context.client.get(url.href, authHeaders(token));
  // Return data from the API
  return data;
}

