import {
  WishlistGetters,
  AgnosticTotals
} from '@vue-storefront/core';
import { Wishlist, WishlistProduct } from '../types';
import productGetters from './productGetters';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getWishlistItems = (wishlist: Wishlist): any => wishlist;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getWishlistItemName = (product: any): string => productGetters.getName(product);

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getWishlistItemImage = (product: any): string => productGetters.getCoverImage(product);

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getWishlistItemPrice = (product: any): any => productGetters.getFormattedPrice(product, true, 0, 4);

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getWishlistItemQty = (product: WishlistProduct): number => 1;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getWishlistItemAttributes = (product: WishlistProduct, filterByAttributeName?: string[]) => ({});

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getWishlistItemSku = (product: any): string => productGetters.getSlug(product);

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getWishlistTotals = (wishlist: Wishlist): AgnosticTotals => {
  return {
    total: 10,
    subtotal: 10
  };
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getWishlistShippingPrice = (wishlist: Wishlist): number => 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getWishlistTotalItems = (wishlist: Wishlist): number => <number>wishlist?.length || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getFormattedPrice = (price: number): string => String(price);

const wishlistGetters: WishlistGetters<Wishlist, WishlistProduct> = {
  getTotals: getWishlistTotals,
  getShippingPrice: getWishlistShippingPrice,
  getItems: getWishlistItems,
  getItemName: getWishlistItemName,
  getItemImage: getWishlistItemImage,
  getItemPrice: getWishlistItemPrice,
  getItemQty: getWishlistItemQty,
  getItemAttributes: getWishlistItemAttributes,
  getItemSku: getWishlistItemSku,
  getTotalItems: getWishlistTotalItems,
  getFormattedPrice
};

export default wishlistGetters;
