import { Ref, computed } from '@vue/composition-api';
import { Context, FactoryParams, CustomQuery, sharedRef, Logger, configureFactoryParams } from '@vue-storefront/core';
import { UseUserOrder, UseUserOrderErrors } from '../types/composeables';

export interface UseUserOrderFactoryParams<ORDERS, ORDER_SEARCH_PARAMS> extends FactoryParams {
  searchOrders: (context: Context, params: ORDER_SEARCH_PARAMS & { customQuery?: CustomQuery }) => Promise<ORDERS>;
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

    return {
      orders: computed(() => orders.value),
      search,
      loading: computed(() => loading.value),
      error: computed(() => error.value)
    };
  };
}