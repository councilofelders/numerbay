export type Cart = Record<string, unknown>;
export type Wishlist = Record<string, unknown>;
export type ProductVariant = {
  id: number;
  description: string;
  name: string;
  category: number;
  sku: string;
  avatar: string;
  // todo consistent camelcase
  // eslint-disable-next-line camelcase
  third_party_url: string;
  images: string[];
  price: number;
  owner: any;
};
export type Category = {
  id: number;
  name: string;
  slug: string;
  parent: Category;
  items: Category[];
};
export type CategoryFilter = Record<string, unknown>;
export type ShippingMethod = Record<string, unknown>;
export type LineItem = Record<string, unknown>;
