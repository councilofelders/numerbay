import { CustomQuery } from '@vue-storefront/core';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function getSalesLeaderboard(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('products/sales-leaderboard', context.config.api.url);

  const payload = {
    // eslint-disable-next-line camelcase
    category_slug: params.categorySlug,
    limit: params.limit,
    skip: params.offset
  };

  // Use axios to send a POST request
  const { data } = await context.client.post(url.href, payload);

  // Return data from the API
  return data;
}

