import { CustomQuery, ProductsSearchParams, Context, FactoryParams } from '@vue-storefront/core';
import { Ref, computed } from '@vue/composition-api';
import { sharedRef, Logger, configureFactoryParams } from '@vue-storefront/core';
import { UseProduct, UseProductErrors } from '../types/composeables';

export interface UseProductFactoryParams<PRODUCTS, PRODUCT_SEARCH_PARAMS extends ProductsSearchParams> extends FactoryParams {
  productsSearch: (context: Context, params: PRODUCT_SEARCH_PARAMS & { customQuery?: CustomQuery }) => Promise<PRODUCTS>;
  createProduct: (context: Context, params: any) => Promise<any>;
  updateProduct: (context: Context, params: any) => Promise<any>;
  deleteProduct: (context: Context, params: any) => Promise<any>;
}

export function useProductFactory<PRODUCTS, PRODUCT_SEARCH_PARAMS>(
  factoryParams: UseProductFactoryParams<PRODUCTS, PRODUCT_SEARCH_PARAMS>
) {
  return function useProduct(id: string): UseProduct<PRODUCTS, PRODUCT_SEARCH_PARAMS> {
    const products: Ref<PRODUCTS> = sharedRef([], `useProduct-products-${id}`);
    const loading = sharedRef(false, `useProduct-loading-${id}`);
    const _factoryParams = configureFactoryParams(factoryParams);

    const errorsFactory = (): UseProductErrors => ({
      search: null,
      listingModal: null
    });

    const error: Ref<UseProductErrors> = sharedRef(errorsFactory(), `useProduct-error-${id}`);

    const resetErrorValue = () => {
      error.value = errorsFactory();
    };

    const search = async (searchParams) => {
      Logger.debug(`useProduct/${id}/search`, searchParams);

      try {
        loading.value = true;
        products.value = await _factoryParams.productsSearch(searchParams);
        error.value.search = null;
      } catch (err) {
        error.value.search = err;
        Logger.error(`useProduct/${id}/search`, err);
      } finally {
        loading.value = false;
      }
    };

    const createProduct = async ({product: providedProduct}) => {
      Logger.debug('useProductFactory.createProduct', providedProduct);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.createProduct({product: providedProduct});
        error.value.listingModal = null;
      } catch (err) {
        error.value.listingModal = err;
        Logger.error('useProduct/createProduct', err);
      } finally {
        loading.value = false;
      }
    };

    const updateProduct = async ({id, product: providedProduct}) => {
      Logger.debug('useProductFactory.updateProduct', providedProduct);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.updateProduct({id, product: providedProduct});
        error.value.listingModal = null;
      } catch (err) {
        error.value.listingModal = err;
        Logger.error('useProduct/updateProduct', JSON.stringify(err));
      } finally {
        loading.value = false;
      }
    };

    const deleteProduct = async ({id}) => {
      Logger.debug('useProductFactory.deleteProduct', id);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.deleteProduct({id});
        error.value.listingModal = null;
      } catch (err) {
        error.value.listingModal = err;
        Logger.error('useProduct/deleteProduct', err);
      } finally {
        loading.value = false;
      }
    };

    return {
      search,
      createProduct,
      updateProduct,
      deleteProduct,
      products: computed(() => products.value),
      loading: computed(() => loading.value),
      error: computed(() => error.value)
    };
  };
}
