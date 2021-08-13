import {useShippingFactory, UseShippingParams, Context, Logger} from '@vue-storefront/core';
import { Address } from '../types';

let details = {};

const params: UseShippingParams<Address, any> = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  load: async (context: Context, { customQuery }) => {
    Logger.debug('Mocked: loadShipping');
    return details;
  },

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  save: async (context: Context, { shippingDetails, customQuery }) => {
    Logger.debug('Mocked: saveShipping');
    details = shippingDetails;
    return details;
  }
};

export default useShippingFactory<Address, any>(params);
