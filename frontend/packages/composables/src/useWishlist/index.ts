/* istanbul ignore file */
import {
  Context, Logger,
  useWishlistFactory,
  UseWishlistFactoryParams
} from '@vue-storefront/core';
import { ref, Ref } from '@vue/composition-api';
import { Wishlist, WishlistProduct, Product } from '../types';

export const wishlist: Ref<Wishlist> = ref(null);

const params: UseWishlistFactoryParams<Wishlist, WishlistProduct, Product> = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  load: async (context: Context) => {
    Logger.debug('Mocked: loadWishlist');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  addItem: async (context: Context, { currentWishlist, product }) => {
    Logger.debug('Mocked: addToWishlist');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  removeItem: async (context: Context, { currentWishlist, product }) => {
    Logger.debug('Mocked: removeFromWishlist');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  clear: async (context: Context, { currentWishlist }) => {
    Logger.debug('Mocked: clearWishlist');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  isInWishlist: (context: Context, { currentWishlist }) => {
    Logger.debug('Mocked: isInWishlist');
    return false;
  }
};

export default useWishlistFactory<Wishlist, WishlistProduct, Product>(params);
