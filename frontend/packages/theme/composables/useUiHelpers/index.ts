import { Logger } from '@vue-storefront/core';
import { getInstance } from '../../helpers/hooks/getInstance';

const nonFilters = ['page', 'sort', 'phrase', 'itemsPerPage'];

const reduceFilters = (query) => (prev, curr) => {
  const makeArray = Array.isArray(query[curr]) || nonFilters.includes(curr);

  return {
    ...prev,
    [curr]: makeArray ? query[curr] : [query[curr]]
  };
};

const getFiltersDataFromUrl = (context, onlyFilters) => {
  const { query } = context.$router.history.current;
  // Always only show active products if not specified
  if (!query?.status) {
    query.status = ['active']
  }
  return Object.keys(query)
    .filter(f => onlyFilters ? !nonFilters.includes(f) : nonFilters.includes(f))
    .reduce(reduceFilters(query), {});
};

const useUiHelpers = () => {
  const instance = getInstance();
  const getFacetsFromURL = () => {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    const { query, params } = instance.$router.history.current;
    const categorySlug = Object.keys(params).reduce((prev, curr) => params[curr] || prev, params.slug_1);

    return {
      rootCatSlug: params.slug_1,
      categorySlug,
      page: parseInt(query.page, 10) || 1,
      sort: query.sort,
      filters: getFiltersDataFromUrl(instance, true),
      itemsPerPage: parseInt(query.itemsPerPage, 10) || 20,
      term: query.term
    };
  };

  // eslint-disable-next-line
  const getCatLink = (category): string => {
    return `/explore/${category.slug}`;
  };

  // eslint-disable-next-line
  const changeSorting = (sort) => {
    // eslint-disable-next-line
    // @ts-ignore
    const { query } = instance.$router.history.current;
    instance.$router.push({ query: { ...query, sort } });
  };

  // eslint-disable-next-line
  const changeFilters = (filters) => {
    const reducedFilters = Object.keys(filters).reduce((acc, elem) => {
      if (filters[elem]?.length >0) acc[elem] = filters[elem]
      return acc
    }, {});
    instance.$router.push({
      query: {
        ...getFiltersDataFromUrl(instance, false),
        ...reducedFilters
      }
    });
  };

  // eslint-disable-next-line
  const changeItemsPerPage = (itemsPerPage) => {
    Logger.warn('[VSF] please implement useUiHelpers.changeItemsPerPage.');
  };

  // eslint-disable-next-line
  const setTermForUrl = (term: string) => {
    Logger.warn('[VSF] please implement useUiHelpers.changeSearchTerm.');
  };

  // eslint-disable-next-line
  const isFacetCheckbox = (facet): boolean => {
    return facet.id === 'platform' || facet.id === 'status';
  };

  const getSearchTermFromUrl = () => {
    Logger.warn('[VSF] please implement useUiHelpers.getSearchTermFromUrl.');
  };

  return {
    getFacetsFromURL,
    getCatLink,
    changeSorting,
    changeFilters,
    changeItemsPerPage,
    setTermForUrl,
    isFacetCheckbox,
    getSearchTermFromUrl
  };
};

export default useUiHelpers;
