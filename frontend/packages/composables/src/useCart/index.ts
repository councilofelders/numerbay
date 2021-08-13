/* istanbul ignore file */

import {
  Context, Logger,
  useCartFactory,
  UseCartFactoryParams
} from '@vue-storefront/core';
import { Cart, CartItem, Coupon, Product } from '../types';

const params: UseCartFactoryParams<Cart, CartItem, Product, Coupon> = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  load: async (context: Context, { customQuery }) => {
    Logger.debug('Mocked: loadCart');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  addItem: async (context: Context, { currentCart, product, quantity, customQuery }) => {
    Logger.debug('Mocked: addToCart');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  removeItem: async (context: Context, { currentCart, product, customQuery }) => {
    Logger.debug('Mocked: removeFromCart');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  updateItemQty: async (context: Context, { currentCart, product, quantity, customQuery }) => {
    Logger.debug('Mocked: updateQuantity');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  clear: async (context: Context, { currentCart }) => {
    Logger.debug('Mocked: clearCart');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  applyCoupon: async (context: Context, { currentCart, couponCode, customQuery }) => {
    Logger.debug('Mocked: applyCoupon');
    return {updatedCart: {}, updatedCoupon: {}};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  removeCoupon: async (context: Context, { currentCart, coupon, customQuery }) => {
    Logger.debug('Mocked: removeCoupon');
    return {updatedCart: {}};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  isInCart: (context: Context, { currentCart, product }) => {
    Logger.debug('Mocked: isInCart');
    return false;
  }
};

export default useCartFactory<Cart, CartItem, Product, Coupon>(params);
