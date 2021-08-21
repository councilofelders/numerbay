import { CustomQuery } from '@vue-storefront/core';
import {authHeaders} from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function getNumeraiModels(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('numerai/', context.config.api.url);
  const token = context.config.auth.onTokenRead();

  // Use axios to send a GET request
  const { data } = await context.client.get(url.href, authHeaders(token)).catch((error) => {
    if (error.response) {
      error.response.data.error = error.response.status;
      return error.response;
    }
  });

  // Return data from the API
  return data;
}

