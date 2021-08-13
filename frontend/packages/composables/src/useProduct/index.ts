import {Context, Logger, ProductsSearchParams} from '@vue-storefront/core';
import { useProductFactory, UseProductFactoryParams } from '../factories/useProductFactory';
import {ProductsResponse} from '../types';

const params: UseProductFactoryParams<ProductsResponse, any> = {
  productsSearch: async (context: Context, params: ProductsSearchParams): Promise<ProductsResponse> => {
    Logger.debug('getProducts');
    return await context.$numerbay.api.getProduct(params);
  }
};

export default useProductFactory<ProductsResponse, any>(params);
