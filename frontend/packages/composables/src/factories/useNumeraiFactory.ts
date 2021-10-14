import { Ref, computed } from '@vue/composition-api';
import {
  configureFactoryParams,
  Context,
  FactoryParams,
  Logger,
  sharedRef
} from '@vue-storefront/core';
import { UseNumerai, UseNumeraiErrors } from '../types/composables';

export interface UseNumeraiFactoryParams extends FactoryParams{
  getModels: (context: Context) => Promise<any>;
  getModelInfo: (context: Context, params: any) => Promise<any>;
}

export function useNumeraiFactory(
  factoryParams: UseNumeraiFactoryParams
) {
  return function useNumerai(cacheId: string): UseNumerai {
    const ssrKey = cacheId || 'useNumeraiFactory';

    const numerai = sharedRef({}, `useNumerai-numerai-${ssrKey}`);
    const loading = sharedRef<boolean>(false, `useNumerai-loading-${ssrKey}`);
    // eslint-disable-next-line @typescript-eslint/naming-convention,no-underscore-dangle
    const _factoryParams = configureFactoryParams(factoryParams);

    const errorsFactory = (): UseNumeraiErrors => ({
      getModels: null,
      getModelInfo: null
    });

    const error: Ref<UseNumeraiErrors> = sharedRef(errorsFactory(), `useNumerai-error-${ssrKey}`);

    const resetErrorValue = () => {
      error.value = errorsFactory();
    };

    const getModels = async (identifer: string) => {
      // todo more debug logs
      Logger.debug(`useNumerai/${ssrKey}/getModels`);
      resetErrorValue();

      loading.value = true;

      try {
        numerai.value.models = await _factoryParams.getModels(identifer);
        error.value.getModels = null;
      } catch (err) {
        error.value.getModels = err;
        Logger.error(`useNumerai/${ssrKey}/getModels`, err);
      } finally {
        loading.value = false;
      }
    };

    const getModelInfo = async (params: any) => {
      Logger.debug(`useNumerai/${ssrKey}/getModelInfo`);
      resetErrorValue();

      loading.value = true;

      try {
        numerai.value.modelInfo = await _factoryParams.getModelInfo(params);
        error.value.getModelInfo = null;
      } catch (err) {
        error.value.getModelInfo = err;
        Logger.error(`useNumerai/${ssrKey}/getModels`, err);
      } finally {
        loading.value = false;
      }
    };

    return {
      getModels,
      getModelInfo,
      loading: computed(() => loading.value),
      numerai: computed(() => numerai.value),
      error: computed(() => error.value)
    };
  };
}
