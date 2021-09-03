import {Context, Logger} from '@vue-storefront/core';
import { useGlobalsFactory, UseGlobalsFactoryParams } from '../factories/useGlobalsFactory';

const factoryParams: UseGlobalsFactoryParams = {
  getGlobals: async (context: Context) => {
    Logger.debug('getGlobals');
    const response = await context.$numerbay.api.getGlobals();
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  }
};

export default useGlobalsFactory(factoryParams);
