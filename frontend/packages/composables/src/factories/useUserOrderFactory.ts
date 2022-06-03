import { Ref, computed } from '@vue/composition-api';
import { Context, FactoryParams, CustomQuery, sharedRef, Logger, configureFactoryParams } from '@vue-storefront/core';
import { UseUserOrder, UseUserOrderErrors } from '../types/composables';

export interface UseUserOrderFactoryParams<ORDERS, ORDER_SEARCH_PARAMS> extends FactoryParams {
  searchOrders: (context: Context, params: ORDER_SEARCH_PARAMS & { customQuery?: CustomQuery }) => Promise<ORDERS>;
  validatePayment: (context: Context, params: any) => Promise<any>;
  cancelOrder: (context: Context, params: any) => Promise<any>;
}

export function useUserOrderFactory<ORDERS, ORDER_SEARCH_PARAMS>(factoryParams: UseUserOrderFactoryParams<ORDERS, ORDER_SEARCH_PARAMS>) {
  return function useUserOrder(cacheId: string): UseUserOrder<ORDERS, ORDER_SEARCH_PARAMS> {
    const ssrKey = cacheId || 'useUserOrderFactory';
    const orders: Ref<ORDERS> = sharedRef([], `useUserOrder-orders-${ssrKey}`);
    const loading: Ref<boolean> = sharedRef(false, `useUserOrder-loading-${ssrKey}`);
    const _factoryParams = configureFactoryParams(factoryParams);
    const error: Ref<UseUserOrderErrors> = sharedRef({}, `useUserOrder-error-${ssrKey}`);

    const search = async (searchParams): Promise<void> => {
      Logger.debug(`useUserOrder/${ssrKey}/search`, searchParams);

      try {
        loading.value = true;
        orders.value = await _factoryParams.searchOrders(searchParams);
        error.value.search = null;
      } catch (err) {
        error.value.search = err;
        Logger.error(`useUserOrder/${ssrKey}/search`, err);
      } finally {
        loading.value = false;
      }
    };

    const validatePayment = async ({orderId, transactionHash}) => {
      Logger.debug(`useUserOrderFactory.validatePayment ${orderId}/${transactionHash}`);

      try {
        loading.value = true;
        await _factoryParams.validatePayment({orderId, transactionHash});
        error.value.validatePayment = null;
      } catch (err) {
        error.value.validatePayment = err;
        Logger.error(`useUserOrder/${ssrKey}/validatePayment`, err);
      } finally {
        loading.value = false;
      }
    };

    const cancelOrder = async ({orderId}) => {
      Logger.debug(`useUserOrderFactory.cancelOrder ${orderId}`);

      try {
        loading.value = true;
        await _factoryParams.cancelOrder({orderId});
        error.value.cancelOrder = null;
      } catch (err) {
        error.value.cancelOrder = err;
        Logger.error(`useUserOrder/${ssrKey}/cancelOrder`, err);
      } finally {
        loading.value = false;
      }
    };

    return {
      orders: computed(() => orders.value),
      search,
      validatePayment,
      cancelOrder,
      loading: computed(() => loading.value),
      error: computed(() => error.value)
    };
  };
}
