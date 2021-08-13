import { CustomQuery } from '@vue-storefront/core';
import {authHeaders} from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function getProduct(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('products/search', context.config.api.url);
  const token = context.config.auth.onTokenRead();

  const payload = {
    id: params.id,
    // eslint-disable-next-line camelcase
    category_id: params.catId,
    limit: params.limit,
    skip: params.offset,
    filters: params.filters,
    term: params.term,
    sort: params.sort
  };

  // Use axios to send a POST request
  const { data } = await context.client.post(url.href, payload, authHeaders(token));

  // Return data from the API
  return data;
}

