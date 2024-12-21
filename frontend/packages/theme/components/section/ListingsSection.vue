<template>
  <div class="col-lg-8">
    <div class="user-panel-title-box">
      <h3>My Listings</h3>
    </div><!-- end user-panel-title-box -->
    <div v-if="!userGetters.getNumeraiApiKeyPublicId(user)" class="alert alert-danger d-flex mb-4" role="alert">
      <svg class="flex-shrink-0 me-3" fill="#ff6a8e" height="30" viewBox="0 0 24 24" width="30">
        <path
          d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"></path>
      </svg>
      <p class="fs-14">
        In order to list Numerai products for sale, you must
        <router-link class="btn-link" to="/numerai-settings">set up a Numerai API key.</router-link>
        It only takes a few minutes!
      </p>
    </div><!-- end alert -->
    <div class="profile-setting-panel">
      <router-link :class="(!userGetters.getNumeraiApiKeyPublicId(user) || userLoading) ? 'disabled' : ''" :to="`/create-listing`"
                   class="btn btn-outline-dark mb-1"><em
        class="ni ni-plus"></em> New Listing
      </router-link>
      <div class="row g-gs" v-if="!displayedProducts || displayedProducts.length === 0">
        <div class="col-xl-12">You currently have no listing
        </div>
      </div>
      <div v-else class="row g-gs mt-5" v-for="category in ['numerai-predictions', 'signals-predictions', 'crypto-predictions', 'numerai-models', 'signals-data', 'other']">
        <div class="row" v-if="filterProductsByCategory(displayedProducts, category).length > 0">
          <div class="col-12">
            <ul class="nav nav-tabs nav-tabs-s3" role="tablist">
              <li class="nav-item" role="presentation">
                <button :id="'past'" class="nav-link" type="button">{{ category }}</button>
              </li>
            </ul>
          </div>
        </div>
        <div v-for="product in filterProductsByCategory(displayedProducts, category)" :key="productGetters.getId(product)"
             class="col-xl-6">
          <div class="card card-full">
            <div class="card-body card-body-s1">
              <p class="mb-3 fs-13 mb-4">Sold {{ productGetters.getQtySales(product) }}<span
                v-if="productGetters.getQtySales(product) > 0"><span class="dot-separeted"></span>{{
                  productGetters.getQtyDelivered(product)
                }} / {{ productGetters.getQtySales(product) }} on time</span></p>
              <div class="card-media mb-3">
                <div class="card-media-img flex-shrink-0">
                  <img :src="productGetters.getCoverImage(product)" alt="avatar image">
                </div><!-- card-media-img -->
                <div class="card-media-body">
                  <h4>
                    <router-link
                      :to="`/product/${productGetters.getCategory(product).slug}/${productGetters.getName(product)}`">
                      {{ productGetters.getName(product).toUpperCase() }}
                    </router-link>
                  </h4>
                  <p class="fw-medium fs-14">{{ productGetters.getCategory(product).slug }}</p>
                  <p v-if="productGetters.getUseEncryption(product)" class="fs-15">Encrypted</p>
                  <p v-else class="fs-15">Unencrypted</p>
                </div><!-- end card-media-body -->
              </div><!-- end card-media -->
              <div class="card-media mb-3">
                <div class="card-media-body">
                  <span class="fw-medium fs-13">Default Price</span>
                  <p class="fw-medium text-black fs-14">
                    {{ productGetters.getOptionFormattedPrice(productGetters.getOrderedOption(product, 0), true) }}</p>
                </div>
                <div class="card-media-body">
                  <span class="fw-medium fs-13">Default Mode</span>
                  <p class="fw-medium text-black fs-14 text-capitalize">
                    {{ productGetters.getMode(productGetters.getOrderedOption(product, 0), true) }}</p>
                </div>
              </div><!-- end d-flex -->
              <ul class="btns-group">
                <li><span :class="getStatusTextClass(product)" class="badge fw-medium">{{
                    getStatusText(product)
                  }}</span></li>
                <li><span v-if="product.is_daily" class="badge fw-medium bg-info">Daily</span></li>
                <li>
                  <router-link :to="{
                            name: 'edit-listing',
                            params: {id: productGetters.getId(product)}}"
                               class="btn-link fw-medium fs-13 text-secondary" title="Edit">Edit
                  </router-link>
                </li>
                <li>
                  <router-link :to="{
                            name: 'manage-artifacts',
                            params: {id: productGetters.getId(product)}}" class="btn-link fw-medium fs-13 text-primary"
                               title="Manage Artifacts">Upload Files
                  </router-link>
                </li>
              </ul>
            </div><!-- end card-body -->
          </div><!-- end card -->
        </div><!-- end col -->
      </div><!-- end row -->
      <!-- pagination -->
<!--      <div class="text-center mt-4 mt-md-5">
        <Pagination v-model="page" :per-page="perPage" :records="products.length"></Pagination>
      </div>-->
    </div><!-- end profile-setting-panel -->
  </div><!-- end col-lg-8 -->
</template>

<script>
import Pagination from 'vue-pagination-2';

// Composables
import {onSSR} from '@vue-storefront/core';
import {computed} from '@vue/composition-api';
import {productGetters, useProduct, useUser, userGetters} from '@vue-storefront/numerbay';

export default {
  name: 'PurchasesSection',
  components: {
    Pagination
  },
  data() {
    return {
      page: 1,
      perPage: 6,
      currentOrder: {}
    };
  },
  computed: {
    displayedProducts() {
      // const startIndex = this.perPage * (this.page - 1);
      // const endIndex = startIndex + this.perPage;
      // return this.products?.slice(startIndex, endIndex);
      return this.products
    }
  },
  methods: {
    filterProductsByCategory(products, category) {
      if (category === 'other') {
        return products.filter(product => !['numerai-predictions', 'signals-predictions', 'numerai-models', 'signals-data', 'crypto-predictions'].includes(productGetters.getCategory(product).slug));
      }
      return products.filter(product => productGetters.getCategory(product).slug === category);
    }
  },
  setup() {
    const {user, loading: userLoading} = useUser();
    const {products, search, loading: productLoading} = useProduct('my-listings');

    onSSR(async () => {
      await search({filters: {user: {in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
    });

    const getStatusText = (product) => {
      if (productGetters.getIsActive(product)) {
        return 'Active';
      } else {
        return 'Delisted';
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
      user,
      userLoading,
      productGetters,
      userGetters,
      getStatusText,
      getStatusTextClass
    };
  }
};
</script>
