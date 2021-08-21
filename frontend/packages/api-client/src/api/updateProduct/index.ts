import { CustomQuery } from '@vue-storefront/core';
import { authHeaders } from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function updateProduct(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL(`products/${params.id}`, context.config.api.url);
  const token = context.config.auth.onTokenRead();

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const payload = {
    // eslint-disable-next-line camelcase
    is_on_platform: params.isOnPlatform,
    price: Number(params.price),
    currency: params.currency,
    // eslint-disable-next-line camelcase
    category_id: Number(params.category),
    avatar: params.avatar,
    // eslint-disable-next-line camelcase
    third_party_url: params.thirdPartyUrl,
    // eslint-disable-next-line camelcase
    is_active: params.isActive,
    // eslint-disable-next-line camelcase
    expiration_round: params.expirationRound,
    description: params.description
  };

  // Use axios to send a PUT request
  const { data } = await context.client.put(url.href, payload, authHeaders(token));
  // Return data from the API
  return data;
}

