import {
  AgnosticMediaGalleryItem,
  AgnosticAttribute,
  AgnosticPrice
} from '@vue-storefront/core';
import { ProductVariant } from '@vue-storefront/numerbay-api/src/types';
import { ProductGetters } from '../types';
import { getReviewRating } from './reviewGetters';

type ProductVariantFilters = any

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductName = (product: ProductVariant): string => product?.name || '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductSlug = (product: ProductVariant): string => product?.sku || '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductPrice = (product: ProductVariant): AgnosticPrice => {
  return {
    regular: product?.price || 0
  };
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductGallery = (product: ProductVariant): AgnosticMediaGalleryItem[] => [
  {
    small: 'https://numer.ai/img/profile_picture_light.jpg',
    normal: 'https://numer.ai/img/profile_picture_light.jpg',
    big: 'https://numer.ai/img/profile_picture_light.jpg'
  },
  {
    small: 'https://numer.ai/img/profile_picture_light.jpg',
    normal: 'https://numer.ai/img/profile_picture_light.jpg',
    big: 'https://numer.ai/img/profile_picture_light.jpg'
  }
];

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductCoverImage = (product: ProductVariant): string => product?.avatar || 'https://numer.ai/img/profile_picture_light.jpg';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductFiltered = (products: ProductVariant[], filters: ProductVariantFilters | any = {}): ProductVariant[] => {
  // todo filter products by attributes
  return products;
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductAttributes = (products: ProductVariant[] | ProductVariant, filterByAttributeName?: string[]): Record<string, AgnosticAttribute | string> => {
  return {};
};

export const getProductDescription = (product: ProductVariant): any => (product as any)?.description || '';

export const getProductCategoryIds = (product: ProductVariant): string[] => (product as any)?.category ? [(product as any)?.category.id.toString()] : [];

export const getProductId = (product: ProductVariant): string => (product as any)?.id || '';

export const getFormattedPrice = (product: ProductVariant, withCurrency = true, decimals = 2): string => {
  const price = (product?.price || 0).toFixed(decimals);
  if (withCurrency) {
    const currency = product?.currency || 'USD';
    if (currency === 'USD') return `$${price}`;
    return `${price} ${currency}`;
  }
  return `${price}`;
};

export const getProductMode = (product: ProductVariant): string => (product as any)?.mode;

export const getProductStakeLimit = (product: ProductVariant): string => (product as any)?.stake_limit ? `${(product as any)?.stake_limit} NMR` : '-';

export const getProductTournamentId = (product: ProductVariant): number => {
  const slug = (product as any)?.category?.slug;
  if (slug) {
    if (slug.startsWith('signals-')) {
      return 11;
    } else if (slug.startsWith('numerai-')) {
      return 8;
    }
  }
  return null;
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductTotalReviews = (product: ProductVariant): number => product?.reviews?.length || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductAverageRating = (product: ProductVariant): number => (product?.reviews?.reduce((
  acc, curr
) => Number.parseInt(`${acc}`, 10) + getReviewRating(curr), 0)) / (product?.reviews?.length || 1) || 0;

export const getProductModelNmrStaked = (product: ProductVariant, decimals = 2): any => (product as any)?.model?.nmr_staked?.toFixed(decimals) || '-';

export const getProductModelRank = (product: ProductVariant, key: string): any => ((product as any)?.model?.latest_ranks || {})[key] || '-';

export const getProductModelRep = (product: ProductVariant, key: string, decimals = 4): any => ((product as any)?.model?.latest_reps || {})[key]?.toFixed(decimals) || '-';

export const getProductModelReturn = (product: ProductVariant, key: string, decimals = 2): any => ((product as any)?.model?.latest_returns || {})[key]?.toFixed(decimals) || '-';

export const getProductIsActive = (product: ProductVariant): boolean => (product as any)?.is_active;

export const getProductExpirationRound = (product: ProductVariant): number => (product as any)?.expiration_round || null;

export const getProductOwner = (product: ProductVariant): string => (product as any)?.owner?.username || '-';

const productGetters: ProductGetters<ProductVariant, ProductVariantFilters> = {
  getName: getProductName,
  getSlug: getProductSlug,
  getPrice: getProductPrice,
  getGallery: getProductGallery,
  getCoverImage: getProductCoverImage,
  getFiltered: getProductFiltered,
  getAttributes: getProductAttributes,
  getDescription: getProductDescription,
  getCategoryIds: getProductCategoryIds,
  getId: getProductId,
  getFormattedPrice: getFormattedPrice,
  getMode: getProductMode,
  getStakeLimit: getProductStakeLimit,
  getTournamentId: getProductTournamentId,
  getTotalReviews: getProductTotalReviews,
  getAverageRating: getProductAverageRating,
  getModelNmrStaked: getProductModelNmrStaked,
  getModelRank: getProductModelRank,
  getModelRep: getProductModelRep,
  getModelReturn: getProductModelReturn,
  getIsActive: getProductIsActive,
  getExpirationRound: getProductExpirationRound,
  getOwner: getProductOwner
};

export default productGetters;
