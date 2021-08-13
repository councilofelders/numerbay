/* istanbul ignore file */

import { User, UserGetters } from '../types';

export const getId = (user: User): number => user?.id || null;

export const getUsername = (user: User): string => user?.username || '';

export const getUserEmailAddress = (user: User): string => user?.email || '';

export const getPublicAddress = (user: User): string => user?.public_address || '';

export const getNumeraiApiKeyPublicId = (user: User): string => user?.numerai_api_key_public_id || '';

export const getNonce = (user: User): string => user?.nonce || '';

const userGetters: UserGetters<User> = {
  getId: getId,
  getUsername: getUsername,
  getEmailAddress: getUserEmailAddress,
  getPublicAddress: getPublicAddress,
  getNumeraiApiKeyPublicId: getNumeraiApiKeyPublicId,
  getNonce: getNonce
};

export default userGetters;
