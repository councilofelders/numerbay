import { SearchData } from './../types';

// const filterFacets = criteria => f => criteria ? criteria.includes(f) : true;

// const createFacetsFromOptions = (facets, filters, filterKey) => {
//   const options = facets[filterKey]?.options || [];
//   const selectedList = filters && filters[filterKey] ? filters[filterKey] : [];
//
//   return options
//     .map(({ label, value }) => ({
//       type: 'attribute',
//       id: label,
//       attrName: filterKey,
//       value,
//       selected: selectedList.includes(value),
//       count: null
//     }));
// };

const getFacetTypeByCode = (code) => {
  if (code === 'rank') {
    return 'range';
  }
  return 'checkbox';
};

const filterFacets = (criteria) => (f) => (criteria ? criteria.includes(f.attribute_code) : true);

const createFacetsFromOptions = (facets, filters, facet) => {
  const options = facet.options || [];
  const selectedList = filters && filters[facet.attribute_code] ? filters[facet.attribute_code] : [];
  return options
    .map(({
      label,
      value,
      count
    }) => ({
      type: getFacetTypeByCode(facet.attribute_code),
      id: label,
      attrName: label,
      value,
      selected: selectedList.includes(value),
      count
    }));
};

export const reduceForFacets = (facets, filters) => (prev, curr) => (
  prev.concat(createFacetsFromOptions(facets, filters, curr))
);

export const reduceForGroupedFacets = (facets, filters) => (prev, curr) => (
  prev.concat([{
    id: curr.attribute_code,
    label: curr.label,
    options: createFacetsFromOptions(facets, filters, curr),
    count: null
  }])
);

export const buildFacets = (searchData: SearchData, reduceFn, criteria?: string[]) => {
  if (!searchData.data) {
    return [];
  }

  const {
    data: { availableFilters: facets },
    input: { filters }
  } = searchData;

  return facets.filter(filterFacets(criteria)).reduce(reduceFn(facets, filters), []);
};
