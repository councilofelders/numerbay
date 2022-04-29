/* istanbul ignore file */

import { Order, OrderItem, UserOrderGetters } from '../types';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getDate = (order: any): string => order?.date_order ? order?.date_order.slice(0, 10).replace(/-/g, '/').replace('T', ' ') : '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getId = (order: any): string => order?.id || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getStatus = (order: any): string => order?.state || 'unknown';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getSubmissionStatus = (order: any): string => order?.submit_state || '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getStakeLimit = (order: any): string => order?.stake_limit ? `${order.stake_limit} NMR` : '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getRound = (order: any): string => String(order?.round_order) || '-';

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
export const getSubmitModelName = (order: any): any => order?.submit_model_name || '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getMode = (order: any): any => order?.mode || null;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItems = (order: any): any[] => order?.items || [];

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItemSku = (item: any): string => item?.sku || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItemName = (item: any): string => item?.name || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItemQty = (item: any): number => item?.quantity || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItemPrice = (item: any): number => item?.price?.current || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getBuyer = (item: any): string => item?.buyer?.username || '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getFormattedPrice = (item: any, withCurrency = true, decimals = 2): string => {
  const price = Number(item?.price || 0).toFixed(decimals);
  if (withCurrency) {
    const currency = item?.currency || 'USD';
    if (currency === 'USD') return `$${price}`;
    return `${price} ${currency}`;
  }
  return `${price}`;
};

const orderGetters: UserOrderGetters<Order, OrderItem> = {
  getDate,
  getId,
  getStatus,
  getSubmissionStatus,
  getStakeLimit,
  getRound,
  getPrice,
  getCurrency,
  getFromAddress,
  getToAddress,
  getTransactionHash,
  getProduct,
  getSubmitModelName,
  getMode,
  getItems,
  getItemSku,
  getItemName,
  getItemQty,
  getItemPrice,
  getFormattedPrice,
  getBuyer
};

export default orderGetters;
