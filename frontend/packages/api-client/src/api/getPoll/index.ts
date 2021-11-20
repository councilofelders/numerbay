import { CustomQuery } from '@vue-storefront/core';
import {authHeaders} from "../utils";

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function getPoll(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const token = context.config.auth.onTokenRead();

  const url = new URL(token ? 'polls/search-authenticated' : 'polls/search', context.config.api.url);

  const payload = {
    id: params.id,
    limit: params.limit,
    skip: params.offset,
    filters: params.filters,
    term: params.term,
    sort: params.sort
  };

  // Use axios to send a POST request
  const { data } = await context.client.post(url.href, payload, token ? authHeaders(token) : null);

  // Return data from the API
  return data;
}

