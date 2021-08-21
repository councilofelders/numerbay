import { CustomQuery } from '@vue-storefront/core';
import { authHeaders } from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function createOrder(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('orders/', context.config.api.url);
  const token = context.config.auth.onTokenRead();

  // price: Decimal
  //   currency: str
  //   chain: str
  //   from_address: str
  //   to_address: str
  //   product_id: int

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const payload = {
    id: Number(params.id)
  };

  // Use axios to send a POST request
  const { data } = await context.client.post(url.href, payload, authHeaders(token)).catch((error) => {
    if (error.response) {
      error.response.data.error = error.response.status;
      return error.response;
    }
  });
  // Return data from the API
  return data;
}

