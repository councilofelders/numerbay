/* istanbul ignore file */
import {Context, Logger, useWishlistFactory, UseWishlistFactoryParams} from '@vue-storefront/core';
import {ref, Ref} from '@vue/composition-api';
import {Product, Wishlist, WishlistProduct} from '../types';

export const wishlist: Ref<Wishlist> = ref(null);

const params: UseWishlistFactoryParams<Wishlist, WishlistProduct, Product> = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  load: async (context: Context) => {
    Logger.debug('loadWishlist');
    return await context.$numerbay.api.getFavorite();
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  addItem: async (context: Context, { currentWishlist, product }) => {
    Logger.debug('addToWishlist');
    await context.$numerbay.api.createFavorite({ productId: product.id });
    return await context.$numerbay.api.getFavorite();
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  removeItem: async (context: Context, { currentWishlist, product }) => {
    Logger.debug('removeFromWishlist');
    await context.$numerbay.api.deleteFavorite({ productId: product.id });
    return await context.$numerbay.api.getFavorite();
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  clear: async (context: Context, { currentWishlist }) => {
    Logger.debug('Mocked: clearWishlist');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  isInWishlist: (context: Context, { currentWishlist, product }) => {
    Logger.debug('isInWishlist');
    // return currentWishlist?.wishlistItems.some(
    //   (item) => item.product.id == product.firstVariant
    // );
    return false;
  }
};

export default useWishlistFactory<Wishlist, WishlistProduct, Product>(params);
