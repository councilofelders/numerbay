/* istanbul ignore file */

import { User, UserGetters } from '../types';

export const getId = (user: User): number => user?.id || null;

export const getUsername = (user: User): string => user?.username || '';

export const getUserEmailAddress = (user: User): string => user?.email || '';

export const getDefaultReceivingWalletAddress = (user: User): string => user?.default_receiving_wallet_address || '';

export const getUserSocialDiscord = (user: User): string => user?.social_discord || '';

export const getUserSocialLinkedIn = (user: User): string => user?.social_linkedin || '';

export const getUserSocialTwitter = (user: User): string => user?.social_twitter || '';

export const getUserSocialWebsite = (user: User): string => user?.social_website || '';

export const getPublicAddress = (user: User): string => user?.public_address || '';

export const getNumeraiApiKeyPublicId = (user: User): string => user?.numerai_api_key_public_id || null;

export const getNumeraiLastSyncDate = (user: User): string => user?.date_last_numerai_sync ? user?.date_last_numerai_sync.slice(0, 19).replace(/-/g, '/').replace('T', ' ') : '-';

export const getNonce = (user: User): string => user?.nonce || '';

export const getPublicKey = (user: User): string => user?.public_key || null;

export const getPublicKeyV2 = (user: User): string => user?.public_key_v2 || null;

export const getModels = (user: User, tournament: number = null, sortDate = true): any[] => {
  let models = user?.models;
  if (tournament) {
    models = models?.filter((m)=>m.tournament === tournament);
  }
  if (sortDate) {
    models = models?.sort((a, b) => a?.start_date?.localeCompare(b?.start_date));
  }
  return models || [];
};

const userGetters: UserGetters<User> = {
  getId: getId,
  getUsername: getUsername,
  getEmailAddress: getUserEmailAddress,
  getDefaultReceivingWalletAddress: getDefaultReceivingWalletAddress,
  getSocialDiscord: getUserSocialDiscord,
  getSocialLinkedIn: getUserSocialLinkedIn,
  getSocialTwitter: getUserSocialTwitter,
  getSocialWebsite: getUserSocialWebsite,
  getPublicAddress: getPublicAddress,
  getNumeraiApiKeyPublicId: getNumeraiApiKeyPublicId,
  getNumeraiLastSyncDate: getNumeraiLastSyncDate,
  getNonce: getNonce,
  getPublicKey: getPublicKey,
  getPublicKeyV2: getPublicKeyV2,
  getModels: getModels
};

export default userGetters;
