import { computed } from '@vue/composition-api';
import {
  configureFactoryParams,
  Context,
  FactoryParams,
  Logger,
  sharedRef
} from '@vue-storefront/core';
import { UseNumerai } from '../types/composeables';

export interface UseNumeraiFactoryParams extends FactoryParams{
  getModels: (context: Context) => Promise<any>;
  getModelInfo: (context: Context, params: any) => Promise<any>;
}

export function useNumeraiFactory(
  factoryParams: UseNumeraiFactoryParams,
) {
  return function useNumerai(cacheId: string): UseNumerai {
    const ssrKey = cacheId || 'useNumeraiFactory';

    const numerai = sharedRef({}, `useNumerai-numerai-${ssrKey}`);
    const loading = sharedRef<boolean>(false, `useNumerai-loading-${ssrKey}`);
    // eslint-disable-next-line @typescript-eslint/naming-convention,no-underscore-dangle
    const _factoryParams = configureFactoryParams(factoryParams);

    const getModels = async (identifer: string) => {
      // todo more debug logs
      Logger.debug(`useNumerai/${ssrKey}/getModels`);
      loading.value = true;

      try {
        numerai.value.models = await _factoryParams.getModels(identifer);
      } finally {
        loading.value = false;
      }
    };

    const getModelInfo = async (params: any) => {
      Logger.debug(`useNumerai/${ssrKey}/getModelInfo`);
      loading.value = true;

      try {
        numerai.value.modelInfo = await _factoryParams.getModelInfo(params);
      } finally {
        loading.value = false;
      }
    };

    return {
      getModels,
      getModelInfo,
      loading: computed(() => loading.value),
      numerai: computed(() => numerai.value)
    };
  };
}
