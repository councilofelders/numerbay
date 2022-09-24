import { computed } from '@vue/composition-api';
import {
  configureFactoryParams,
  Context,
  FactoryParams,
  Logger,
  sharedRef
} from '@vue-storefront/core';
import { UseGlobals } from '../types/composables';

export interface UseGlobalsFactoryParams extends FactoryParams{
  getGlobals: (context: Context) => Promise<any>;
}

export function useGlobalsFactory(
  factoryParams: UseGlobalsFactoryParams
) {
  return function useGlobals(cacheId: string): UseGlobals {
    const ssrKey = cacheId || 'useGlobalsFactory';

    const globals = sharedRef({}, `useGlobals-globals-${ssrKey}`);
    const loading = sharedRef<boolean>(false, `useGlobals-loading-${ssrKey}`);
    // eslint-disable-next-line @typescript-eslint/naming-convention,no-underscore-dangle
    const _factoryParams = configureFactoryParams(factoryParams);

    const load = async (identifer: string) => {
      Logger.debug(`useGlobals/${ssrKey}/getGlobals`);

      loading.value = true;

      try {
        globals.value = await _factoryParams.getGlobals(identifer);
      } catch (err) {
        Logger.error(`useGlobals/${ssrKey}/getModels`, err);
      } finally {
        loading.value = false;
      }
    };

    return {
      load,
      loading: computed(() => loading.value),
      globals: computed(() => globals.value)
    };
  };
}
