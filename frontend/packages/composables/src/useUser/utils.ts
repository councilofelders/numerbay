// import {ethers} from 'ethers';

export const setChainData = (state, chainId) => {
  state.chainId = chainId;

  switch (chainId) {
    case '0x1':
      state.chainName = 'Mainnet';
      break;
    case '0x2a':
      state.chainName = 'Kovan';
      break;
    case '0x3':
      state.chainName = 'Ropsten';
      break;
    case '0x4':
      state.chainName = 'Rinkeby';
      break;
    case '0x5':
      state.chainName = 'Goerli';
      break;
      // eslint-disable-next-line line-comment-position
    case '0x539': // 1337 (often used on localhost)
      // eslint-disable-next-line line-comment-position,no-fallthrough
    case '0x1691': // 5777 (default in Ganache)
    default:
      state.chainName = 'Localhost';
      break;
  }
};

export const setEthersProvider = async (state, providerW3m) => {
  state.providerW3m = providerW3m;
  // state.providerEthers = new ethers.providers.Web3Provider(providerW3m);
};

export const setIsConnected = (state, isConnected) => {
  state.isConnected = isConnected;
  // add to persistent storage so that the user can be logged back in when revisiting website
  localStorage.setItem('isConnected', String(isConnected));
  if (!isConnected) {
    localStorage.removeItem('isConnected');
    localStorage.removeItem('cachedPublicAddress');
  }
};

export const disconnectWallet = async (state) => {
  state.activeAccount = null;
  state.activeBalance = 0;
  state.providerEthers = null;
  if (state?.providerW3m && state.providerW3m.close && state.providerW3m !== null) {
    await state.providerW3m.close();
  }
  state.providerW3m = null;
  if (state?.web3Modal) {
    await state.web3Modal.clearCachedProvider();
  }
};
