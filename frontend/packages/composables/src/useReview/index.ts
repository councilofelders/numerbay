import {
  Context, Logger
} from '@vue-storefront/core';
import { useReviewFactory, UseReviewFactoryParams } from '../factories/useReviewFactory';
import { Review } from '../types';

const params: UseReviewFactoryParams<any, any, any, any, any> = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  searchReviews: async (context: Context, params) => {
    Logger.debug('getReviews');
    return await context.$numerbay.api.getReview(params);
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  addReview: async (context: Context, params) => {
    Logger.debug('addReview');
    const response = await context.$numerbay.api.createReview(params);
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  loadReviewMetadata: async (context: Context) => {
    Logger.debug('loadReviewMetadata');

    const { data } = await context.$numerbay.api.productReviewRatingsMetadata();

    return data.productReviewRatingsMetadata.items;
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  loadCustomerReviews: async (
    context: Context,
    params
  ) => {
    Logger.debug('loadCustomerReviews');

    const { data } = await context.$numerbay.api.customerProductReview(params);

    return data.customer;
  }
};

export default useReviewFactory<Review, any, any, any, any>(params);
