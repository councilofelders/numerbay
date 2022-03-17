<template>
    <div class="col-lg-8">
        <div class="user-panel-title-box">
            <h3>My Listings</h3>
        </div><!-- end user-panel-title-box -->
        <div class="profile-setting-panel-wrap">
          <router-link :to="`/create-listing`" class="btn btn-outline-dark"><em class="ni ni-plus"></em> New Listing</router-link>
          <div class="table-responsive">
                <table class="table mb-0 table-s2">
                    <thead class="fs-14">
                        <tr>
                            <th scope="col" v-for="(list, i) in [
                              'Product',
                              'Category',
                              'Default Price',
                              'Status',
                              'Action'
                            ]" :key="i">{{ list }}</th>
                        </tr>
                    </thead>
                    <tbody class="fs-13">
                        <tr v-for="product in products" :key="productGetters.getId(product)">
                          <th scope="row"><router-link class="btn-link" :to="`/product/${productGetters.getCategory(product).slug}/${productGetters.getName(product)}`">{{ productGetters.getName(product) }}</router-link></th>
                          <td>{{ productGetters.getCategory(product).slug }}</td>
                          <td>{{ productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, 0), true) }}</td>
                          <td><span class="badge fw-medium" :class="getStatusTextClass(product)">{{ getStatusText(product) }}</span></td>
                          <td><div class="d-flex justify-content-between">
                            <router-link :to="{
                              name: 'manage-artifacts',
                              params: {id: productGetters.getId(product)}}" class="icon-btn ms-auto" title="Manage Artifacts"><em class="ni ni-upload"></em></router-link>
                            <router-link :to="{
                              name: 'edit-listing',
                              params: {id: productGetters.getId(product)}}" class="icon-btn ms-auto" title="Edit"><em class="ni ni-edit"></em></router-link>
                          </div></td>
                        </tr>
                    </tbody>
                </table>
            </div><!-- end table-responsive -->
            <!-- pagination -->
            <div class="text-center mt-4 mt-md-5">
                <Pagination :records="products.length" v-model="page" :per-page="perPage"></Pagination>
            </div>
        </div><!-- end profile-setting-panel-wrap-->
    </div><!-- end col-lg-8 -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';
import Pagination from 'vue-pagination-2';

// Composables
import { onSSR } from '@vue-storefront/core';
import { computed } from '@vue/composition-api';
import { productGetters, useProduct, useUser, userGetters } from '@vue-storefront/numerbay';

export default {
  name: 'PurchasesSection',
  components: {
    Pagination
  },
  data () {
    return {
      SectionData,
      page: 1,
      perPage: 6,
      currentOrder: {}
    };
  },
  computed: {
    displayedOrders() {
      const startIndex = this.perPage * (this.page - 1);
      const endIndex = startIndex + this.perPage;
      return this.orders?.slice(startIndex, endIndex);
    }
  },
  setup() {
    const { user, loading: userLoading } = useUser();
    const { products, search, loading: productLoading } = useProduct('my-listings');

    onSSR(async () => {
      await search({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
    });

    const getStatusText = (product) => {
      if (productGetters.getIsActive(product)) {
        return 'active';
      } else {
        return 'delisted';
      }
    };

    const getStatusTextClass = (product) => {
      if (productGetters.getIsActive(product)) {
        return 'bg-success';
      } else {
        return 'bg-secondary';
      }
    };

    return {
      products: computed(() => products?.value?.data ? products.value.data : []),
      productGetters,
      getStatusText,
      getStatusTextClass
    };
  }
};
</script>
