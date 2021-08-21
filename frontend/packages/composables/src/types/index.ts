import {ProductVariant} from '@vue-storefront/numerbay-api';
import {
  AgnosticAttribute,
  AgnosticBreadcrumb,
  AgnosticMediaGalleryItem,
  AgnosticPrice,
  FacetSearchResult
} from '@vue-storefront/core';

export { UseCategory, UseProduct, UseUserFactoryParams } from '@vue-storefront/core';

export type Address = Record<string, unknown>;

export type Category = Record<string, unknown>;

export type User = {
  id?: number;
  username?: string;
  email?: string;
    // eslint-disable-next-line camelcase
  public_address?: string;
    // eslint-disable-next-line camelcase
  numerai_api_key_public_id?: string;
  nonce?: string;
  models?: any[]
};

export type UserAddress = Record<string, unknown>;

export type Cart = Record<string, unknown>;

export type CartItem = Record<string, unknown>;

export type Coupon = Record<string, unknown>;

export type Order = Record<string, unknown>;

export type OrderItem = Record<string, unknown>;

export type Product = Record<string, unknown>;

export type Review = Record<string, unknown>;

export type Shipping = Record<string, unknown>;

export type ShippingMethod = Record<string, unknown>;

export type WishlistProduct = Record<string, unknown>;

export type Wishlist = Record<string, unknown>;

export type ProductsResponse = {
  data: Product[];
  total: number;
};

export type OrderSearchParams = Record<string, any>;

export type OrdersResponse = {
  data: any[];
  total: number;
};

export enum AttributeType {
  STRING = 'StringAttribute',
  DATE = 'DateAttribute',
  DATETIME = 'DateTimeAttribute',
  TIME = 'TimeAttribute',
  NUMBER = 'NumberAttribute',
  ENUM = 'EnumAttribute',
  MONEY = 'MoneyAttribute',
  BOOLEAN = 'BooleanAttribute'
}

export type Attribute = {
  typename?: string;
  name: string;
  value?: any;
};

export interface FilterOption {
  label: string;
  value: string | number | boolean | [number, number] | [string, string];
  selected: boolean;
}

export interface Filter {
  type: AttributeType;
  name: string;
  value: any;
}

export interface FacetResultsData {
  products: ProductVariant[];
  categories: Category[];
  facets: Record<string, Filter>;
  availableFilters: Record<string, any>;
  total: number;
  perPageOptions: number[];
  itemsPerPage: number;
}

export type SearchData = FacetSearchResult<FacetResultsData>

// _______________ Getters _______________

export interface UserGetters<USER> {
    getId: (customer: USER) => number;
    getUsername: (customer: USER) => string;
    getEmailAddress: (customer: USER) => string;
    getPublicAddress: (customer: USER) => string;
    getNumeraiApiKeyPublicId: (customer: USER) => string;
    getNonce: (customer: USER) => string;
    getModels: (customer: USER, tournament: number, sortDate: boolean) => any[];
    [getterName: string]: (element: any, options?: any) => unknown;
}

export interface ProductGetters<PRODUCT, PRODUCT_FILTER> {
  getName: (product: PRODUCT) => string;
  getSlug: (product: PRODUCT) => string;
  getPrice: (product: PRODUCT) => AgnosticPrice;
  getGallery: (product: PRODUCT) => AgnosticMediaGalleryItem[];
  getCoverImage: (product: PRODUCT) => string;
  getFiltered: (products: PRODUCT[], filters?: PRODUCT_FILTER) => PRODUCT[];
  getAttributes: (products: PRODUCT[] | PRODUCT, filters?: Array<string>) => Record<string, AgnosticAttribute | string>;
  getDescription: (product: PRODUCT) => string;
  getCategoryIds: (product: PRODUCT) => string[];
  getId: (product: PRODUCT) => string;
  getFormattedPrice: (product: PRODUCT) => string;
  getTotalReviews: (product: PRODUCT) => number;
  getAverageRating: (product: PRODUCT) => number;
  getBreadcrumbs?: (product: PRODUCT) => AgnosticBreadcrumb[];
  [getterName: string]: any;
}

export interface UserOrderGetters<ORDER, ORDER_ITEM> {
    getDate: (order: ORDER) => string;
    getId: (order: ORDER) => string;
    getStatus: (order: ORDER) => string;
    getPrice: (order: ORDER) => number;
    getCurrency: (order: ORDER) => string;
    getFromAddress: (order: ORDER) => string;
    getToAddress: (order: ORDER) => string;
    getTransactionHash: (order: ORDER) => string;
    getProduct: (order: ORDER) => any;
    getItems: (order: ORDER) => ORDER_ITEM[];
    getItemSku: (item: ORDER_ITEM) => string;
    getItemName: (item: ORDER_ITEM) => string;
    getItemQty: (item: ORDER_ITEM) => number;
    getItemPrice: (item: ORDER_ITEM) => number;
    getFormattedPrice: (item: ORDER_ITEM) => string;
    [getterName: string]: (element: any, options?: any) => unknown;
}
