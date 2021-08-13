import {
  ComputedProperty,
  CustomQuery,
  UseUserErrors,
  UseUserLoginParams,
  UseUserRegisterParams,
  UseProductErrors,
  ComposableFunctionArgs
} from '@vue-storefront/core';
import {Ref} from '@vue/composition-api';

export interface UseWeb3User {
  activeAccount: any,
  activeBalance: number,
  chainId: any,
  chainName: any,
  // eslint-disable-next-line line-comment-position
  providerEthers: any, // this is "provider" for Ethers.js
  isConnected: boolean,
  // eslint-disable-next-line line-comment-position
  providerW3m: any, // this is "provider" from Web3Modal
  web3Modal: any
}

export interface UseUser<USER, UPDATE_USER_PARAMS> {
  user: ComputedProperty<USER>;
  web3User: ComputedProperty<UseWeb3User>;
  setUser: (user: USER) => void;
  updateUser: (params: { user: UPDATE_USER_PARAMS; customQuery?: CustomQuery }) => Promise<void>;
  register: (params: { user: UseUserRegisterParams; customQuery?: CustomQuery }) => Promise<void>;
  login: (params: { user: UseUserLoginParams; customQuery?: CustomQuery }) => Promise<void>;
  logout: (params?: {customQuery: CustomQuery}) => Promise<void>;
  initWeb3Modal: (params?: {customQuery: CustomQuery}) => Promise<void>;
  ethereumListener: (params?: {customQuery: CustomQuery}) => Promise<void>;
  connectWeb3Modal: (params?: {customQuery: CustomQuery}) => Promise<void>;
  disconnectWeb3Modal: (params?: {customQuery: CustomQuery}) => Promise<void>;
  changePassword: (params: { current: string; new: string, customQuery?: CustomQuery }) => Promise<void>;
  load: (params?: {customQuery: CustomQuery}) => Promise<void>;
  isAuthenticated: Ref<boolean>;
  loading: ComputedProperty<boolean>;
  error: ComputedProperty<UseUserErrors>;
}

export interface UseProduct<PRODUCTS, PRODUCT_SEARCH_PARAMS> {
  products: ComputedProperty<PRODUCTS>;
  loading: ComputedProperty<boolean>;
  error: ComputedProperty<UseProductErrors>;
  search(params: ComposableFunctionArgs<PRODUCT_SEARCH_PARAMS>): Promise<void>;
  [x: string]: any;
}

export interface UseNumerai {
  getModels: (identifier: string) => Promise<void>;
  getModelInfo: (params: any) => Promise<void>;
  loading: ComputedProperty<boolean>;
  numerai: ComputedProperty<any>;
}
