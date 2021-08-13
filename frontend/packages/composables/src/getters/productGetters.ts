import {
  AgnosticMediaGalleryItem,
  AgnosticAttribute,
  AgnosticPrice,
  ProductGetters
} from '@vue-storefront/core';
import { ProductVariant } from '@vue-storefront/numerbay-api/src/types';

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

export const getFormattedPrice = (price: number) => String(price);

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductTotalReviews = (product: ProductVariant): number => 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductAverageRating = (product: ProductVariant): number => 0;

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
  getAverageRating: getProductAverageRating
};

export default productGetters;
