import {Context, Logger} from '@vue-storefront/core';
import { useNumeraiFactory, UseNumeraiFactoryParams } from '../factories/useNumeraiFactory';

const factoryParams: UseNumeraiFactoryParams = {
  getModels: async (context: Context) => {
    Logger.debug('getNumeraiModels');
    const response = await context.$numerbay.api.getNumeraiModels();
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  getModelInfo: async (context: Context, params: any) => {
    Logger.debug('getNumeraiModelInfo');
    const response = await context.$numerbay.api.getNumeraiModelInfo(params);
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  }
};

export default useNumeraiFactory(factoryParams);
