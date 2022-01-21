import { Context, CustomQuery, FactoryParams, Logger, configureFactoryParams, sharedRef } from '@vue-storefront/core';
import { Ref, computed } from '@vue/composition-api';
import { UseOrderArtifact, UseOrderArtifactErrors } from '../types/composables';

export interface UseOrderArtifactFactoryParams<ARTIFACTS, ARTIFACT_SEARCH_PARAMS> extends FactoryParams {
  searchArtifacts: (context: Context, params: ARTIFACT_SEARCH_PARAMS & { customQuery?: CustomQuery }) => Promise<ARTIFACTS>;
  downloadArtifact: (context: Context, params: any) => Promise<any>;
  submitArtifact: (context: Context, params: any) => Promise<any>;
  createArtifact: (context: Context, params: any) => Promise<any>;
  updateArtifact: (context: Context, params: any) => Promise<any>;
  deleteArtifact: (context: Context, params: any) => Promise<any>;
}

export function useOrderArtifactFactory<ARTIFACTS, ARTIFACT_SEARCH_PARAMS>(factoryParams: UseOrderArtifactFactoryParams<ARTIFACTS, ARTIFACT_SEARCH_PARAMS>) {
  return function useOrderArtifact(cacheId: string): UseOrderArtifact<ARTIFACTS, ARTIFACT_SEARCH_PARAMS> {
    const ssrKey = cacheId || 'useOrderArtifactFactory';
    const artifacts: Ref<ARTIFACTS> = sharedRef(null, `useOrderArtifact-artifacts-${ssrKey}`);
    const loading: Ref<boolean> = sharedRef(false, `useOrderArtifact-loading-${ssrKey}`);
    const _factoryParams = configureFactoryParams(factoryParams);
    const errorsFactory = (): UseOrderArtifactErrors => ({
      search: null,
      downloadArtifact: null,
      submitArtifact: null,
      createArtifact: null,
      updateArtifact: null,
      deleteArtifact: null
    });
    const error: Ref<UseOrderArtifactErrors> = sharedRef(errorsFactory(), `useOrderArtifact-error-${ssrKey}`);
    const resetErrorValue = () => {
      error.value = errorsFactory();
    };

    const search = async (searchParams): Promise<void> => {
      Logger.debug(`useOrderArtifact/${ssrKey}/search`, searchParams);

      try {
        loading.value = true;
        artifacts.value = await _factoryParams.searchArtifacts(searchParams);
        error.value.search = null;
      } catch (err) {
        error.value.search = err;
        Logger.error(`useOrderArtifact/${ssrKey}/search`, err);
      } finally {
        loading.value = false;
      }
    };

    const downloadArtifact = async ({productId, artifactId}) => {
      Logger.debug(`useOrderArtifactFactory.downloadArtifact ${productId}/${artifactId}`);
      resetErrorValue();

      let downloadUrl = null;
      try {
        loading.value = true;
        downloadUrl = await _factoryParams.downloadArtifact({productId, artifactId});
        error.value.downloadArtifact = null;
      } catch (err) {
        error.value.downloadArtifact = err;
        Logger.error('useOrderArtifact/downloadArtifact', err);
      } finally {
        loading.value = false;
      }
      return downloadUrl;
    };

    const submitArtifact = async ({orderId, artifactId}) => {
      Logger.debug(`useOrderArtifactFactory.submitArtifact ${orderId}/${artifactId}`);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.submitArtifact({orderId, artifactId});
        error.value.submitArtifact = null;
      } catch (err) {
        error.value.submitArtifact = err;
        Logger.error('useOrderArtifact/submitArtifact', err);
      } finally {
        loading.value = false;
      }
    };

    const createArtifact = async ({productId, artifact: providedArtifact}) => {
      Logger.debug('useOrderArtifactFactory.createArtifact', productId, providedArtifact);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.createArtifact({productId, artifact: providedArtifact});
        error.value.createArtifact = null;
      } catch (err) {
        error.value.createArtifact = err;
        Logger.error('useOrderArtifact/createArtifact', err);
      } finally {
        loading.value = false;
      }
    };

    const updateArtifact = async ({productId, artifactId, description}) => {
      Logger.debug('useOrderArtifactFactory.updateArtifact', productId, artifactId, description);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.updateArtifact({productId, artifactId, description});
        error.value.updateArtifact = null;
      } catch (err) {
        error.value.updateArtifact = err;
        Logger.error('useOrderArtifact/updateArtifact', JSON.stringify(err));
      } finally {
        loading.value = false;
      }
    };

    const deleteArtifact = async ({productId, artifactId}) => {
      Logger.debug(`useOrderArtifactFactory.deleteArtifact ${productId}/${artifactId}`);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.deleteArtifact({productId, artifactId});
        error.value.deleteArtifact = null;
      } catch (err) {
        error.value.deleteArtifact = err;
        Logger.error('useOrderArtifact/deleteArtifact', err);
      } finally {
        loading.value = false;
      }
    };

    return {
      search,
      downloadArtifact,
      submitArtifact,
      createArtifact,
      updateArtifact,
      deleteArtifact,
      artifacts: computed(() => artifacts.value),
      loading: computed(() => loading.value),
      error: computed(() => error.value)
    };
  };
}
