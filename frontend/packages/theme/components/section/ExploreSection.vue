<template>
  <section class="explore-section pt-4  section-space">
    <div class="container">
      <!-- filter -->
      <div class="filter-box pb-5">
        <div class="filter-box-filter justify-content-between align-items-center">
          <div class="filter-box-filter-item">
            <v-select class="generic-select generic-select-s2" label="value" v-model="selectedSortBy"
                      :options="sortBy.options" :clearable=false @input="onChangeSorting"></v-select>
          </div><!-- end filter-box-filter-item -->
<!--          <div class="filter-box-filter-item">
            <button class="icon-btn icon-btn-s1" @click="toggleFilterSidebar" :class="isFilterSidebarOpen ? 'text-primary':''"><em class="ni ni-filter"></em></button>
          </div>&lt;!&ndash; end filter-box-filter-item &ndash;&gt;-->
          <div class="filter-box-filter-item ms-lg-auto filter-btn-wrap">
            <div class="filter-btn-group">
              <div class="menu-item d-inline-block" v-for="subcategory in getSubcategories(categoryTree)" :key="subcategory.id">
                <nuxt-link :to="localePath(th.getCatLink(subcategory))" class="btn filter-btn" :class="getActiveClass(subcategory.id)"
                   @click.prevent="activeId = subcategory.id">{{ subcategory.label }}</nuxt-link>
                <div class="menu-sub" style="z-index: 10000;">
                   <ul class="menu-list">
                        <li class="menu-item"><router-link :to="localePath(th.getCatLink(subcategory))" class="menu-link">All</router-link></li>
                        <li class="menu-item" v-for="subsubcategory in getSubcategories(subcategory)"><router-link :to="localePath(th.getCatLink(subsubcategory))" class="menu-link">{{ subsubcategory.label }}</router-link></li>
                   </ul>
                </div>
              </div>
            </div>
          </div><!-- end filter-box-filter-item -->
        </div><!-- end filter-box-filter -->
<!--        <transition name="fade">
        <div class="filter-box-filter justify-content-between align-items-center mt-2" v-if="isFilterSidebarOpen">
          <div v-for="(facet, i) in facets" :key="i">
            <h4>{{ facet.label }}</h4>
            <div
              v-if="isFacetCheckbox(facet)"
              class="filters__colors"
              :key="`${facet.id}-colors`"
            >
              <SfFilter
                v-for="option in facet.options"
                :key="`${facet.id}-${option.value}`"
                :label="option.id + `${option.count ? ` (${option.count})` : ''}`"
                :selected="isFilterSelected(facet, option)"
                class="filters__item"
                @change="() => selectFilter(facet, option)"
              />
            </div>
            <div v-else>
              <SfRange
                :id="facet.id"
                :disabled="false"
                :value="getSelectedRangeFilterValue(facet)"
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
                class="filters__item"
                @change="(values) => updateRangeFilter(facet, values)"
              />
            </div>
          </div>
        </div>&lt;!&ndash; end filter-box-filter &ndash;&gt;
        </transition>-->
      </div><!-- end filter-box -->
      <!-- Product -->
      <div class="row g-gs" v-if="loading">
        <div class="col-lg-6" v-for="index in 10" :key="index">
          <div class="card card-full flex-sm-row product-s2">
              <div class="card-image">
                  <img src="https://numer.ai/img/profile_picture_light.jpg" class="product-img" alt="avatar image">
              </div>
              <div class="card-body card-justified p-4">
                  <h5 class="card-title text-truncate mb-0 placeholder-glow"><span class="placeholder col-8"></span></h5>
                  <div class="card-author d-flex align-items-center justify-content-between placeholder-glow"><span class="placeholder col-6"></span></div>
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
      <div class="row g-gs" v-else>
        <div class="col-lg-6" v-for="product in products" :key="product.id">
          <ProductCard :product="product"></ProductCard>
        </div>
      </div><!-- end row -->
      <!-- pagination -->
      <div class="text-center mt-4 mt-md-5">
        <Pagination :records="pagination.totalItems" v-model="page" :per-page="pagination.itemsPerPage"
                    @paginate="goToPage"></Pagination>
      </div>
    </div><!-- .container -->
  </section><!-- end explore-section -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';
import Pagination from 'vue-pagination-2';
import ProductCard from '@/components/section/ProductCard';

// Composables
// import {onSSR} from '@vue-storefront/core';
import {facetGetters, productGetters, useCart, useFacet, useUser, useWishlist} from '@vue-storefront/numerbay';
import {useUiHelpers, useUiNotification, useUiState} from '~/composables';
import {computed, ref} from '@vue/composition-api';
import {useVueRouter} from '~/helpers/hooks/useVueRouter';

export default {
  name: 'ExploreSection',
  components: {
    Pagination,
    ProductCard
  },
  data() {
    return {
      selectedSortBy: null,
      page: this.$route.query.page ? parseInt(this.$route.query.page, 10) : 1,
      SectionData,
      category: 'all',
      name: '',
      activeId: 1,
      options: [
        'all',
        'art',
        'music',
        'games',
        'collectibles'
      ]
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
      return categoryTree?.items || [];
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
  mounted() {
    this.selectedSortBy = this.sortBy?.options?.find(o => o.id === (this.$route?.query?.sort || 'rank-best'));
  },
  watch: {
    async $route(to, from) {
      // react to route changes...
      await this.search(this.th.getFacetsFromURL());
      // this.getActiveClass(this.activeId = this.activeCategory);
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
    const sortBy = computed(() => facetGetters.getSortOptions(result.value));
    const facets = computed(() => facetGetters.getGrouped(result.value, ['status', 'platform', 'rank', 'stake', 'return3m']));
    const pagination = computed(() => facetGetters.getPagination(result.value));
    const activeCategory = computed(() => {
      const items = categoryTree?.value?.items;

      if (!items) {
        return '';
      }

      const category = items.find(({ isCurrent, items }) => isCurrent || items.find(({ isCurrent }) => isCurrent));

      return category?.id || items[0].id;
    });

    const { changeFilters, isFacetCheckbox } = useUiHelpers();
    const { isFilterSidebarOpen, toggleFilterSidebar } = useUiState();
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

    const isFilterSelected = (facet, option) => (selectedFilters.value[facet.id] || []).includes(option.id);

    const getRangeFilterOption = (options, tag) => {
      return options.filter(o=>o.id === tag) ? Number(options.filter(o=>o.id === tag)[0].value) : 0;
    };

    const getSelectedRangeFilterValue = (facet) => {
      const selectedValue = selectedFilters.value[facet.id] ? selectedFilters.value[facet.id][0] : [];
      if (selectedValue) {
        return selectedValue.map(Number);
      }
      return selectedValue;
    };


    return {
      sortBy,
      facets,
      loading,
      pagination,
      products,
      categoryTree,
      activeCategory,
      search,
      th,
      isFilterSidebarOpen,
      isFacetCheckbox,
      isFilterSelected,
      toggleFilterSidebar,
      changeFilters,
      getRangeFilterOption,
      getSelectedRangeFilterValue,
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
