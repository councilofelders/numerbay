import { CustomQuery } from '@vue-storefront/core';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export default async function getCategory(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('categories/', context.config.api.url);

  // Add parameters passed from composable as query strings to the URL
  params.slug && url.searchParams.set('slug', params.slug);

  // Use axios to send a GET request
  const { data } = await context.client.get(url.href);

  // Return data from the API
  return data;
}
