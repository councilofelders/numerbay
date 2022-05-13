import {Context, Logger} from '@vue-storefront/core';
import { useCouponFactory, UseCouponFactoryParams } from '../factories/useCouponFactory';

const params: UseCouponFactoryParams<any, any> = {
  createCoupon: async (context: Context, {coupon}) => {
    Logger.debug('createCoupon');
    const response = await context.$numerbay.api.createCoupon(coupon);
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  deleteCoupon: async (context: Context, {id}) => {
    Logger.debug('deleteCoupon');
    const response = await context.$numerbay.api.deleteCoupon({id});
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  }
};

export default useCouponFactory<any, any>(params);
