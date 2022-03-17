import { CustomQuery } from '@vue-storefront/core';
import { authHeaders } from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function getProduct(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const token = context.config.auth.onTokenRead();

  const url = new URL(token ? 'products/search-authenticated' : 'products/search', context.config.api.url);

  const payload = {
    id: params.id,
    // eslint-disable-next-line camelcase
    category_id: params.catId,
    limit: params.limit,
    skip: params.offset,
    filters: params.filters,
    term: params.term,
    name: params.name,
    // eslint-disable-next-line camelcase
    category_slug: params.categorySlug,
    sort: params.sort,
    coupon: params.coupon,
    qty: params.qty
  };

  // Use axios to send a POST request
  const { data } = await context.client.post(url.href, payload, token ? authHeaders(token) : null).catch(async () => {
    if (token) {
      // retry without token
      return await context.client.post((new URL('products/search', context.config.api.url)).href, payload);
    }
  });

  // Return data from the API
  return data;
}

