import { Order } from '../types';
import {UseMakeOrder, useMakeOrderFactory, Context, Logger} from '@vue-storefront/core';

const factoryParams = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  make: async (context: Context, params): Promise<Order> => {
    Logger.debug('makeOrder');
    const { id, optionId, submitModelId } = params;
    const response = await context.$numerbay.api.createOrder({ id, optionId, submitModelId });
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  }
};

const useMakeOrder: () => UseMakeOrder<Order> = useMakeOrderFactory<Order>(factoryParams);

export default useMakeOrder;
