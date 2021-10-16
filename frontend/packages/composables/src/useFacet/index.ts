import {Context, useFacetFactory, FacetSearchResult, Logger} from '@vue-storefront/core';
import {ProductVariant} from '@vue-storefront/numerbay-api';
// import getFiltersFromProductsAttributes from '../helpers/internals/getFiltersFromProductsAttributes';

// TODO: move to the config file
const ITEMS_PER_PAGE = [20, 40, 100];

// eslint-disable-next-line @typescript-eslint/ban-types
const constructFilterObject = (inputFilters: Object) => {
  const filter = {};

  Object.keys(inputFilters).forEach((key) => {
    if (key === 'price') {
      const price = { from: 0, to: 0 };
      const flatPrices = inputFilters[key].flatMap((inputFilter) => inputFilter.split('_')).sort();

      [price.from] = flatPrices;
      price.to = flatPrices[flatPrices.length - 1];

      filter[key] = price;
    } else if (typeof inputFilters[key] === 'string') {
      filter[key] = { in: [inputFilters[key]] };
    } else {
      filter[key] = { in: inputFilters[key] };
    }
  });

  return filter;
};

const factoryParams = {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  search: async (context: Context, params: FacetSearchResult<any>) => {
    Logger.debug('searchFacet');
    const itemsPerPage = params.input.itemsPerPage;
    const categories = await context.$numerbay.api.getCategory({ slug: params.input.categorySlug });
    const inputFilters = (params.input.filters) ? params.input.filters : {};

    const filters = {
      ...constructFilterObject({
        ...inputFilters
      })
    };
    const productResponse = await context.$numerbay.api.getProduct({
      catId: categories[0].id,
      limit: itemsPerPage,
      offset: (params.input.page - 1) * itemsPerPage,
      filters,
      term: params.input.term,
      sort: params.input.sort
    });
    const products = productResponse?.data as ProductVariant[] || [];
    const availableFilters = productResponse?.aggregations;
    // const facets = getFiltersFromProductsAttributes(products);
    // const facets = null;

    return {
      products,
      categories,
      availableFilters,
      total: productResponse?.total,
      perPageOptions: ITEMS_PER_PAGE,
      itemsPerPage
    };
  }
};

export default useFacetFactory<any>(factoryParams);
