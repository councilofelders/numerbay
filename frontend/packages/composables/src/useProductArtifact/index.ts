/* istanbul ignore file */

import { Context, Logger } from '@vue-storefront/core';
import { useProductArtifactFactory, UseProductArtifactFactoryParams } from '../factories/useProductArtifactFactory';
import { ArtifactsResponse, ArtifactSearchParams } from '../types';

const params: UseProductArtifactFactoryParams<ArtifactsResponse, ArtifactSearchParams> = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  searchArtifacts: async (context: Context, params: ArtifactSearchParams): Promise<ArtifactsResponse> => {
    Logger.debug('searchArtifacts');
    return await context.$numerbay.api.getArtifact(params);
  },

  downloadArtifact: async (context: Context, {productId, artifactId}) => {
    Logger.debug('downloadArtifact');
    const response = await context.$numerbay.api.getArtifactDownloadUrl({productId, artifactId});
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

  deleteArtifact: async (context: Context, {productId, artifactId}) => {
    Logger.debug('deleteArtifact');
    const response = await context.$numerbay.api.deleteArtifact({productId, artifactId});
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  }
};

export default useProductArtifactFactory<ArtifactsResponse, ArtifactSearchParams>(params);
