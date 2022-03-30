import {
  AgnosticBreadcrumb,
  AgnosticCategoryTree,
  AgnosticFacet,
  AgnosticGroupedFacet,
  AgnosticPagination,
  AgnosticSort,
  FacetsGetters
} from '@vue-storefront/core';
import { buildFacets, reduceForGroupedFacets } from '../useFacet/_utils';
import { getCategoryTree as buildCategoryTree } from './categoryGetters';
import { getProductFiltered } from './productGetters';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const getAll = (searchData, criteria?: string[]): AgnosticFacet[] => [];

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const getGrouped = (searchData, criteria?: string[]): AgnosticGroupedFacet[] => buildFacets(searchData, reduceForGroupedFacets, criteria);

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const getSortOptions = (searchData): AgnosticSort => {
  const options = [
    { type: 'sort', id: 'rank-best', value: 'Rank from top to bottom', count: null },
    // { type: 'sort', id: 'rank-worst', value: 'Rank from worst to best', count: null },
    { type: 'sort', id: 'stake-down', value: 'Stake from high to low', count: null },
    // { type: 'sort', id: 'stake-up', value: 'Stake from low to high', count: null },
    { type: 'sort', id: 'return3m-down', value: '3M Return from high to low', count: null },
    // { type: 'sort', id: 'return3m-up', value: '3M Return from low to high', count: null },
    { type: 'sort', id: 'mmc-down', value: 'MMC Rep from high to low', count: null },
    { type: 'sort', id: 'corrmmc-down', value: 'CORR+MMC Rep from high to low', count: null },
    { type: 'sort', id: 'corr2mmc-down', value: 'CORR+2xMMC Rep from high to low', count: null },
    { type: 'sort', id: 'fnc-down', value: 'FNC Rep from high to low', count: null },
    { type: 'sort', id: 'fncV3-down', value: 'FNCv3 Rep from high to low', count: null },
    { type: 'sort', id: 'tc-down', value: 'TC Rep from high to low', count: null },
    { type: 'sort', id: 'name-up', value: 'Name: A to Z', count: null},
    // { type: 'sort', id: 'price-up', value: 'Price from low to high', count: null },
    // { type: 'sort', id: 'price-down', value: 'Price from high to low', count: null },
    { type: 'sort', id: 'name-down', value: 'Name: Z to A', count: null},
    { type: 'sort', id: 'latest', value: 'Latest', count: null }
  ].map(o => ({ ...o, selected: o.id === searchData.input.sort }));

  const selected = options.find(o => o.id === searchData.input.sort)?.id || 'rank-best';

  return { options, selected };
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const getCategoryTree = (searchData): AgnosticCategoryTree => {
  if (!searchData.data?.categories) {
    return {} as any;
  }
  return buildCategoryTree(searchData.data.categories[0]);
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const getProducts = (searchData): any => {
  return getProductFiltered(searchData.data?.products || [], { master: true });
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const getPagination = (searchData): AgnosticPagination => ({
  currentPage: searchData.input?.page || 1,
  totalPages: (searchData.data) ? Math.ceil(searchData.data.total / searchData.input.itemsPerPage) : 0,
  totalItems: (searchData.data) ? searchData.data.total : 0,
  itemsPerPage: searchData.input?.itemsPerPage || 20,
  pageOptions: [10, 50, 100]
});

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const getBreadcrumbs = (searchData): AgnosticBreadcrumb[] => [];

const facetGetters: FacetsGetters<any, any> = {
  getSortOptions,
  getGrouped,
  getAll,
  getProducts,
  getCategoryTree,
  getBreadcrumbs,
  getPagination
};

export default facetGetters;
