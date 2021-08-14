import {Context, Logger, ProductsSearchParams} from '@vue-storefront/core';
import { useProductFactory, UseProductFactoryParams } from '../factories/useProductFactory';
import {ProductsResponse} from '../types';

const params: UseProductFactoryParams<ProductsResponse, any> = {
  productsSearch: async (context: Context, params: ProductsSearchParams): Promise<ProductsResponse> => {
    Logger.debug('getProducts');
    return await context.$numerbay.api.getProduct(params);
  },

  createProduct: async (context: Context, {product}) => {
    Logger.debug('createProduct');
    const response = await context.$numerbay.api.createProduct(product);
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  updateProduct: async (context: Context, {id, product}) => {
    Logger.debug('updateProduct');
    product.id = id;
    const response = await context.$numerbay.api.updateProduct(product);
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  deleteProduct: async (context: Context, {id}) => {
    Logger.debug('deleteProduct');
    const response = await context.$numerbay.api.deleteProduct({id});
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  }
};

export default useProductFactory<ProductsResponse, any>(params);
