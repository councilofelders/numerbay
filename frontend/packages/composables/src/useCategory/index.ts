import {
  Context, Logger,
  useCategoryFactory,
  UseCategoryFactoryParams
} from '@vue-storefront/core';
import { Category } from '../types';

const params: UseCategoryFactoryParams<Category, any> = {
  categorySearch: async (context: Context, params) => {
    Logger.debug('categorySearch');
    const { ...searchParams } = params;

    return await context.$numerbay.api.getCategory(searchParams);
  }
};

export default useCategoryFactory<Category, any>(params);
