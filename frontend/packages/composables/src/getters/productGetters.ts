import {
  AgnosticAttribute,
  AgnosticMediaGalleryItem,
  AgnosticPrice
} from '@vue-storefront/core';
import { ProductGetters } from '../types';
import { ProductVariant } from '@vue-storefront/numerbay-api/src/types';
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

export const getProductCategory = (product: ProductVariant): any => (product as any)?.category || {};

export const getProductId = (product: ProductVariant): string => (product as any)?.id || '';

export const getProductOptions = (product: ProductVariant): any[] => (product as any)?.options || [];

export const getProductOrderedOptions = (product: ProductVariant): any[] => (product as any)?.options ? (product as any)?.options.slice().sort((a, b) => parseFloat(a.id) - parseFloat(b.id)).map((o, i) => {
  o.index = i;
  return o;
}) : [];

export const getProductOptionById = (product: ProductVariant, optionId: number): any => {
  const options = (product as any)?.options?.filter((o)=>parseInt(o.id) === parseInt(String(optionId))) || [];
  return options[0] || {};
};

export const getProductOrderedOption = (product: ProductVariant, optionIdx = 0): any => {
  const orderedOptions = getProductOrderedOptions(product);
  return orderedOptions[parseInt(String(optionIdx))] || {};
};

export const getOptionUrl = (option: any): string => option?.third_party_url;

export const getOptionIsOnPlatform = (option: any): boolean => option?.is_on_platform;

export const getOptionPlatform = (option: any) => {
  if (typeof option?.is_on_platform === 'boolean' && option?.is_on_platform === false && option?.third_party_url) {
    const domain = (new URL(option?.third_party_url));
    const urlParts = domain.hostname.split('.').slice(0);
    const baseUrl = urlParts.slice(-(urlParts.length === 4 ? 3 : 2)).join('.');
    return baseUrl;
  }
  if (option?.is_on_platform) {
    return 'NumerBay';
  }
  return '-';
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const formatPrice = (price: any, currency: any, withCurrency = true): string => {
  if (withCurrency) {
    if (currency === 'USD') return `$${price}`;
    return `${price} ${currency}`;
  }
  return `${price}`;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const getOptionFormattedPrice = (option: any, withCurrency = true): string => {
  const decimals = option?.is_on_platform ? 4 : 2;
  const price = (option?.price || 0).toFixed(decimals);
  return formatPrice(price, option?.currency, withCurrency);
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const getOptionFormattedDescription = (option: any, category: any): string => {
  let sale_mode = null;
  if (option?.mode === 'file') {
    sale_mode = 'file'
  } else if (option?.mode === 'stake') {
    sale_mode = 'stake only'
  } else if (option?.mode === 'stake_with_limit') {
    sale_mode = `${option?.stake_limit} NMR`
  }

  const quantity = option?.quantity;
  let quantity_suffix = '';
  if (category?.is_per_round) {
    if (quantity == 1) {
      quantity_suffix = 'round ';
    } else if (quantity > 1) {
      quantity_suffix = 'rounds ';
    }
  }

  if (sale_mode) {
    return `For ${quantity} ${quantity_suffix}- ${sale_mode}`;
  } else {
    return `For ${quantity} ${quantity_suffix}`;
  }
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const getOptionFormattedSpecialPrice = (option: any, withCurrency = true): string => {
  const decimals = option?.is_on_platform ? 4 : 2;
  if (option?.special_price) {
    const price = (option?.special_price).toFixed(decimals);
    return formatPrice(price, option?.currency, withCurrency);
  }
  return null;
};

export const getFormattedOption = (option: any): string => {
  if (option.is_on_platform) {
    return `${option.quantity} x ${option.mode === 'stake_with_limit' ? 'up to ' + option.stake_limit.toFixed(0) + ' NMR stake' : option.mode} for ${getOptionFormattedPrice(option, true)}${option.description ? ' [' + option.description + ']' : ''}`;
  }
  return `${option.quantity} x ${getOptionPlatform(option)} for ${getOptionFormattedPrice(option, true)} ref price${option.description ? ' [' + option.description + ']' : ''}`;
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getFormattedPrice = (product: ProductVariant, withCurrency = true, optionIdx = 0, decimals = 2): string => {
  const options = getProductOrderedOptions(product);
  if (optionIdx >= options.length) {
    return '-';
  }
  const option = options[optionIdx];
  const isOnPlatform = option.is_on_platform;
  const price = (option?.price || 0).toFixed(isOnPlatform ? 4 : 2);
  if (withCurrency) {
    const currency = option?.currency || 'USD';
    if (currency === 'USD') return `$${price}`;
    return `${price} ${currency}`;
  }
  return `${price}`;
};

export const getProductMode = (product: ProductVariant): string => (product as any)?.mode || '-';

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

export const getProductWebhook = (product: ProductVariant): string => product?.webhook;

export const getProductModelNmrStaked = (product: ProductVariant, decimals = 2): any => (product as any)?.model?.nmr_staked?.toFixed(decimals) || '-';

export const getProductModelStakeInfo = (product: ProductVariant, key: string): any => ((product as any)?.model?.stake_info || {})[key];

export const getProductModelRank = (product: ProductVariant, key: string): any => ((product as any)?.model?.latest_ranks || {})[key] || '-';

export const getProductModelRep = (product: ProductVariant, key: string, decimals = 4): any => ((product as any)?.model?.latest_reps || {})[key]?.toFixed(decimals) || '-';

export const getProductModelReturn = (product: ProductVariant, key: string, decimals = 2): any => ((product as any)?.model?.latest_returns || {})[key]?.toFixed(decimals) || '-';

export const getProductIsActive = (product: ProductVariant): boolean => (product as any)?.is_active;

export const getProductIsDaily = (product: ProductVariant): boolean => (product as any)?.is_daily;

export const getProductUseEncryption = (product: ProductVariant): boolean => (product as any)?.use_encryption;

export const getProductIsOnPlatform = (product: ProductVariant): boolean => ((product as any)?.options || [])[0]?.is_on_platform;

export const getProductExpirationRound = (product: ProductVariant): number => (product as any)?.expiration_round || null;

export const getProductOwner = (product: ProductVariant): string => (product as any)?.owner?.username || '-';

export const getProductModelName = (product: ProductVariant): string => (product as any)?.model?.name || '-';

export const getProductModelUrl = (product: ProductVariant): string => {
  if ((product as any)?.category?.is_per_model) {
    const tournament = (product as any)?.category?.tournament;
    if (tournament === 8) {
      return `https://numer.ai/${(product as any)?.model?.name}`;
    } else if (tournament === 11) {
      return `https://signals.numer.ai/${(product as any)?.model?.name}`;
    }
  }
  return null;
};

export const getProductIsAvailable = (product: ProductVariant, optionIdx: number): boolean => {
  return getProductIsActive(product) && !(!getOptionUrl(getProductOrderedOption(product, optionIdx)) && !getOptionIsOnPlatform(getProductOrderedOption(product, optionIdx)));
};

export const getProductTotalSales = (product: ProductVariant): number => (product as any)?.total_num_sales || 0;

export const getProductQtySales = (product: ProductVariant): number => (product as any)?.total_qty_sales || 0;

export const getProductLastPrice = (product: ProductVariant): number => (product as any)?.last_sale_price || '-';

export const getProductLastPriceDelta = (product: ProductVariant): number => (product as any)?.last_sale_price_delta || '-';

export const getProductQtyDelivered = (product: ProductVariant): number => (product as any)?.total_qty_delivered || 0;

export const getProductOnTimeRating = (product: ProductVariant): string => {
  const total_qty_sales = (product as any)?.total_qty_sales || 0;
  if (total_qty_sales > 3) {
    const total_qty_delivered = (product as any)?.total_qty_delivered || 0;
    const delivery_rate = total_qty_delivered / total_qty_sales;
    if (delivery_rate >= 0.95) {
      return 'always';
    } else if (delivery_rate >= 0.75) {
      return 'good';
    } else if (delivery_rate >= 0.5) {
      return 'average';
    } else {
      return 'poor';
    }
  }
  return null;
};

const productGetters: ProductGetters<ProductVariant, ProductVariantFilters> = {
  getName: getProductName,
  getSlug: getProductSlug,
  getPrice: getProductPrice,
  getGallery: getProductGallery,
  getCoverImage: getProductCoverImage,
  getFiltered: getProductFiltered,
  getAttributes: getProductAttributes,
  getDescription: getProductDescription,
  getCategory: getProductCategory,
  getCategoryIds: getProductCategoryIds,
  getId: getProductId,
  getOptionById: getProductOptionById,
  getOrderedOption: getProductOrderedOption,
  getOptions: getProductOptions,
  getOrderedOptions: getProductOrderedOptions,
  getOptionUrl: getOptionUrl,
  getOptionIsOnPlatform: getOptionIsOnPlatform,
  getOptionPlatform: getOptionPlatform,
  getOptionFormattedPrice: getOptionFormattedPrice,
  getOptionFormattedDescription: getOptionFormattedDescription,
  getOptionFormattedSpecialPrice: getOptionFormattedSpecialPrice,
  getFormattedOption: getFormattedOption,
  getFormattedPrice: getFormattedPrice,
  getMode: getProductMode,
  getStakeLimit: getProductStakeLimit,
  getTournamentId: getProductTournamentId,
  getTotalReviews: getProductTotalReviews,
  getAverageRating: getProductAverageRating,
  getWebhook: getProductWebhook,
  getModelNmrStaked: getProductModelNmrStaked,
  getModelStakeInfo: getProductModelStakeInfo,
  getModelRank: getProductModelRank,
  getModelRep: getProductModelRep,
  getModelReturn: getProductModelReturn,
  getIsActive: getProductIsActive,
  getIsDaily: getProductIsDaily,
  getUseEncryption: getProductUseEncryption,
  getIsOnPlatform: getProductIsOnPlatform,
  getExpirationRound: getProductExpirationRound,
  getOwner: getProductOwner,
  getModelName: getProductModelName,
  getModelUrl: getProductModelUrl,
  getIsAvailable: getProductIsAvailable,
  getTotalSales: getProductTotalSales,
  getQtySales: getProductQtySales,
  getQtyDelivered: getProductQtyDelivered,
  getLastPrice: getProductLastPrice,
  getLastPriceDelta: getProductLastPriceDelta,
  getOnTimeRating: getProductOnTimeRating
};

export default productGetters;
