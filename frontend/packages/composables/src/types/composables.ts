import {
  ComposableFunctionArgs,
  ComputedProperty,
  CustomQuery,
  UseUserLoginParams,
  UseUserRegisterParams
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
    syncUserNumerai: Error;
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
  syncUserNumerai: () => Promise<void>;
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
    salesLeaderboard: Error;
    listingModal: Error;
}

export interface UseProduct<PRODUCTS, PRODUCT_SEARCH_PARAMS> {
  products: ComputedProperty<PRODUCTS>;
  loading: ComputedProperty<boolean>;
  loadingWebhook: ComputedProperty<boolean>;
  error: ComputedProperty<UseProductErrors>;
  search(params: ComposableFunctionArgs<PRODUCT_SEARCH_PARAMS>): Promise<void>;
  getSalesLeaderboard(params: any): Promise<void>;
  createProduct(params: { product: any }): Promise<void>;
  updateProduct(params: { id: number, product: any }): Promise<void>;
  deleteProduct(params: { id: number }): Promise<void>;
  testProductWebhook(params: { url: string }): Promise<void>;
  [x: string]: any;
}

export interface UseNumeraiErrors {
    getModels: Error;
    getModelInfo: Error;
}

export interface UseNumerai {
  getModels: (identifier: string) => Promise<void>;
  getModelInfo: (params: any) => Promise<void>;
  loading: ComputedProperty<boolean>;
  numerai: ComputedProperty<any>;
  error: ComputedProperty<UseNumeraiErrors>;
}

export interface UseUserOrderErrors {
  search: Error;
  updateOrderSubmissionModel: Error;
  validatePayment: Error;
  cancelOrder: Error;
  sendUploadReminder: Error;
  sendRefundRequest: Error;
}

export interface UseUserOrder<ORDERS, ORDER_SEARCH_PARAMS> {
  orders: ComputedProperty<ORDERS>;
  search(params: ComposableFunctionArgs<ORDER_SEARCH_PARAMS>): Promise<void>;
  updateOrderSubmissionModel(params: { orderId: number, modelId: string }): Promise<void>;
  validatePayment(params: { orderId: number, transactionHash: string }): Promise<void>;
  cancelOrder(params: { orderId: number }): Promise<void>;
  sendUploadReminder(params: { orderId: number }): Promise<void>;
  sendRefundRequest(params: any): Promise<void>;
  loading: ComputedProperty<boolean>;
  error: ComputedProperty<UseUserOrderErrors>;
}

export interface UseProductArtifactErrors {
  search: Error;
  downloadArtifact: Error;
  submitArtifact: Error;
  deleteArtifact: Error;
}

export interface UseProductArtifact<ARTIFACTS, ARTIFACT_SEARCH_PARAMS> {
  artifacts: ComputedProperty<ARTIFACTS>;
  search(params: ComposableFunctionArgs<ARTIFACT_SEARCH_PARAMS>): Promise<void>;
  loading: ComputedProperty<boolean>;
  error: ComputedProperty<UseProductArtifactErrors>;
  downloadArtifact(params: { productId: number, artifactId: number }): Promise<void>;
  submitArtifact(params: { orderId: number, artifactId: number }): Promise<void>;
  deleteArtifact(params: { productId: number, artifactId: number }): Promise<void>;
}

export interface UseOrderArtifactErrors {
  search: Error;
  downloadArtifact: Error;
  submitArtifact: Error;
  deleteArtifact: Error;
}

export interface UseOrderArtifact<ARTIFACTS, ARTIFACT_SEARCH_PARAMS> {
  artifacts: ComputedProperty<ARTIFACTS>;
  search(params: ComposableFunctionArgs<ARTIFACT_SEARCH_PARAMS>): Promise<void>;
  loading: ComputedProperty<boolean>;
  error: ComputedProperty<UseOrderArtifactErrors>;
  downloadArtifact(params: { productId: number, artifactId: number }): Promise<void>;
  submitArtifact(params: { orderId: number, artifactId: number }): Promise<void>;
  deleteArtifact(params: { productId: number, artifactId: number }): Promise<void>;
}

export interface UseGlobals {
  load: (identifier: string) => Promise<void>;
  loading: ComputedProperty<boolean>;
  globals: ComputedProperty<any>;
}

export interface UseStats {
  getStats: (identifier: string) => Promise<void>;
  loading: ComputedProperty<boolean>;
  stats: ComputedProperty<any>;
}

export interface UseReviewErrors {
  search: Error;
  addReview: Error;
  loadReviewMetadata: Error;
  loadCustomerReviews: Error;
}

export interface UseReview<REVIEW,
  REVIEWS_SEARCH_PARAMS,
  REVIEWS_USER_SEARCH_PARAMS,
  REVIEW_ADD_PARAMS,
  REVIEW_METADATA>{
  search(params?: ComposableFunctionArgs<REVIEWS_SEARCH_PARAMS>): Promise<void>;

  loadCustomerReviews(params?: ComposableFunctionArgs<REVIEWS_USER_SEARCH_PARAMS>): Promise<void>;

  addReview(params: ComposableFunctionArgs<REVIEW_ADD_PARAMS>): Promise<void>;

  loadReviewMetadata(): Promise<void>;

  error: ComputedProperty<UseReviewErrors>;
  reviews: ComputedProperty<REVIEW>;
  metadata: ComputedProperty<REVIEW_METADATA[]>;
  loading: ComputedProperty<boolean>;

  [x: string]: any;
}

export interface UsePollErrors {
    search: Error;
    pollModal: Error;
    voting: Error;
}

export interface UsePoll<POLLS, POLL_SEARCH_PARAMS> {
  polls: ComputedProperty<POLLS>;
  loading: ComputedProperty<boolean>;
  error: ComputedProperty<UsePollErrors>;
  search(params: ComposableFunctionArgs<POLL_SEARCH_PARAMS>): Promise<any>;
  createPoll(params: { poll: any }): Promise<void>;
  updatePoll(params: { id: string, poll: any }): Promise<void>;
  deletePoll(params: { id: string }): Promise<void>;
  closePoll(params: { id: string }): Promise<void>;
  vote(params: { id: string, options: any[] }): Promise<void>;
  [x: string]: any;
}

export interface UseCouponErrors {
    create: Error;
    delete: Error;
}

export interface UseCoupon<COUPONS, COUPON_SEARCH_PARAMS> {
  loading: ComputedProperty<boolean>;
  error: ComputedProperty<UseCouponErrors>;
  createCoupon(params: { coupon: any }): Promise<void>;
  deleteCoupon(params: { id: number }): Promise<void>;
  [x: string]: any;
}
