import {Context, Logger} from '@vue-storefront/core';
import { useStatsFactory, UseStatsFactoryParams } from '../factories/useStatsFactory';

const factoryParams: UseStatsFactoryParams = {
  getStats: async (context: Context) => {
    Logger.debug('getStats');
    const response = await context.$numerbay.api.getStats();
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  }
};

export default useStatsFactory(factoryParams);
