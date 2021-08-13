import { SearchData } from './../types';

const filterFacets = criteria => f => criteria ? criteria.includes(f) : true;

const createFacetsFromOptions = (facets, filters, filterKey) => {
  const options = facets[filterKey]?.options || [];
  const selectedList = filters && filters[filterKey] ? filters[filterKey] : [];

  return options
    .map(({ label, value }) => ({
      type: 'attribute',
      id: label,
      attrName: filterKey,
      value,
      selected: selectedList.includes(value),
      count: null
    }));
};

export const reduceForFacets = (facets, filters) => (prev, curr) => (
  prev.concat(createFacetsFromOptions(facets, filters, curr))
);

export const reduceForGroupedFacets = (facets, filters) => (prev, curr) => (
  prev.concat([{
    id: curr,
    label: curr,
    options: createFacetsFromOptions(facets, filters, curr),
    count: null
  }])
);

export const buildFacets = (searchData: SearchData, reduceFn, criteria?: string[]) => {
  if (!searchData.data) {
    return [];
  }

  const {
    data: { facets },
    input: { filters }
  } = searchData;

  return Object.keys(facets)
    .filter(filterFacets(criteria))
    .reduce(reduceFn(facets, filters), []);
};
