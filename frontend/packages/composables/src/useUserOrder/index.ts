/* istanbul ignore file */

import { Context, Logger } from '@vue-storefront/core';
import { useUserOrderFactory, UseUserOrderFactoryParams } from '../factories/useUserOrderFactory';
import { OrdersResponse, OrderSearchParams } from '../types';

const params: UseUserOrderFactoryParams<OrdersResponse, OrderSearchParams> = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  searchOrders: async (context: Context, params: OrderSearchParams): Promise<OrdersResponse> => {
    Logger.debug('searchOrders');
    return await context.$numerbay.api.getOrder(params);
    // return {
    //   data: [],
    //   total: 0
    // };
  }
};

export default useUserOrderFactory<OrdersResponse, OrderSearchParams>(params);
