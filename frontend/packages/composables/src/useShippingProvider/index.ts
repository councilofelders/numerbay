import {useShippingProviderFactory, UseShippingProviderParams, Context, Logger} from '@vue-storefront/core';
import { Shipping, ShippingMethod } from '../types';

let provider = {};

const params: UseShippingProviderParams<Shipping, ShippingMethod> = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  load: async (context: Context, { customQuery }) => {
    Logger.debug('Mocked: loadShippingProvider');

    return provider;
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  save: async (context: Context, { shippingMethod, customQuery }) => {
    Logger.debug('Mocked: saveShippingProvider');
    provider = shippingMethod;
    return provider;
  }
};

export default useShippingProviderFactory<Shipping, ShippingMethod>(params);
