<template>
  <section class="explore-section pt-4  section-space">
    <div class="container">
      <!-- filter -->
      <div class="filter-box pb-5">
        <div class="filter-box-filter justify-content-between align-items-center">
          <div class="filter-box-filter-item">
            <v-select v-model="selectedSortBy" :clearable=false :options="sortBy.options"
                      class="generic-select generic-select-s2" label="value" @input="onChangeSorting"></v-select>
          </div><!-- end filter-box-filter-item -->
          <div class="filter-box-filter-item filter-btn-wrap">
            <button :class="isFilterSidebarOpen ? 'text-primary':''" class="icon-btn icon-btn-s1"
                    @click="toggleFilterSidebar"><em class="ni ni-filter"></em></button>
          </div><!-- end filter-box-filter-item -->
          <div class="filter-box-filter-item ms-lg-auto filter-btn-wrap">
            <div class="filter-btn-group">
              <div v-for="subcategory in getSubcategories(categoryTree)" :key="subcategory.id"
                   class="menu-item d-inline-block">
                <a :class="getActiveClass(subcategory.id)" class="btn filter-btn"
                   href="javascript:void(0);"
                   @click.prevent="activeId = subcategory.id">{{ subcategory.label }}
                </a>
                <div class="menu-sub" style="z-index: 10000;">
                  <ul class="menu-list">
                    <li v-for="subsubcategory in getSubcategories(subcategory)" class="menu-item">
                      <nuxt-link :to="localePath(th.getCatLink(subsubcategory))" class="menu-link">
                        {{ subsubcategory.label }}
                      </nuxt-link>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div><!-- end filter-box-filter-item -->
        </div><!-- end filter-box-filter -->
        <transition name="fade">
          <div v-show="isFilterSidebarOpen" class="justify-content-between align-items-center mt-2 filter-btn-wrap">
            <div class="row">
              <div class="col-9">
                <div class="row">
                  <div v-for="(facet, i) in facets" :key="i" class="col-4">
                    <h5>{{ facet.label }}</h5>
                    <div
                      v-if="isFacetCheckbox(facet)"
                      :key="`${facet.id}-colors`"
                      class="d-flex"
                    >
                      <div v-for="option in facet.options" :key="`${facet.id}-${option.value}`" class="d-flex me-2">
                        <input :id="`${facet.id}-${option.value}`" :checked="isFilterSelected(facet, option)" class="form-check-input me-1"
                               type="checkbox" @change="() => selectFilter(facet, option)">
                        <label :for="`${facet.id}-${option.value}`" class="form-check-label form-check-label-s1">
                          {{ option.id + `${option.count ? ` (${option.count})` : ''}` }} </label>
                      </div>
                    </div>
                    <div v-else>
                      <Range
                        :id="facet.id"
                        :config='{
                      "start":[getRangeFilterOption(facet.options, "from"), getRangeFilterOption(facet.options, "to")],
                      "range":{
                        "min":getRangeFilterOption(facet.options, "from"),
                        "max":getRangeFilterOption(facet.options, "to")
                      },"step":getRangeFilterOption(facet.options, "step"),"connect":true,"direction":"ltr",
                      "orientation":"horizontal","behaviour":"tap-drag","tooltips":true,"keyboardSupport":true,
                      format: {
                        to: (v) => parseFloat(parseFloat(v).toFixed(getRangeFilterOption(facet.options, "decimals"))),
                        from: (v) => parseFloat(parseFloat(v).toFixed(getRangeFilterOption(facet.options, "decimals")))
                      }
                    }'
                        :disabled="false"
                        :value="getSelectedRangeFilterValue(facet)"
                        class="form-range"
                        @change="(values) => updateRangeFilter(facet, values)"
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-3">
                <div class="float-end">
                  <button class="btn btn-dark" @click="applyFilters">Apply</button>
                  <button class="btn filter-btn" @click="clearFilters">Clear</button>
                </div>
              </div>
            </div>
          </div><!-- end filter-box-filter -->
        </transition>
      </div><!-- end filter-box -->
      <!-- Product -->
      <div v-if="loading" class="row g-gs">
        <div v-for="index in pagination.itemsPerPage" :key="index" class="col-lg-6">
          <div class="card card-full flex-sm-row product-s2">
            <div class="card-image">
              <img alt="avatar image" class="product-img" src="https://numer.ai/img/profile_picture_light.jpg">
            </div>
            <div class="card-body card-justified p-4">
              <h5 class="card-title text-truncate mb-0 placeholder-glow"><span class="placeholder col-8"></span></h5>
              <div class="card-author d-flex align-items-center justify-content-between placeholder-glow"><span
                class="placeholder col-6"></span></div>
              <div style="vertical-align: bottom">
                <hr>
                <div class="card-price-wrap d-flex align-items-center justify-content-between">
                  <div class="me-5 me-sm-2 placeholder-glow">
                    <span class="card-price-title">Price</span>
                    <span class="card-price-number placeholder col-12"></span>
                  </div>
                  <span class="btn btn-sm btn-dark disabled placeholder col-3"></span>
                </div><!-- end card-price-wrap -->
              </div>
            </div><!-- end card-body -->
            <a class="details"></a>
          </div><!-- end card -->
        </div>
      </div><!-- end placeholder row -->
      <div v-else class="row g-gs">
        <div v-for="product in products" :key="product.id" class="col-lg-6">
          <ProductCard :product="product"></ProductCard>
        </div>
      </div><!-- end row -->
      <!-- pagination -->
      <div class="text-center mt-4 mt-md-5">
        <Pagination v-if="pagination.totalItems" v-model="page" :per-page="pagination.itemsPerPage"
                    :records="pagination.totalItems" @paginate="goToPage"></Pagination>
        <span v-else>No more items</span>
      </div>
    </div><!-- .container -->
  </section><!-- end explore-section -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import Pagination from 'vue-pagination-2';
import ProductCard from '@/components/section/ProductCard';
import Range from "../common/Range";

// Composables
import Vue from 'vue';
import {facetGetters, useFacet} from '@vue-storefront/numerbay';
import {useUiHelpers, useUiState} from '~/composables';
import {computed, ref} from '@vue/composition-api';
import {useVueRouter} from '~/helpers/hooks/useVueRouter';

export default {
  name: 'ExploreSection',
  components: {
    Pagination,
    ProductCard,
    Range
  },
  data() {
    return {
      selectedSortBy: null,
      page: this.$route.query.page ? parseInt(this.$route.query.page, 10) : 1,
      category: 'all',
      name: '',
      activeId: 1
    };
  },
  methods: {
    // sorting
    async onChangeSorting(option) {
      await this.th.changeSorting(option.id);
    },
    // pagination
    getLinkTo(page) {
      return {
        ...this.$route,
        query: {
          ...this.$route.query,
          page: page
        }
      };
    },
    async goToPage(page) {
      // console.log('page', this.getLinkTo(page));
      await this.$router.push(this.getLinkTo(page));
      // this.$emit("click", page);
    },
    // filter by category
    getSubcategories(categoryTree) {
      return categoryTree?.items || {
        "label": "All",
        "slug": "all",
        "id": 1,
        "isCurrent": false,
        "items": [
          {
            "label": "Numerai",
            "slug": "numerai",
            "id": 2,
            "isCurrent": false,
            "items": []
          },
          {
            "label": "Signals",
            "slug": "signals",
            "id": 5,
            "isCurrent": false,
            "items": []
          },
          {
            "label": "OnlyFams",
            "slug": "onlyfams",
            "id": 8,
            "isCurrent": false,
            "items": []
          }
        ]
      }.items;
    },
    filterProductsByCategory(products) {
      return products.filter(product => !product.category.indexOf(this.category));
    },
    // search item by keyword
    filterProductsByName(products) {
      return products.filter(product => !product.name.toLowerCase().indexOf(this.name.toLowerCase()));
    },
    // add active class to button
    getActiveClass(id) {
      if (id === this.activeCategory) {
        return 'active';
      } else {
        return '';
      }
    }
  },
  watch: {
    async $route(to, from) {
      // react to route changes...
      await this.search(this.th.getFacetsFromURL());
      // this.getActiveClass(this.activeId = this.activeCategory);
    },
    facets() {
      this.selectedSortBy = this.sortBy?.options?.find(o => o.id === (this.$route?.query?.sort || (this.result?.data?.categories[0].tournament ? 'rank-best' : 'latest')));
    }
  },
  computed: {
    sortBy() {
      return this.facetGetters.getSortOptions(this.result);
    }
  },
  setup() {
    const {
      route
    } = useVueRouter();
    const {path} = route;
    const th = useUiHelpers();
    const {
      result,
      search,
      loading
    } = useFacet(`facetId:${path}`);
    const products = computed(() => facetGetters.getProducts(result.value));
    const categoryTree = computed(() => facetGetters.getCategoryTree(result.value));
    // const sortBy = computed(() => facetGetters.getSortOptions(result.value));
    const facets = computed(() => facetGetters.getGrouped(result.value, ['status', 'platform', 'rank', 'stake', 'return3m']));
    const pagination = computed(() => facetGetters.getPagination(result.value));
    const activeCategory = computed(() => {
      const items = categoryTree?.value?.items;

      if (!items) {
        return '';
      }

      const category = items.find(({isCurrent, items}) => isCurrent || items.find(({isCurrent}) => isCurrent));

      return category?.id || items[0].id;
    });

    const {changeFilters, isFacetCheckbox} = useUiHelpers();
    const {isFilterSidebarOpen, toggleFilterSidebar} = useUiState();
    const selectedFilters = ref({});

    // onSSR(async () => {
    //   await search(th.getFacetsFromURL());
    //
    //   // if (facets.value.length > 0) {
    //   //   selectedFilters.value = facets.value.reduce((prev, curr) => ({
    //   //     ...prev,
    //   //     [curr.id]: curr.options
    //   //       .filter(o => o.selected)
    //   //       .map(o => o.id)
    //   //   }), {});
    //   // }
    // });

    search(th.getFacetsFromURL());

    if (facets.value.length > 0) {
      selectedFilters.value = facets.value.reduce((prev, curr) => ({
        ...prev,
        [curr.id]: curr.options
          .filter(o => o.selected)
          .map(o => o.id)
      }), {});
    }

    const filters = th.getFacetsFromURL().filters;
    Object.keys(filters).forEach((filter) => {
      if (filter === 'status' || filter === 'platform') {
        selectedFilters.value[filter] = filters[filter];
      } else {
        if (!selectedFilters.value[filter]) {
          Vue.set(selectedFilters.value, filter, []);
        }
        if (typeof filters[filter][0] === 'string') {
          selectedFilters.value[filter] = [filters[filter][0].split(',').map(Number)]
        } else {
          selectedFilters.value[filter] = [filters[filter][0]];
        }
      }
    });

    const isFilterSelected = (facet, option) => (selectedFilters.value[facet.id] || []).includes(option.id);

    const selectFilter = (facet, option) => {
      if (!selectedFilters.value[facet.id]) {
        Vue.set(selectedFilters.value, facet.id, []);
      }

      if (selectedFilters.value[facet.id].find(f => f === option.id)) {
        selectedFilters.value[facet.id] = selectedFilters.value[facet.id].filter(f => f !== option.id);
        return;
      }

      selectedFilters.value[facet.id].push(option.id);
    };

    const clearFilters = () => {
      toggleFilterSidebar();
      selectedFilters.value = {};
      changeFilters(selectedFilters.value);
    };

    const applyFilters = () => {
      // toggleFilterSidebar();
      changeFilters(selectedFilters.value);
    };

    const getRangeFilterOption = (options, tag) => {
      return options.filter(o => o.id === tag) ? Number(options.filter(o => o.id === tag)[0].value) : 0;
    };

    const getSelectedRangeFilterValue = (facet) => {
      const selectedValue = selectedFilters.value[facet.id] ? selectedFilters.value[facet.id][0] : [];
      if (selectedValue) {
        return selectedValue.map(Number);
      }
      return selectedValue;
    };

    const updateRangeFilter = (facet, values) => {
      if (!selectedFilters.value[facet.id]) {
        Vue.set(selectedFilters.value, facet.id, []);
      }

      selectedFilters.value[facet.id] = [values];
    };


    return {
      result,
      facets,
      facetGetters,
      loading,
      pagination,
      products,
      categoryTree,
      activeCategory,
      search,
      th,
      isFilterSidebarOpen,
      selectedFilters,
      isFacetCheckbox,
      isFilterSelected,
      toggleFilterSidebar,
      selectFilter,
      clearFilters,
      applyFilters,
      changeFilters,
      getRangeFilterOption,
      getSelectedRangeFilterValue,
      updateRangeFilter
    };
  }
};
</script>

<style lang="scss" scoped>
.details {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.fade {
  &-enter-active,
  &-leave-active {
    transition: opacity 0.25s linear;
  }

  &-enter,
  &-leave,
  &-leave-to {
    opacity: 0;
  }
}
</style>
