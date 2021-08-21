import {apiClientFactory, ApiClientExtension, Logger} from '@vue-storefront/core';
import getProduct from './api/getProduct';
import createProduct from './api/createProduct';
import updateProduct from './api/updateProduct';
import deleteProduct from './api/deleteProduct';
import getCategory from './api/getCategory';
import signUpUser from './api/signUpUser';
import logInGetToken from './api/logInGetToken';
import logInGetTokenWeb3 from './api/logInGetTokenWeb3';
import logInGetNonce from './api/logInGetNonce';
import logOutUser from './api/logOutUser';
import getMe from './api/getMe';
import userUpdateMe from './api/userUpdateMe';
import getNumeraiModels from './api/getNumeraiModels';
import getNumeraiModelInfo from './api/getNumeraiModelInfo';
import getOrder from './api/getOrder';
import createOrder from './api/createOrder';
import axios from 'axios';

// const defaultSettings = {};

const onCreate = (settings) => {
  const client = axios.create({
    baseURL: settings.api.url
  });

  client.interceptors.request.use(request => {
    Logger.debug('Starting Request', JSON.stringify(request, null, 2));
    return request;
  });

  client.interceptors.response.use(response => {
    Logger.debug('Response:', response);
    // console.log('Response:', JSON.stringify(response, null, 2));
    return response;
  });

  return {
    config: settings,
    client
  };
};

const parseToken = (rawToken) => {
  try {
    return JSON.parse(rawToken);
  } catch (e) {
    return null;
  }
};

const tokenExtension: ApiClientExtension = {
  name: 'tokenExtension',
  hooks: (req, res) => {
    const rawCurrentToken = req.cookies['nb-token'];
    const currentToken = parseToken(rawCurrentToken);

    return {
      beforeCreate: ({ configuration }) => ({
        ...configuration,
        auth: {
          onTokenChange: (newToken) => {
            if (!currentToken || currentToken !== newToken) {
              res.cookie(
                'nb-token',
                JSON.stringify(newToken),
                newToken?.expires_at ? { expires: new Date(newToken.expires_at) } : {}
              );
            }
          },

          onTokenRead: () => {
            res.cookie(
              'nb-token',
              rawCurrentToken,
              currentToken?.expires_at ? { expires: new Date(currentToken.expires_at) } : {}
            );
            return currentToken;
          },

          onTokenRemove: () => {
            delete req.cookies['nb-token'];
            res.clearCookie('nb-token');
          }
        }
      })
    };
  }
};

const { createApiClient } = apiClientFactory<any, any>({
  onCreate,
  api: {
    getProduct,
    createProduct,
    updateProduct,
    deleteProduct,
    getCategory,
    signUpUser,
    logInGetToken,
    logInGetTokenWeb3,
    logInGetNonce,
    logOutUser,
    getMe,
    userUpdateMe,
    getNumeraiModels,
    getNumeraiModelInfo,
    getOrder,
    createOrder
  },
  extensions: [tokenExtension]
});

export {
  createApiClient
};
