import { CustomQuery } from '@vue-storefront/core';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function getNumeraiModelInfo(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL(`numerai/${params.tournament}/${params.modelName}`, context.config.api.url);

  // Use axios to send a GET request
  const { data } = await context.client.get(url.href);

  // Return data from the API
  return data;
}

