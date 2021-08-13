import {Context, Logger} from '@vue-storefront/core';
import { useNumeraiFactory, UseNumeraiFactoryParams } from '../factories/useNumeraiFactory';

const factoryParams: UseNumeraiFactoryParams = {
  getModels: async (context: Context) => {
    Logger.debug('getNumeraiModels');
    try {
      const response = await context.$numerbay.api.getNumeraiModels();
      return response;
    } catch (e) {
      return null;
    }
  },

  getModelInfo: async (context: Context, params: any) => {
    Logger.debug('getNumeraiModelInfo');
    try {
      const response = await context.$numerbay.api.getNumeraiModelInfo(params);
      return response;
    } catch (e) {
      return null;
    }
  }
};

export default useNumeraiFactory(factoryParams);
