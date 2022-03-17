export const AVALANCHE_MAINNET_PARAMS = {
  chainId: '0xA86A',
  chainName: 'Avalanche Mainnet C-Chain',
  nativeCurrency: {
    name: 'Avalanche',
    symbol: 'AVAX',
    decimals: 18
  },
  rpcUrls: ['https://api.avax.network/ext/bc/C/rpc'],
  blockExplorerUrls: ['https://snowtrace.io']
};

export const AVALANCHE_TESTNET_PARAMS = {
  chainId: '0xA869',
  chainName: 'Avalanche Testnet C-Chain',
  nativeCurrency: {
    name: 'Avalanche',
    symbol: 'AVAX',
    decimals: 18
  },
  rpcUrls: ['https://api.avax-test.network/ext/bc/C/rpc'],
  blockExplorerUrls: ['https://testnet.snowtrace.io']
};

export const POLYGON_MAINNET_PARAMS = {
  chainId: '0x89',
  chainName: 'Polygon Mainnet',
  nativeCurrency: {
    name: 'Polygon',
    symbol: 'MATIC',
    decimals: 18
  },
  rpcUrls: [
    'https://polygon-rpc.com',
    'https://rpc-mainnet.matic.network',
    'https://rpc-mainnet.maticvigil.com',
    'https://rpc-mainnet.matic.quiknode.pro'
  ],
  blockExplorerUrls: ['https://polygonscan.com']
};

export const POLYGON_MUMBAI_TESTNET_CONFIG = {
  chainId: '0x13881',
  chainName: 'Polygon Testnet',
  nativeCurrency: {
    name: 'Polygon',
    symbol: 'MATIC',
    decimals: 18
  },
  rpcUrls: ['https://rpc-mumbai.maticvigil.com'],
  blockExplorerUrls: ['https://mumbai.polygonscan.com']
};

export const FANTOM_TESTNET_CONFIG = {
  chainId: '0xfa2',
  chainName: 'Fantom Testnet',
  nativeCurrency: {
    name: 'Fantom',
    symbol: 'FTM',
    decimals: 18
  },
  rpcUrls: ['https://rpc.testnet.fantom.network'],
  blockExplorerUrls: ['https://testnet.ftmscan.com']
};

export const FANTOM_MAINNET_CONFIG = {
  chainId: '0xFA',
  chainName: 'Fantom Opera',
  nativeCurrency: {
    name: 'Fantom',
    symbol: 'FTM',
    decimals: 18
  },
  rpcUrls: ['https://rpc.ftm.tools'],
  blockExplorerUrls: ['https://ftmscan.com']
};

export const ETHEREUM_RINKEBY = {
  chainId: '0x4',
  chainName: 'Rinkeby',
  nativeCurrency: {
    name: 'Ethereum',
    symbol: 'ETH',
    decimals: 18
  },
  rpcUrls: [],
  blockExplorerUrls: ['https://rinkeby.etherscan.io']
};

export const ETHEREUM_MAINNET = {
  chainId: '0x1',
  chainName: 'Mainnet',
  nativeCurrency: {
    name: 'Ethereum',
    symbol: 'ETH',
    decimals: 18
  },
  rpcUrls: [],
  blockExplorerUrls: ['https://etherscan.io']
};

export const BSC_MAINNET = {
  chainId: '0x38',
  chainName: 'Binance Smart Chain',
  nativeCurrency: {
    name: 'BNB',
    symbol: 'BNB',
    decimals: 18
  },
  rpcUrls: ['https://bsc-dataseed.binance.org'],
  blockExplorerUrls: ['https://bscscan.com']
};

export const BSC_TESTNET = {
  chainId: '0x61',
  chainName: 'Binance Smart Chain Testnet',
  nativeCurrency: {
    name: 'BNB',
    symbol: 'BNB',
    decimals: 18
  },
  rpcUrls: ['https://data-seed-prebsc-1-s1.binance.org:8545/'],
  blockExplorerUrls: ['https://testnet.bscscan.com']
};

export function getMainnetConfig(testnetChainId) {
  if (['0x4', '4'].includes(testnetChainId)) return ETHEREUM_MAINNET;
  if (['0xA869', '43113'].includes(testnetChainId)) return AVALANCHE_MAINNET_PARAMS;
  if (['0x89', '80001'].includes(testnetChainId)) return POLYGON_MAINNET_PARAMS;
  if (['0xFA2', '4002'].includes(testnetChainId)) return FANTOM_MAINNET_CONFIG;
  if (['0x38', '56'].includes(testnetChainId)) return BSC_MAINNET;

  throw new Error('Matching mainnet config not found');
}

export const CHAINID_CONFIG_MAP = {
  43114: AVALANCHE_MAINNET_PARAMS,
  43113: AVALANCHE_TESTNET_PARAMS,
  80001: POLYGON_MUMBAI_TESTNET_CONFIG,
  4: ETHEREUM_RINKEBY,
  1: ETHEREUM_MAINNET,
  4002: FANTOM_TESTNET_CONFIG,
  250: FANTOM_MAINNET_CONFIG,
  56: BSC_MAINNET,
  97: BSC_TESTNET,

  '0xA86A': AVALANCHE_MAINNET_PARAMS,
  '0xA869': AVALANCHE_TESTNET_PARAMS,
  '0x13881': POLYGON_MUMBAI_TESTNET_CONFIG,
  '0x89': POLYGON_MAINNET_PARAMS,
  '0x4': ETHEREUM_RINKEBY,
  '0x1': ETHEREUM_MAINNET,
  '0xFA2': FANTOM_TESTNET_CONFIG,
  '0xFA': FANTOM_MAINNET_CONFIG,
  '0x38': BSC_MAINNET,
  '0x61': BSC_TESTNET
};

export const FAUCETS = {
  43113: ['https://faucet.avax-test.network'],
  80001: ['https://faucet.polygon.technology'],
  4: ['https://faucet.rinkeby.io', 'https://faucets.chain.link/rinkeby'],
  4002: ['https://faucet.fantom.network'],
  97: ['https://testnet.binance.org/faucet-smart']
};

export const isTestnet = (chainId) => {
  return ['43113', '80001', '4', '4002', '97', '0xA869', '0x13881', '0x4', '0xFA2', '0x61'].includes(chainId);
};

export function getExplorerUrl(chainId) {
  return CHAINID_CONFIG_MAP[chainId]?.blockExplorerUrls[0];
}

export function getCurrency(chainId) {
  return CHAINID_CONFIG_MAP[chainId]?.nativeCurrency.symbol;
}

export function getNetwork(chainId) {
  return CHAINID_CONFIG_MAP[chainId]?.chainName;
}

export function getFaucetList(chainId) {
  return CHAINID_CONFIG_MAP[chainId]?.faucetUrls;
}
