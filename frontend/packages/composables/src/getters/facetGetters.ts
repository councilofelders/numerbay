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
  var options = []
  var tournament = null;

  if (searchData?.data) {
    tournament = searchData?.data?.categories[0].tournament
    if (tournament) {  // if is tournament category
      if (tournament === 8) {  // if is Numerai tournament
        options.push(
            { type: 'sort', id: 'rank-best', value: 'TC from high to low', count: null },
            { type: 'sort', id: 'stake-down', value: 'Stake from high to low', count: null },
            { type: 'sort', id: 'return3m-down', value: '3M Return from high to low', count: null },
            { type: 'sort', id: 'return1y-down', value: '1Y Return from high to low', count: null },
            { type: 'sort', id: 'corr-down', value: 'CORR from high to low', count: null },
            { type: 'sort', id: 'corrtc-down', value: 'CORR+TC from high to low', count: null },
            { type: 'sort', id: 'corr2tc-down', value: 'CORR+2xTC from high to low', count: null },
            { type: 'sort', id: 'corr3tc-down', value: 'CORR+3xTC from high to low', count: null },
            { type: 'sort', id: 'corr60-down', value: 'CORJ60 from high to low', count: null },
            { type: 'sort', id: 'fnc-down', value: 'FNC from high to low', count: null },
            { type: 'sort', id: 'fncV3-down', value: 'FNCv3 from high to low', count: null }
        );
      }

      if (tournament === 11) {  // if is Signals tournament
        options.push(
            { type: 'sort', id: 'rank-best', value: 'TC from high to low', count: null },
            { type: 'sort', id: 'stake-down', value: 'Stake from high to low', count: null },
            { type: 'sort', id: 'return3m-down', value: '3M Return from high to low', count: null },
            { type: 'sort', id: 'return1y-down', value: '1Y Return from high to low', count: null },
            { type: 'sort', id: 'corr-down', value: 'CORR from high to low', count: null },
            { type: 'sort', id: 'corrtc-down', value: 'CORR+TC from high to low', count: null },
            { type: 'sort', id: 'corr2tc-down', value: 'CORR+2xTC from high to low', count: null },
            { type: 'sort', id: 'corr60-down', value: 'CORR60 from high to low', count: null },
            { type: 'sort', id: 'ic-down', value: 'IC from high to low', count: null },
        );
      }
    }
  }

  options.push(
      { type: 'sort', id: 'name-up', value: 'Name: A to Z', count: null},
      { type: 'sort', id: 'name-down', value: 'Name: Z to A', count: null},
      { type: 'sort', id: 'sales-down', value: 'Sales from high to low', count: null },
      { type: 'sort', id: 'latest', value: 'Latest', count: null }
  );

  options = options.map(o => ({ ...o, selected: o.id === searchData.input.sort }));
  const selected = options.find(o => o.id === searchData.input.sort)?.id || (tournament ? 'rank-best':'latest');
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
