import {
  ComputedProperty,
  CustomQuery,
  UseUserLoginParams,
  UseUserRegisterParams,
  ComposableFunctionArgs
} from '@vue-storefront/core';
import {Ref} from '@vue/composition-api';

export interface UseWeb3User {
  nonce: string,
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

export interface UseUserErrors {
    updateUser: Error;
    register: Error;
    login: Error;
    web3: Error;
    logout: Error;
    changePassword: Error;
    load: Error;
}

export interface UseUser<USER, UPDATE_USER_PARAMS> {
  user: ComputedProperty<USER>;
  web3User: ComputedProperty<UseWeb3User>;
  setUser: (user: USER) => void;
  updateUser: (params: { user: UPDATE_USER_PARAMS; customQuery?: CustomQuery }) => Promise<void>;
  register: (params: { user: UseUserRegisterParams; customQuery?: CustomQuery }) => Promise<void>;
  login: (params: { user: UseUserLoginParams; customQuery?: CustomQuery }) => Promise<void>;
  loginWeb3: (params: { user: { publicAddress: string, signature: string }; customQuery?: CustomQuery }) => Promise<void>;
  logout: (params?: {customQuery: CustomQuery}) => Promise<void>;
  getNonce: (params?: {publicAddress: string, customQuery: CustomQuery}) => Promise<void>;
  getNonceAuthenticated: (params?: {customQuery: CustomQuery}) => Promise<void>;
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

export interface UseProductErrors {
    search: Error;
    listingModal: Error;
}

export interface UseProduct<PRODUCTS, PRODUCT_SEARCH_PARAMS> {
  products: ComputedProperty<PRODUCTS>;
  loading: ComputedProperty<boolean>;
  error: ComputedProperty<UseProductErrors>;
  search(params: ComposableFunctionArgs<PRODUCT_SEARCH_PARAMS>): Promise<void>;
  createProduct(params: { product: any }): Promise<void>;
  updateProduct(params: { id: number, product: any }): Promise<void>;
  deleteProduct(params: { id: number }): Promise<void>;
  [x: string]: any;
}

export interface UseNumerai {
  getModels: (identifier: string) => Promise<void>;
  getModelInfo: (params: any) => Promise<void>;
  loading: ComputedProperty<boolean>;
  numerai: ComputedProperty<any>;
}
