/* istanbul ignore file */

import { Order, OrderItem, UserOrderGetters } from '../types';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getDate = (order: any): string => order?.date_order ? order?.date_order.slice(0, 10).replace(/-/g, '/').replace('T', ' ') : '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getId = (order: any): string => order?.id || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getStatus = (order: any): string => order?.state || 'unknown';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getPrice = (order: any): number | null => order?.price || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getCurrency = (order: any): string | null => order?.currency || 'NMR';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getFromAddress = (order: any): string | null => order?.from_address || null;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getToAddress = (order: any): string | null => order?.to_address || null;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getTransactionHash = (order: any): string | null => order?.transaction_hash || null;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProduct = (order: any): any => order?.product || null;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItems = (order: any): any[] => order?.items || [];

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItemSku = (item: any): string => item?.sku || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItemName = (item: any): string => item?.name || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItemQty = (item: any): number => item?.qty || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItemPrice = (item: any): number => item?.price?.current || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getFormattedPrice = (item: any): string => {
  const price = (item?.price || 0).toFixed(2);
  const currency = item?.currency || 'USD';
  if (currency === 'USD') return `$${price}`;
  return `${price} ${currency}`;
};

const orderGetters: UserOrderGetters<Order, OrderItem> = {
  getDate,
  getId,
  getStatus,
  getPrice,
  getCurrency,
  getFromAddress,
  getToAddress,
  getTransactionHash,
  getProduct,
  getItems,
  getItemSku,
  getItemName,
  getItemQty,
  getItemPrice,
  getFormattedPrice
};

export default orderGetters;
