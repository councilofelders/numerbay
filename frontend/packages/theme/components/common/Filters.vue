<template>
  <div class="filter-box">
    <div class="filter-box-filter">
      <div class="filter-box-filter-item dropdown d-none">
        <button class="btn dropdown-toggle filter-btn" type="button" data-bs-toggle="dropdown">
          {{ SectionData.filterCatData.title }}
        </button>
        <div class="dropdown-menu card-generic card-generic-s2 my-2 keep-open">
          <div class="generic-scroll">
            <router-link class="dropdown-item card-generic-item" :to="list.path" v-for="(list, i) in []" :key="i"
                         :class="list.class">{{ list.title }}
            </router-link>
          </div>
        </div>
      </div><!-- end dropdwon -->
      <div class="filter-box-filter-item dropdown d-none">
        <button class="btn dropdown-toggle filter-btn" type="button" data-bs-toggle="dropdown">
          {{ SectionData.filterCollectionData.title }}
        </button>
        <div class="dropdown-menu card-generic card-generic-s2 my-2 keep-open">
          <div class="generic-scroll">
            <router-link class="dropdown-item card-generic-item" :to="list.path" v-for="(list, i) in []" :key="i"
                         :class="list.class">{{ list.title }}
            </router-link>
          </div>
          <hr class="my-2">
          <div class="card-generic-footer p-2">
            <ul class="btns-group">
              <li v-for="(btn, i) in SectionData.filterCollectionData.btnData" :key="i"><a href="#"
                                                                                           class="btn btn-sm btn-light">{{
                  btn
                }}</a></li>
            </ul>
          </div>
        </div>
      </div><!-- end dropdwon -->
      <div class="filter-box-filter-item dropdown d-none">
        <button class="btn dropdown-toggle filter-btn" type="button" data-bs-toggle="dropdown">
          {{ SectionData.filterSaleTypeData.title }}
        </button>
        <div class="dropdown-menu card-generic card-generic-s2 my-2 keep-open">
          <div class="generic-scroll">
            <router-link class="dropdown-item card-generic-item" :to="list.path"
                         v-for="(list, i) in SectionData.filterSaleTypeData.saleTypeList" :key="i" :class="list.class">
              {{ list.title }}
            </router-link>
          </div>
          <hr class="my-2">
          <div class="card-generic-footer p-2">
            <ul class="btns-group">
              <li v-for="(btn, i) in SectionData.filterSaleTypeData.btnData" :key="i"><a href="#"
                                                                                         class="btn btn-sm btn-light">{{
                  btn
                }}</a></li>
            </ul>
          </div>
        </div>
      </div><!-- end dropdwon -->
      <div class="filter-box-filter-item ms-md-auto">
        <div class="dropdown">
          <button class="btn dropdown-toggle filter-btn" type="button" data-bs-toggle="dropdown">{{
              menuTabs.title
            }}
          </button>
          <div class="dropdown-menu card-generic card-generic-s2 my-2 dropdown-menu-end keep-open">
            <div class="text-secondary py-2 px-3 filter-box-sort-text"><span>Sort by</span></div>
            <a href="#" class="dropdown-item card-generic-item" v-for="tab in menuTabs" @click.prevent="setTab(tab)"
               :key="tab.id">{{ tab.title }}</a>
          </div>

        </div>
      </div><!-- end filter-box-filter-item -->
    </div><!-- end filter-box-filter -->
  </div><!-- end filter-box -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

export default {
  name: 'Filters',
  data() {
    return {
      SectionData,
      menuTabs: [
        {
          title: 'All jobs',
          options: [
            {
              status: 'all'
            },
            {
              status: 'active'
            },
            {
              status: 'not_active'
            }
          ]
        },
        {
          title: 'Drafts',
          options: [
            {
              status: 'all'
            },
            {
              status: 'draft'
            }
          ]
        },
        {
          title: 'To Be Approved',
          options: [
            {
              status: 'all'
            },
            {
              status: 'need_approval'
            },
            {
              status: 'rejected'
            }
          ]
        }
      ],
      tableData: [
        {
          id: 1,
          title: 'Salesperson',
          publish_date: '2019-07-10',
          status: 'active'
        },
        {
          id: 2,
          title: 'Developer',
          publish_date: '2019-11-12',
          status: 'not_active'
        },
        {
          id: 3,
          title: 'Freelanceer',
          publish_date: '2019-06-10',
          status: 'need_approval'
        },
        {
          id: 4,
          title: 'Construction worker',
          publish_date: '2019-12-06',
          status: 'active'
        },
        {
          id: 5,
          title: 'IT support',
          publish_date: '2019-11-20',
          status: 'draft'
        }
      ],
      selectedTab: null
    };
  },
  methods: {
    setTab(tab) {
      this.selectedTab = tab;
    }
  },
  computed: {
    filteredData() {
      return this.tableData.filter(data => {
        if (this.selectedTab === null) return true;
        const opts = this.selectedTab.options.map(opt => opt.status);
        return opts.includes(data.status);
      });
    }
  }
};
</script>
