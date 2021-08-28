/* istanbul ignore file */

import { User, UserGetters } from '../types';

export const getId = (user: User): number => user?.id || null;

export const getUsername = (user: User): string => user?.username || '';

export const getUserEmailAddress = (user: User): string => user?.email || '';

export const getPublicAddress = (user: User): string => user?.public_address || '';

export const getNumeraiApiKeyPublicId = (user: User): string => user?.numerai_api_key_public_id || '';

export const getNonce = (user: User): string => user?.nonce || '';

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
  getPublicAddress: getPublicAddress,
  getNumeraiApiKeyPublicId: getNumeraiApiKeyPublicId,
  getNonce: getNonce,
  getModels: getModels
};

export default userGetters;
