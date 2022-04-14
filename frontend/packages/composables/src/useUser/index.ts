/* istanbul ignore file */

import {Context, Logger} from '@vue-storefront/core';
import { UseUserFactoryParams, useUserFactory } from '../factories/useUserFactory';
import { disconnectWallet, setChainData, setEthersProvider } from './utils';
import { User } from '../types';
// import Web3Modal from 'web3modal';

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
  getNonce: async (context: Context, { publicAddress }) => {
    Logger.debug('getNonce');
    const data = await context.$numerbay.api.logInGetNonce({publicAddress});
    return data;
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  getNonceAuthenticated: async (context: Context, { currentUser }) => {
    Logger.debug('getNonceAuthenticated');
    const data = await context.$numerbay.api.logInGetNonceAuthenticated();
    return data;
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  updateUser: async (context: Context, { currentUser, updatedUserData }) => {
    Logger.debug('UpdateUser');
    const response = await context.$numerbay.api.userUpdateMe(updatedUserData);
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  syncUserNumerai: async (context: Context, { currentUser }) => {
    Logger.debug('syncUserNumerai');
    const response = await context.$numerbay.api.userSyncNumerai();
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
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
    return response.user;
  },

  logInWeb3: async (context: Context, { publicAddress, signature }) => {
    Logger.debug('LogInWeb3');
    const response = await context.$numerbay.api.logInGetTokenWeb3({publicAddress, signature});
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response.user;
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  changePassword: async (context: Context, { currentUser, currentPassword, newPassword }) => {
    Logger.debug('Mocked: changePassword');
    return {};
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  initWeb3Modal: async (context: Context, { currentWeb3User }) => {
    Logger.debug('initWeb3Modal');
    try {
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

      // const w3mObject = new Web3Modal({
      //   cacheProvider: true, // optional
      //   providerOptions // required
      // });
      //
      // // This will get deprecated soon. Setting it to false removes a warning from the console.
      // window.ethereum.autoRefreshOnNetworkChange = false;
      //
      // // if the user is flagged as already connected, automatically connect back to Web3Modal
      // if (localStorage.getItem('isConnected') === 'true') {
      //   try {
      //     const providerW3m = await w3mObject.connect();
      //     currentWeb3User.activeAccount = window.ethereum.selectedAddress;
      //     setChainData(currentWeb3User, window.ethereum.chainId);
      //     await setEthersProvider(currentWeb3User, providerW3m);
      //     currentWeb3User.activeBalance = await currentWeb3User.providerEthers.getBalance(currentWeb3User.activeAccount);
      //     // setIsConnected(currentWeb3User, true);
      //     // indicate that this is auto login, used for detecting public address change
      //     localStorage.setItem('cachedPublicAddress', window.ethereum.selectedAddress);
      //   } catch (e) {
      //     console.log('Connect Error: ', e);
      //   }
      // }
      // currentWeb3User.web3Modal = w3mObject;
    } catch (err) {
      Logger.error(err);
      throw new Error(
        'Failed to initialize MetaMask. Please make sure it is enabled.'
      );
    }
  },

  ethereumListener: async (context: Context, { currentWeb3User }) => {
    Logger.debug('ethereumListener');
    // window.ethereum.on('accountsChanged', async (accounts) => {
    //   // if (currentWeb3User.isConnected) {
    //   currentWeb3User.activeAccount = accounts[0];
    //   await setEthersProvider(currentWeb3User, currentWeb3User.providerW3m);
    //   currentWeb3User.activeBalance = await currentWeb3User.providerEthers.getBalance(currentWeb3User.activeAccount);
    //   // }
    // });
    //
    // window.ethereum.on('chainChanged', async () => {
    //   setChainData(currentWeb3User, window.ethereum.chainId);
    //   await setEthersProvider(currentWeb3User, currentWeb3User.providerW3m);
    //   currentWeb3User.activeBalance = await currentWeb3User.providerEthers.getBalance(currentWeb3User.activeAccount);
    // });
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  connectWeb3Modal: async (context: Context, { currentWeb3User }) => {
    Logger.debug('connectWeb3Modal');
    Logger.debug('currentWeb3User: ', currentWeb3User);
    // const w3mObject = currentWeb3User.web3Modal;
    // try {
    //   const providerW3m = await currentWeb3User.web3Modal.connect();
    //   currentWeb3User.web3Modal = w3mObject;
    //   currentWeb3User.activeAccount = window.ethereum.selectedAddress;
    //   setChainData(currentWeb3User, window.ethereum.chainId);
    //   await setEthersProvider(currentWeb3User, providerW3m);
    //   currentWeb3User.activeBalance = await currentWeb3User.providerEthers.getBalance(currentWeb3User.activeAccount);
    //   // setIsConnected(currentWeb3User, true);
    // } catch (e) {
    //   console.log('Connect Error: ', e);
    // }
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  disconnectWeb3Modal: async (context: Context, { currentWeb3User }) => {
    Logger.debug('disconnectWeb3Modal');
    await disconnectWallet(currentWeb3User);
    // setIsConnected(currentWeb3User, false);
  }
};

export default useUserFactory<User, any, any>(params);
