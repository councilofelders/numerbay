import {ApiClientExtension, Logger, apiClientFactory} from '@vue-storefront/core';
import axios from 'axios';
import closePoll from './api/closePoll';
import createFavorite from './api/createFavorite';
import createOrder from './api/createOrder';
import createPoll from './api/createPoll';
import createProduct from './api/createProduct';
import createCoupon from './api/createCoupon';
import deleteCoupon from './api/deleteCoupon';
import createReview from './api/createReview';
import deleteArtifact from './api/deleteArtifact';
import deleteFavorite from './api/deleteFavorite';
import deleteOrderArtifact from './api/deleteOrderArtifact';
import deletePoll from './api/deletePoll';
import deleteProduct from './api/deleteProduct';
import testProductWebhook from './api/testProductWebhook';
import getArtifact from './api/getArtifact';
import getArtifactDownloadUrl from './api/getArtifactDownloadUrl';
import getArtifactUploadUrl from './api/getArtifactUploadUrl';
import getCategory from './api/getCategory';
import getFavorite from './api/getFavorite';
import getGlobals from './api/getGlobals';
import getStats from './api/getStats';
import getMe from './api/getMe';
import getNumeraiModelInfo from './api/getNumeraiModelInfo';
import getNumeraiModels from './api/getNumeraiModels';
import getOrder from './api/getOrder';
import getOrderArtifact from './api/getOrderArtifact';
import getOrderArtifactDownloadUrl from './api/getOrderArtifactDownloadUrl';
import getOrderArtifactUploadUrl from './api/getOrderArtifactUploadUrl';
import getPoll from './api/getPoll';
import getProduct from './api/getProduct';
import getSalesLeaderboard from './api/getSalesLeaderboard';
import getReview from './api/getReview';
import logInGetNonce from './api/logInGetNonce';
import logInGetNonceAuthenticated from './api/logInGetNonceAuthenticated';
import logInGetToken from './api/logInGetToken';
import logInGetTokenWeb3 from './api/logInGetTokenWeb3';
import logOutUser from './api/logOutUser';
import signUpUser from './api/signUpUser';
import submitArtifact from './api/submitArtifact';
import updateOrderSubmissionModel from './api/updateOrderSubmissionModel';
import updatePoll from './api/updatePoll';
import updateProduct from './api/updateProduct';
import userUpdateMe from './api/userUpdateMe';
import userSyncNumerai from './api/userSyncNumerai';
import validateArtifactUpload from './api/validateArtifactUpload';
import validateOrderArtifactUpload from './api/validateOrderArtifactUpload';
import validatePayment from './api/validatePayment';
import cancelOrder from './api/cancelOrder';
import sendOrderUploadReminder from './api/sendOrderUploadReminder';
import votePoll from './api/votePoll';

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
    getSalesLeaderboard,
    createProduct,
    updateProduct,
    deleteProduct,
    createCoupon,
    deleteCoupon,
    testProductWebhook,
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
    userSyncNumerai,
    getNumeraiModels,
    getNumeraiModelInfo,
    getOrder,
    createOrder,
    getGlobals,
    getStats,
    getArtifactDownloadUrl,
    getOrderArtifactDownloadUrl,
    getArtifactUploadUrl,
    getOrderArtifactUploadUrl,
    validateArtifactUpload,
    validateOrderArtifactUpload,
    updateOrderSubmissionModel,
    validatePayment,
    sendOrderUploadReminder,
    cancelOrder,
    getArtifact,
    getOrderArtifact,
    submitArtifact,
    deleteArtifact,
    deleteOrderArtifact,
    getPoll,
    createPoll,
    updatePoll,
    deletePoll,
    closePoll,
    votePoll
  },
  extensions: [tokenExtension]
});

export {
  createApiClient
};
