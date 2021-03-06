import { CustomQuery } from '@vue-storefront/core';
import { authHeaders } from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function createCoupon(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL(`coupons/${params.username}`, context.config.api.url);
  const token = context.config.auth.onTokenRead();

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const payload = {
    coupon_in: {
      applicability: params.applicability,
      code: params.code,
      // eslint-disable-next-line camelcase
      date_expiration: params.date_expiration,
      // eslint-disable-next-line camelcase
      applicable_product_ids: params.applicable_product_ids,
      // eslint-disable-next-line camelcase
      discount_percent: Number(params.discount_percent),
      // eslint-disable-next-line camelcase
      quantity_total: Number(params.quantity_total),
      // eslint-disable-next-line camelcase
      max_discount: Number(params.max_discount),
      // eslint-disable-next-line camelcase
      min_spend: Number(params.min_spend),
    },
    message: params.message
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

