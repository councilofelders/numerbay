import { CustomQuery } from '@vue-storefront/core';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function getPoll(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('polls/search', context.config.api.url);

  const payload = {
    id: params.id,
    limit: params.limit,
    skip: params.offset,
    filters: params.filters,
    term: params.term,
    sort: params.sort
  };

  // Use axios to send a POST request
  const { data } = await context.client.post(url.href, payload);

  // Return data from the API
  return data;
}

