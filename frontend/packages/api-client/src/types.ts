export type Cart = Record<string, unknown>;
export type Wishlist = Record<string, unknown>;
export type ProductVariant = {
  id: number;
  description: string;
  name: string;
  category: number;
  sku: string;
  images: string[];
  // eslint-disable-next-line camelcase
  is_on_platform: boolean;
  price: number;
  currency: string;
  owner: any;
  model: any;
  avatar: string;
  // todo consistent camelcase
  // eslint-disable-next-line camelcase
  third_party_url: string;
  reviews: any[];
};
export type Category = {
  id: number;
  name: string;
  slug: string;
  parent: Category;
  items: Category[];
};
export type CategoryFilter = Record<string, unknown>;
export type Order = {
  id: number
  clientOrderRef?: string
  dateOrder?: Date
  roundOrder?: number
  product?: ProductVariant
  price?: number
  currency?: string
  chain?: string
  orderStatus?: string
}
export type ShippingMethod = Record<string, unknown>;
export type LineItem = Record<string, unknown>;
