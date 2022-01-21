/* istanbul ignore file */
import { ArtifactSearchParams, ArtifactsResponse } from '../types';
import { Context, Logger } from '@vue-storefront/core';
import { UseOrderArtifactFactoryParams, useOrderArtifactFactory } from '../factories/useOrderArtifactFactory';

const params: UseOrderArtifactFactoryParams<ArtifactsResponse, ArtifactSearchParams> = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  searchArtifacts: async (context: Context, params: ArtifactSearchParams): Promise<ArtifactsResponse> => {
    Logger.debug('searchOrderArtifacts');
    return await context.$numerbay.api.getOrderArtifact(params);
  },

  downloadArtifact: async (context: Context, {artifactId}) => {
    Logger.debug('downloadOrderArtifact');
    const response = await context.$numerbay.api.getOrderArtifactDownloadUrl({artifactId});
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  submitArtifact: async (context: Context, {orderId, artifactId}) => {
    Logger.debug('submitArtifact');
    const response = await context.$numerbay.api.submitArtifact({orderId, artifactId});
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  createArtifact: async (context: Context, {productId, artifact}) => {
    Logger.debug('createArtifact');
    const response = await context.$numerbay.api.createArtifact({productId, ...artifact});
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  updateArtifact: async (context: Context, {productId, artifactId, description}) => {
    Logger.debug('updateArtifact');
    const response = await context.$numerbay.api.updateArtifact({productId, artifactId, description});
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  deleteArtifact: async (context: Context, {artifactId}) => {
    Logger.debug('deleteOrderArtifact');
    const response = await context.$numerbay.api.deleteOrderArtifact({artifactId});
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  }
};

export default useOrderArtifactFactory<ArtifactsResponse, ArtifactSearchParams>(params);
