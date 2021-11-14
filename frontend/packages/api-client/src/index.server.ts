import {apiClientFactory, ApiClientExtension, Logger} from '@vue-storefront/core';
import getProduct from './api/getProduct';
import createProduct from './api/createProduct';
import updateProduct from './api/updateProduct';
import deleteProduct from './api/deleteProduct';
import getCategory from './api/getCategory';
import getReview from './api/getReview';
import getFavorite from './api/getFavorite';
import createFavorite from './api/createFavorite';
import deleteFavorite from './api/deleteFavorite';
import createReview from './api/createReview';
import signUpUser from './api/signUpUser';
import logInGetToken from './api/logInGetToken';
import logInGetTokenWeb3 from './api/logInGetTokenWeb3';
import logInGetNonce from './api/logInGetNonce';
import logInGetNonceAuthenticated from './api/logInGetNonceAuthenticated';
import logOutUser from './api/logOutUser';
import getMe from './api/getMe';
import userUpdateMe from './api/userUpdateMe';
import getNumeraiModels from './api/getNumeraiModels';
import getNumeraiModelInfo from './api/getNumeraiModelInfo';
import getOrder from './api/getOrder';
import createOrder from './api/createOrder';
import getGlobals from './api/getGlobals';
import getArtifactDownloadUrl from './api/getArtifactDownloadUrl';
import getArtifactUploadUrl from './api/getArtifactUploadUrl';
import validateArtifactUpload from './api/validateArtifactUpload';
import getArtifact from './api/getArtifact';
import createArtifact from './api/createArtifact';
import submitArtifact from './api/submitArtifact';
import updateArtifact from './api/updateArtifact';
import deleteArtifact from './api/deleteArtifact';
import getPoll from './api/getPoll';
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
    getReview,
    getFavorite,
    createFavorite,
    deleteFavorite,
    createReview,
    signUpUser,
    logInGetToken,
    logInGetTokenWeb3,
    logInGetNonce,
    logInGetNonceAuthenticated,
    logOutUser,
    getMe,
    userUpdateMe,
    getNumeraiModels,
    getNumeraiModelInfo,
    getOrder,
    createOrder,
    getGlobals,
    getArtifactDownloadUrl,
    getArtifactUploadUrl,
    validateArtifactUpload,
    getArtifact,
    createArtifact,
    submitArtifact,
    updateArtifact,
    deleteArtifact,
    getPoll
  },
  extensions: [tokenExtension]
});

export {
  createApiClient
};
