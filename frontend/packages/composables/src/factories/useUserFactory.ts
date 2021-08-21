import { Ref, computed } from '@vue/composition-api';
import { Context, FactoryParams, CustomQuery } from '@vue-storefront/core';
import { UseUser, UseWeb3User, UseUserErrors } from '../types/composeables';
import { sharedRef, Logger, mask, configureFactoryParams } from '@vue-storefront/core';

export interface UseUserFactoryParams<USER, UPDATE_USER_PARAMS, REGISTER_USER_PARAMS> extends FactoryParams {
  load: (context: Context, params?: { customQuery: CustomQuery }) => Promise<USER>;
  logOut: (context: Context, params: {currentUser: USER}) => Promise<void>;
  getNonce: (context: Context, params: {publicAddress: string}) => Promise<void>;
  getNonceAuthenticated: (context: Context, params: {currentUser: USER}) => Promise<void>;
  updateUser: (context: Context, params: {currentUser: USER; updatedUserData: UPDATE_USER_PARAMS; customQuery?: CustomQuery}) => Promise<USER>;
  register: (context: Context, params: REGISTER_USER_PARAMS & {customQuery?: CustomQuery}) => Promise<USER>;
  logIn: (context: Context, params: { username: string; password: string; customQuery?: CustomQuery }) => Promise<USER>;
  logInWeb3: (context: Context, params: { publicAddress: string; signature: string; customQuery?: CustomQuery }) => Promise<USER>;
  initWeb3Modal: (context: Context, params: { currentWeb3User: UseWeb3User }) => Promise<void>;
  ethereumListener: (context: Context, params: { currentWeb3User: UseWeb3User }) => Promise<void>;
  connectWeb3Modal: (context: Context, params: { currentWeb3User: UseWeb3User }) => Promise<void>;
  disconnectWeb3Modal: (context: Context, params: { currentWeb3User: UseWeb3User }) => Promise<void>;
  changePassword: (context: Context, params: {currentUser: USER; currentPassword: string; newPassword: string; customQuery?: CustomQuery}) => Promise<USER>;
}

export const useUserFactory = <USER, UPDATE_USER_PARAMS, REGISTER_USER_PARAMS extends { email: string; password: string }>(
  factoryParams: UseUserFactoryParams<USER, UPDATE_USER_PARAMS, REGISTER_USER_PARAMS>
) => {
  return function useUser (): UseUser<USER, UPDATE_USER_PARAMS> {
    const errorsFactory = (): UseUserErrors => ({
      updateUser: null,
      register: null,
      login: null,
      web3: null,
      logout: null,
      changePassword: null,
      load: null
    });

    const web3UserFactory = (): UseWeb3User => ({
      nonce: null,
      activeAccount: null,
      activeBalance: 0,
      chainId: null,
      chainName: null,
      // eslint-disable-next-line line-comment-position
      providerEthers: null, // this is "provider" for Ethers.js
      isConnected: false,
      // eslint-disable-next-line line-comment-position
      providerW3m: null, // this is "provider" from Web3Modal
      web3Modal: null
    });

    const user: Ref<USER> = sharedRef(null, 'useUser-user');
    const web3User: Ref<UseWeb3User> = sharedRef(web3UserFactory(), 'useUser-web3User');
    const loading: Ref<boolean> = sharedRef(false, 'useUser-loading');
    const isAuthenticated = computed(() => Boolean(user.value));
    const _factoryParams = configureFactoryParams(factoryParams);
    const error: Ref<UseUserErrors> = sharedRef(errorsFactory(), 'useUser-error');

    const setUser = (newUser: USER) => {
      user.value = newUser;
      Logger.debug('useUserFactory.setUser', newUser);
    };

    const resetErrorValue = () => {
      error.value = errorsFactory();
    };

    const updateUser = async ({ user: providedUser, customQuery }) => {
      Logger.debug('useUserFactory.updateUser', providedUser);
      resetErrorValue();

      try {
        loading.value = true;
        user.value = await _factoryParams.updateUser({currentUser: user.value, updatedUserData: providedUser, customQuery});
        error.value.updateUser = null;
      } catch (err) {
        error.value.updateUser = err;
        Logger.error('useUser/updateUser', err);
      } finally {
        loading.value = false;
      }
    };

    const register = async ({ user: providedUser, customQuery } = { user: null, customQuery: null }) => {
      Logger.debug('useUserFactory.register', providedUser);
      resetErrorValue();

      try {
        loading.value = true;
        user.value = await _factoryParams.register({...providedUser, customQuery});
        error.value.register = null;
      } catch (err) {
        error.value.register = err;
        Logger.error('useUser/register', err);
      } finally {
        loading.value = false;
      }
    };

    const login = async ({ user: providedUser, customQuery } = { user: null, customQuery: null }) => {
      Logger.debug('useUserFactory.login', providedUser);
      resetErrorValue();

      try {
        loading.value = true;
        user.value = await _factoryParams.logIn({...providedUser, customQuery});
        error.value.login = null;
      } catch (err) {
        error.value.login = err;
        Logger.error('useUser/login', err);
      } finally {
        loading.value = false;
      }
    };

    const loginWeb3 = async ({ user: providedUser, customQuery } = { user: null, customQuery: null }) => {
      Logger.debug('useUserFactory.loginWeb3', providedUser);
      resetErrorValue();

      try {
        loading.value = true;
        user.value = await _factoryParams.logInWeb3({...providedUser, customQuery});
        error.value.web3 = null;
      } catch (err) {
        error.value.web3 = err;
        Logger.error('useUser/loginWeb3', err);
      } finally {
        loading.value = false;
      }
    };

    const logout = async () => {
      Logger.debug('useUserFactory.logout');
      resetErrorValue();

      try {
        await _factoryParams.logOut({ currentUser: user.value });
        // log out of metamask as well
        await _factoryParams.disconnectWeb3Modal({ currentWeb3User: web3User.value });
        error.value.logout = null;
        user.value = null;
        web3User.value = web3UserFactory();
      } catch (err) {
        error.value.logout = err;
        Logger.error('useUser/logout', err);
      }
    };

    const getNonce = async ({publicAddress}) => {
      Logger.debug('useUserFactory.getNonce');
      resetErrorValue();

      try {
        web3User.value.nonce = await _factoryParams.getNonce({publicAddress});

        error.value.login = null;
      } catch (err) {
        error.value.login = err;
        Logger.error('useUser/getNonce', err);
      }
    };

    const getNonceAuthenticated = async () => {
      Logger.debug('useUserFactory.getNonceAuthenticated');
      resetErrorValue();

      try {
        web3User.value.nonce = await _factoryParams.getNonceAuthenticated({ currentUser: user.value });

        error.value.login = null;
      } catch (err) {
        error.value.login = err;
        Logger.error('useUser/getNonceAuthenticated', err);
      }
    };

    const changePassword = async (params = { current: null, new: null, customQuery: null }) => {
      Logger.debug('useUserFactory.changePassword', { currentPassword: mask(params.current), newPassword: mask(params.new) });
      resetErrorValue();

      try {
        loading.value = true;
        user.value = await _factoryParams.changePassword({
          currentUser: user.value,
          currentPassword: params.current,
          newPassword: params.new,
          customQuery: params.customQuery
        });
        error.value.changePassword = null;
      } catch (err) {
        error.value.changePassword = err;
        Logger.error('useUser/changePassword', err);
      } finally {
        loading.value = false;
      }
    };

    const load = async ({customQuery} = {customQuery: undefined}) => {
      Logger.debug('useUserFactory.load');
      resetErrorValue();

      try {
        loading.value = true;
        user.value = await _factoryParams.load({customQuery});
        error.value.load = null;
      } catch (err) {
        error.value.load = err;
        Logger.error('useUser/load', err);
      } finally {
        loading.value = false;
      }
    };

    const initWeb3Modal = async () => {
      Logger.debug('useUserFactory.initWeb3Modal');
      resetErrorValue();

      try {
        await _factoryParams.initWeb3Modal({ currentWeb3User: web3User.value });
        error.value.login = null;
      } catch (err) {
        error.value.login = err;
        Logger.error('useUser/initWeb3Modal', err);
      }
    };

    const ethereumListener = async () => {
      Logger.debug('useUserFactory.ethereumListener');
      resetErrorValue();

      try {
        await _factoryParams.ethereumListener({ currentWeb3User: web3User.value });
        error.value.login = null;
      } catch (err) {
        error.value.login = err;
        Logger.error('useUser/ethereumListener', err);
      }
    };

    const connectWeb3Modal = async () => {
      Logger.debug('useUserFactory.connectWeb3Modal');
      resetErrorValue();

      try {
        await _factoryParams.connectWeb3Modal({ currentWeb3User: web3User.value });
        error.value.login = null;
      } catch (err) {
        error.value.login = err;
        Logger.error('useUser/connectWeb3Modal', err);
      }
    };

    const disconnectWeb3Modal = async () => {
      Logger.debug('useUserFactory.disconnectWeb3Modal');
      resetErrorValue();

      try {
        await _factoryParams.disconnectWeb3Modal({ currentWeb3User: web3User.value });
        error.value.login = null;
        web3User.value = web3UserFactory();
      } catch (err) {
        error.value.login = err;
        Logger.error('useUser/disconnectWeb3Modal', err);
      }
    };

    return {
      setUser,
      user: computed(() => user.value),
      web3User: computed(() => web3User.value),
      updateUser,
      register,
      login,
      loginWeb3,
      logout,
      getNonce,
      getNonceAuthenticated,
      initWeb3Modal,
      ethereumListener,
      connectWeb3Modal,
      disconnectWeb3Modal,
      isAuthenticated,
      changePassword,
      load,
      loading: computed(() => loading.value),
      error: computed(() => error.value)
    };
  };
};
