/* istanbul ignore file */

import { Artifact, ProductArtifactGetters } from '../types';

function humanFileSize(bytes, si = false, dp = 1) {
  const thresh = si ? 1000 : 1024;

  if (Math.abs(bytes) < thresh) {
    return bytes + ' B';
  }

  const units = si
    ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
  let u = -1;
  const r = 10 ** dp;

  do {
    bytes /= thresh;
    ++u;
  } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);

  return bytes.toFixed(dp) + ' ' + units[u];
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getDate = (artifact: any): string => artifact?.date_artifact ? artifact?.date_artifact.slice(0, 10).replace(/-/g, '/').replace('T', ' ') : '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getId = (artifact: any): string => artifact?.id || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getObjectName = (artifact: any): string => artifact?.object_name || artifact?.url || 'unknown';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getObjectSize = (artifact: any): string => artifact?.object_size ? humanFileSize(artifact?.object_size) : '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getPrice = (artifact: any): number | null => artifact?.price || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getCurrency = (artifact: any): string | null => artifact?.currency || 'NMR';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getFromAddress = (artifact: any): string | null => artifact?.from_address || null;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getToAddress = (artifact: any): string | null => artifact?.to_address || null;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getTransactionHash = (artifact: any): string | null => artifact?.transaction_hash || null;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProduct = (artifact: any): any => artifact?.product || null;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItems = (artifact: any): any[] => artifact?.items || [];

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItemSku = (item: any): string => item?.sku || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItemName = (item: any): string => item?.name || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItemQty = (item: any): number => item?.qty || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItemPrice = (item: any): number => item?.price?.current || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getBuyer = (item: any): string => item?.buyer?.username || '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getFormattedPrice = (item: any, withCurrency = true, decimals = 2): string => {
  const price = (item?.price || 0).toFixed(decimals);
  if (withCurrency) {
    const currency = item?.currency || 'USD';
    if (currency === 'USD') return `$${price}`;
    return `${price} ${currency}`;
  }
  return `${price}`;
};

const artifactGetters: ProductArtifactGetters<Artifact> = {
  getDate,
  getId,
  getObjectName,
  getObjectSize,
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
  getFormattedPrice,
  getBuyer
};

export default artifactGetters;
