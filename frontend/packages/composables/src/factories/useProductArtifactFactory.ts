import { Ref, computed } from '@vue/composition-api';
import { Context, FactoryParams, CustomQuery, sharedRef, Logger, configureFactoryParams } from '@vue-storefront/core';
import {UseProductArtifact, UseProductArtifactErrors} from '../types/composables';

export interface UseProductArtifactFactoryParams<ARTIFACTS, ARTIFACT_SEARCH_PARAMS> extends FactoryParams {
  searchArtifacts: (context: Context, params: ARTIFACT_SEARCH_PARAMS & { customQuery?: CustomQuery }) => Promise<ARTIFACTS>;
  downloadArtifact: (context: Context, params: any) => Promise<any>;
  submitArtifact: (context: Context, params: any) => Promise<any>;
  deleteArtifact: (context: Context, params: any) => Promise<any>;
}

export function useProductArtifactFactory<ARTIFACTS, ARTIFACT_SEARCH_PARAMS>(factoryParams: UseProductArtifactFactoryParams<ARTIFACTS, ARTIFACT_SEARCH_PARAMS>) {
  return function useProductArtifact(cacheId: string): UseProductArtifact<ARTIFACTS, ARTIFACT_SEARCH_PARAMS> {
    const ssrKey = cacheId || 'useProductArtifactFactory';
    const artifacts: Ref<ARTIFACTS> = sharedRef(null, `useProductArtifact-artifacts-${ssrKey}`);
    const loading: Ref<boolean> = sharedRef(false, `useProductArtifact-loading-${ssrKey}`);
    const _factoryParams = configureFactoryParams(factoryParams);
    const errorsFactory = (): UseProductArtifactErrors => ({
      search: null,
      downloadArtifact: null,
      submitArtifact: null,
      deleteArtifact: null
    });
    const error: Ref<UseProductArtifactErrors> = sharedRef(errorsFactory(), `useProductArtifact-error-${ssrKey}`);
    const resetErrorValue = () => {
      error.value = errorsFactory();
    };

    const search = async (searchParams): Promise<void> => {
      Logger.debug(`useProductArtifact/${ssrKey}/search`, searchParams);

      try {
        loading.value = true;
        artifacts.value = await _factoryParams.searchArtifacts(searchParams);
        error.value.search = null;
      } catch (err) {
        error.value.search = err;
        Logger.error(`useProductArtifact/${ssrKey}/search`, err);
      } finally {
        loading.value = false;
      }
    };

    const downloadArtifact = async ({productId, artifactId}) => {
      Logger.debug(`useProductArtifactFactory.downloadArtifact ${productId}/${artifactId}`);
      resetErrorValue();

      let downloadUrl = null;
      try {
        loading.value = true;
        downloadUrl = await _factoryParams.downloadArtifact({productId, artifactId});
        error.value.downloadArtifact = null;
      } catch (err) {
        error.value.downloadArtifact = err;
        Logger.error('useProductArtifact/downloadArtifact', err);
      } finally {
        loading.value = false;
      }
      return downloadUrl;
    };

    const submitArtifact = async ({orderId, artifactId}) => {
      Logger.debug(`useProductArtifactFactory.submitArtifact ${orderId}/${artifactId}`);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.submitArtifact({orderId, artifactId});
        error.value.submitArtifact = null;
      } catch (err) {
        error.value.submitArtifact = err;
        Logger.error('useProductArtifact/submitArtifact', err);
      } finally {
        loading.value = false;
      }
    };

    const deleteArtifact = async ({productId, artifactId}) => {
      Logger.debug(`useProductArtifactFactory.deleteArtifact ${productId}/${artifactId}`);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.deleteArtifact({productId, artifactId});
        error.value.deleteArtifact = null;
      } catch (err) {
        error.value.deleteArtifact = err;
        Logger.error('useProductArtifact/deleteArtifact', err);
      } finally {
        loading.value = false;
      }
    };

    return {
      search,
      downloadArtifact,
      submitArtifact,
      deleteArtifact,
      artifacts: computed(() => artifacts.value),
      loading: computed(() => loading.value),
      error: computed(() => error.value)
    };
  };
}
