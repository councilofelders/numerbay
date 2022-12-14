import { CustomQuery } from '@vue-storefront/core';
import { authHeaders } from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function updateProduct(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL(`products/${params.id}`, context.config.api.url);
  const token = context.config.auth.onTokenRead();

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const payload = {
    avatar: params.avatar ? params.avatar : null,
    // eslint-disable-next-line camelcase
    is_active: params.isActive,
    // eslint-disable-next-line camelcase
    is_daily: params.isDaily,
    // eslint-disable-next-line camelcase
    use_encryption: params.useEncryption,
    webhook: params.webhook ? params.webhook : null,
    // eslint-disable-next-line camelcase
    expiration_round: params.expirationRound,
    description: params.description,
    options: params.options,
    // eslint-disable-next-line camelcase
    featured_products: params.featuredProducts ? params.featuredProducts.map(p => p.id) : null
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

