import { Order } from '../types';
import {UseMakeOrder, useMakeOrderFactory, Context, Logger} from '@vue-storefront/core';

const factoryParams = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  make: async (context: Context, { customQuery }): Promise<Order> => {
    Logger.debug('Mocked: makeOrder');
    return {
      id: '123-456-7890'
    };
  }
};

const useMakeOrder: () => UseMakeOrder<Order> = useMakeOrderFactory<Order>(factoryParams);

export default useMakeOrder;
