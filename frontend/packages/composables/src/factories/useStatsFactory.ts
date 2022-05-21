import { computed } from '@vue/composition-api';
import {
  configureFactoryParams,
  Context,
  FactoryParams,
  Logger,
  sharedRef
} from '@vue-storefront/core';
import { UseStats } from '../types/composables';

export interface UseStatsFactoryParams extends FactoryParams{
  getStats: (context: Context) => Promise<any>;
}

export function useStatsFactory(
  factoryParams: UseStatsFactoryParams
) {
  return function useStats(cacheId: string): UseStats {
    const ssrKey = cacheId || 'useStatsFactory';

    const stats = sharedRef({}, `useStats-stats-${ssrKey}`);
    const loading = sharedRef<boolean>(false, `useStats-loading-${ssrKey}`);
    // eslint-disable-next-line @typescript-eslint/naming-convention,no-underscore-dangle
    const _factoryParams = configureFactoryParams(factoryParams);

    const getStats = async (identifer: string) => {
      Logger.debug(`useStats/${ssrKey}/getStats`);

      loading.value = true;

      try {
        stats.value = await _factoryParams.getStats(identifer);
      } catch (err) {
        Logger.error(`useStats/${ssrKey}/getStats`, err);
      } finally {
        loading.value = false;
      }
    };

    return {
      getStats,
      loading: computed(() => loading.value),
      stats: computed(() => stats.value)
    };
  };
}
