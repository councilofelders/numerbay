/* istanbul ignore file */

import {Context, Logger} from '@vue-storefront/core';
import { useUserFactory, UseUserFactoryParams } from '../factories/useUserFactory';
import { User } from '../types';
import Web3Modal from 'web3modal';
import { setChainData, setEthersProvider, setIsConnected, disconnectWallet } from './utils';

// @todo useUser

const params: UseUserFactoryParams<User, any, any> = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  load: async (context: Context) => {
    Logger.debug('load user');
    try {
      return await context.$numerbay.api.getMe();
    } catch (e) {
      return null;
    }
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  logOut: async (context: Context) => {
    Logger.debug('LogOut');
    await context.$numerbay.api.logOutUser();
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  updateUser: async (context: Context, { currentUser, updatedUserData }) => {
    Logger.debug('UpdateUser');
    const data = await context.$numerbay.api.userUpdateMe(updatedUserData);
    return data;
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  register: async (context: Context, { username, password }) => {
    Logger.debug('register');
    const registerResponse = await context.$numerbay.api.signUpUser({username: username, password: password});
    if (registerResponse?.error) {
      throw new Error(registerResponse.detail);
    }
    const response = await context.$numerbay.api.logInGetToken({username: username, password: password});
    return response;
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  logIn: async (context: Context, { username, password }) => {
    Logger.debug('LogIn');
    const response = await context.$numerbay.api.logInGetToken({username: username, password: password});
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  changePassword: async (context: Context, { currentUser, currentPassword, newPassword }) => {
    Logger.debug('Mocked: changePassword');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  initWeb3Modal: async (context: Context, { currentWeb3User }) => {
    Logger.debug('initWeb3Modal');
    const providerOptions = {
      // MetaMask is enabled by default
      // Find other providers here: https://github.com/Web3Modal/web3modal/tree/master/docs/providers
      // burnerconnect: {
      //   package: BurnerConnectProvider // required
      // },
      // authereum: {
      //   package: Authereum // required
      // }
    };

    const w3mObject = new Web3Modal({
      cacheProvider: true, // optional
      providerOptions // required
    });

    // This will get deprecated soon. Setting it to false removes a warning from the console.
    window.ethereum.autoRefreshOnNetworkChange = false;

    // if the user is flagged as already connected, automatically connect back to Web3Modal
    if (localStorage.getItem('isConnected') === 'true') {
      try {
        const providerW3m = await w3mObject.connect();
        setIsConnected(currentWeb3User, true);
        currentWeb3User.activeAccount = window.ethereum.selectedAddress;
        setChainData(currentWeb3User, window.ethereum.chainId);
        setEthersProvider(currentWeb3User, providerW3m);
        currentWeb3User.activeBalance = await currentWeb3User.providerEthers.getBalance(currentWeb3User.activeAccount);
        // indicate that this is auto login, used for detecting public address change
        localStorage.setItem('cachedPublicAddress', window.ethereum.selectedAddress);
      } catch (e) {
        console.log('Connect Error: ', e);
      }
    }
    currentWeb3User.web3Modal = w3mObject;
  },

  ethereumListener: async (context: Context, { currentWeb3User }) => {
    Logger.debug('ethereumListener');
    window.ethereum.on('accountsChanged', async (accounts) => {
      if (currentWeb3User.isConnected) {
        currentWeb3User.activeAccount = accounts[0];
        setEthersProvider(currentWeb3User, currentWeb3User.providerW3m);
        currentWeb3User.activeBalance = await currentWeb3User.providerEthers.getBalance(currentWeb3User.activeAccount);
      }
    });

    window.ethereum.on('chainChanged', async () => {
      setChainData(currentWeb3User, window.ethereum.chainId);
      setEthersProvider(currentWeb3User, currentWeb3User.providerW3m);
      currentWeb3User.activeBalance = await currentWeb3User.providerEthers.getBalance(currentWeb3User.activeAccount);
    });
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  connectWeb3Modal: async (context: Context, { currentWeb3User }) => {
    Logger.debug('connectWeb3Modal');
    Logger.debug('currentWeb3User: ', currentWeb3User);
    const w3mObject = currentWeb3User.web3Modal;
    try {
      const providerW3m = await currentWeb3User.web3Modal.connect();
      currentWeb3User.web3Modal = w3mObject;
      setIsConnected(currentWeb3User, true);

      currentWeb3User.activeAccount = window.ethereum.selectedAddress;
      setChainData(currentWeb3User, window.ethereum.chainId);
      setEthersProvider(currentWeb3User, providerW3m);
      currentWeb3User.activeBalance = await currentWeb3User.providerEthers.getBalance(currentWeb3User.activeAccount);
    } catch (e) {
      console.log('Connect Error: ', e);
    }
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  disconnectWeb3Modal: async (context: Context, { currentWeb3User }) => {
    Logger.debug('disconnectWeb3Modal');
    disconnectWallet(currentWeb3User);
    setIsConnected(currentWeb3User, false);
  }
};

export default useUserFactory<User, any, any>(params);
