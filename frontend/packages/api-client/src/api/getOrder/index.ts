import { CustomQuery } from '@vue-storefront/core';
import {authHeaders} from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function getOrder(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('orders/search', context.config.api.url);
  const token = context.config.auth.onTokenRead();

  const payload = {
    role: params.role,
    id: params.id,
    limit: params.limit,
    skip: params.offset,
    filters: params.filters,
    sort: params.sort
  };

  // Use axios to send a POST request
  const { data } = await context.client.post(url.href, payload, authHeaders(token));

  // Return data from the API
  return data;
}

