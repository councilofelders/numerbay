import { CustomQuery } from '@vue-storefront/core';
import { authHeaders } from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function updatePoll(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL(`polls/${params.id}`, context.config.api.url);
  const token = context.config.auth.onTokenRead();

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const payload = {
    description: params.description,
    date_finish: params.dateFinish,
    is_blind: params.isBlind,
    options: params.options
  };

  // Use axios to send a PUT request
  const { data } = await context.client.put(url.href, payload, authHeaders(token)).catch((error) => {
    if (error.response) {
      error.response.data.error = error.response.status;
      return error.response;
    }
  });
  // Return data from the API
  return data;
}

