import {
  Context, Logger
} from '@vue-storefront/core';
import { useReviewFactory, UseReviewFactoryParams } from '../factories/useReviewFactory';
import { Review } from '../types';

const params: UseReviewFactoryParams<any, any, any, any, any> = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  searchReviews: async (context: Context, params) => {
    Logger.debug('Mocked: searchReviews');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  addReview: async (context: Context, params) => {
    Logger.debug('Mocked: addReview');
    return {};
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
