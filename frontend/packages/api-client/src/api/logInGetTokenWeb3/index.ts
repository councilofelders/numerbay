import { CustomQuery } from '@vue-storefront/core';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function logInGetTokenWeb3(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('login/access-token-web3', context.config.api.url);

  const payload = {
    // eslint-disable-next-line camelcase
    public_address: params.publicAddress,
    signature: params.signature
  };

  // Use axios to send a POST request
  const { data } = await context.client.post(url.href, payload);

  await context.config.auth.onTokenChange(data.access_token);
  // Return data from the API
  return data;
}

