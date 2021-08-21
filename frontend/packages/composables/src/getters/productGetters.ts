import {
  AgnosticMediaGalleryItem,
  AgnosticAttribute,
  AgnosticPrice
} from '@vue-storefront/core';
import { ProductVariant } from '@vue-storefront/numerbay-api/src/types';
import { ProductGetters } from '../types';

type ProductVariantFilters = any

// TODO: Add interfaces for some of the methods in core
// Product

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductName = (product: ProductVariant): string => product?.name || 'Product\'s name';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductSlug = (product: ProductVariant): string => product.sku;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductPrice = (product: ProductVariant): AgnosticPrice => {
  return {
    regular: product?.price || 0
  };
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductGallery = (product: ProductVariant): AgnosticMediaGalleryItem[] => [
  {
    small: 'https://numerai-public-images.s3.amazonaws.com/profile_images/weekend-Qzl7KmFRcrH6.jpg',
    normal: 'https://numerai-public-images.s3.amazonaws.com/profile_images/weekend-Qzl7KmFRcrH6.jpg',
    big: 'https://numerai-public-images.s3.amazonaws.com/profile_images/weekend-Qzl7KmFRcrH6.jpg'
  },
  {
    small: 'https://numerai-public-images.s3.amazonaws.com/profile_images/weekend-Qzl7KmFRcrH6.jpg',
    normal: 'https://numerai-public-images.s3.amazonaws.com/profile_images/weekend-Qzl7KmFRcrH6.jpg',
    big: 'https://numerai-public-images.s3.amazonaws.com/profile_images/weekend-Qzl7KmFRcrH6.jpg'
  }
];

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductCoverImage = (product: ProductVariant): string => product?.avatar || 'https://numerai-public-images.s3.amazonaws.com/profile_images/weekend-Qzl7KmFRcrH6.jpg';

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

export const getFormattedPrice = (product: ProductVariant): string => {
  const price = (product?.price || 0).toFixed(2);
  const currency = product?.currency || 'USD';
  if (currency === 'USD') return `$${price}`;
  return `${price} ${currency}`;
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductTotalReviews = (product: ProductVariant): number => 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductAverageRating = (product: ProductVariant): number => 0;

export const getProductModelNmrStaked = (product: ProductVariant, decimals = 2): any => (product as any)?.model?.nmr_staked?.toFixed(decimals) || '-';

export const getProductModelRep = (product: ProductVariant, key: string, decimals = 4): any => ((product as any)?.model?.latest_reps || {})[key]?.toFixed(decimals) || '-';

export const getProductModelReturn = (product: ProductVariant, key: string, decimals = 2): any => ((product as any)?.model?.latest_returns || {})[key]?.toFixed(decimals) || '-';

export const getProductIsActive = (product: ProductVariant): boolean => (product as any)?.is_active;

export const getProductExpirationRound = (product: ProductVariant): number => (product as any)?.expiration_round || null;

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
  getTotalReviews: getProductTotalReviews,
  getAverageRating: getProductAverageRating,
  getModelNmrStaked: getProductModelNmrStaked,
  getModelRep: getProductModelRep,
  getModelReturn: getProductModelReturn,
  getIsActive: getProductIsActive,
  getExpirationRound: getProductExpirationRound
};

export default productGetters;
