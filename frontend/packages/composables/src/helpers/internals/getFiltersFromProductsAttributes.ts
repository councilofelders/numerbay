import { ProductVariant } from '@vue-storefront/numerbay-api';
import {Attribute, Filter, FilterOption} from '../../types';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const extractAttributes = (product: ProductVariant): Attribute[] => [
  {name: 'price', value: product?.price, typename: 'MoneyAttribute'},
  {name: 'rank', value: product?.model?.latest_ranks?.corr, typename: 'NumberAttribute'}
];

const flattenAttributes = (prev: Attribute[], curr: Attribute[]): Attribute[] => prev.concat(curr || []);

const getFilterFromAttribute = (attribute: Attribute, prev) => {
  const attrValue = attribute.value;
  const filter = prev[attribute.name] || {
    type: attribute.typename,
    options: []
  };
  const option: FilterOption = {
    value: attrValue,
    label: (attribute as any).label || (typeof attrValue === 'string' ? attrValue : null),
    selected: false
  };
  const hasSuchOption = filter.options.some(opt => opt.value === option.value);
  hasSuchOption || filter.options.push(option);
  return filter;
};

export default (products: ProductVariant[]): Record<string, Filter> => {
  if (!products) {
    return {};
  }

  return products.map(extractAttributes).reduce(flattenAttributes, []).reduce((prev, attribute) => {
    prev[attribute.name] = getFilterFromAttribute(attribute, prev);
    return prev;
  }, {});
};
