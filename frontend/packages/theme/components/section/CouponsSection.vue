<template>
  <div class="col-lg-8">
    <div class="user-panel-title-box">
      <h3>My Coupons</h3>
    </div><!-- end user-panel-title-box -->
    <div class="alert alert-danger d-flex mb-4" role="alert" v-if="!userGetters.getNumeraiApiKeyPublicId(user)">
      <svg class="flex-shrink-0 me-3" width="30" height="30" viewBox="0 0 24 24" fill="#ff6a8e">
        <path
          d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"></path>
      </svg>
      <p class="fs-14">
        In order to make a purchase, you must
        <router-link to="/numerai-settings" class="btn-link">set up a Numerai API key.</router-link>
        It only takes a few minutes!
      </p>
    </div><!-- end alert -->
    <div class="profile-setting-panel-wrap">
      <router-link :to="`/create-coupon`" class="btn btn-outline-dark mb-4"
                   :class="(!userGetters.getNumeraiApiKeyPublicId(user) || userLoading) ? 'disabled' : ''">Create Coupon
      </router-link>
      <ul class="nav nav-tabs nav-tabs-s3 mb-2" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link" :class="'active'" :id="'received'" type="button">Received coupons</button>
        </li>
      </ul>
      <div class="row g-gs">
        <div class="col-xl-12" v-if="!displayedProductCoupons || displayedProductCoupons.length === 0">You have not
          received any coupon
        </div>
        <div class="col-xl-6" v-for="(productCoupon, i) in displayedProductCoupons" :key="i"
             v-if="displayedProductCoupons">
          <div class="card card-full">
            <div class="card-body card-body-s1">
              <p class="mb-3 fs-13 mb-4">{{ productCoupon.quantity_remaining }} / {{ productCoupon.quantity_total }}
                remaining<span
                  v-if="productCoupon.date_expiration"><span
                  class="dot-separeted"></span>expires on {{ productCoupon.date_expiration }}</span></p>
              <div class="card-media mb-3">
                <div class="card-media-img flex-shrink-0">
                  <img :src="productGetters.getCoverImage(productCoupon.product)" alt="avatar image">
                </div><!-- card-media-img -->
                <div class="card-media-body">
                  <h4>
                    <router-link
                      :to="`/product/${productGetters.getCategory(productCoupon.product).slug}/${productGetters.getName(productCoupon.product)}`">
                      {{ productGetters.getName(productCoupon.product).toUpperCase() }}
                    </router-link>
                  </h4>
                  <p class="fw-medium fs-14">{{ productGetters.getCategory(productCoupon.product).slug }}</p>
                  <div class="fs-15">
                    Code:
                    <div class="tooltip-s1">
                      <button v-clipboard:copy="productCoupon.code" v-clipboard:success="onCopy"
                              class="copy-text" type="button">
                        <span class="tooltip-s1-text tooltip-text">Copy</span>
                        <span class="btn-link text-decoration-none fw-medium">{{ productCoupon.code }}</span>
                        <em class="ni ni-copy"></em>
                      </button>
                    </div>
                  </div>
                </div><!-- end card-media-body -->
              </div><!-- end card-media -->
              <div class="card-media mb-3">
                <div class="card-media-body">
                  <span class="fw-medium fs-13">Discount %</span>
                  <p class="fw-medium text-black fs-14">
                    {{ productCoupon.discount_percent }} %</p>
                </div>
                <div class="card-media-body">
                  <span class="fw-medium fs-13">Discount Cap</span>
                  <p class="fw-medium text-black fs-14 text-capitalize">
                    {{ productCoupon.max_discount }} NMR</p>
                </div>
              </div><!-- end d-flex -->
            </div><!-- end card-body -->
          </div><!-- end card -->
        </div><!-- end col -->
      </div><!-- end row -->
      <!-- pagination -->
      <div class="text-center mt-4 mt-md-5">
        <Pagination :records="productCoupons.length" v-model="page" :per-page="perPage"></Pagination>
      </div>
      <ul class="nav nav-tabs nav-tabs-s3 mb-2 mt-4" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link" :id="'created'" type="button">Created coupons</button>
        </li>
      </ul>
      <div class="row g-gs">
        <div class="col-xl-12" v-if="!displayedCreatedProductCoupons || displayedCreatedProductCoupons.length === 0">You
          have not created any coupon
        </div>
        <div class="col-xl-6" v-for="(productCoupon, i) in displayedCreatedProductCoupons" :key="i"
             v-if="displayedCreatedProductCoupons">
          <div class="card card-full">
            <div class="card-body card-body-s1">
              <p class="mb-3 fs-13 mb-4">@{{ productCoupon.owner.username }}<span
                class="dot-separeted"></span>{{ productCoupon.quantity_remaining }} / {{ productCoupon.quantity_total }}
                remaining<span
                  v-if="productCoupon.date_expiration"><span
                  class="dot-separeted"></span>expires on {{ productCoupon.date_expiration }}</span></p>
              <div class="card-media mb-3">
                <div class="card-media-img flex-shrink-0">
                  <img :src="productGetters.getCoverImage(productCoupon.product)" alt="avatar image">
                </div><!-- card-media-img -->
                <div class="card-media-body">
                  <h4>
                    <router-link
                      :to="`/product/${productGetters.getCategory(productCoupon.product).slug}/${productGetters.getName(productCoupon.product)}`">
                      {{ productGetters.getName(productCoupon.product).toUpperCase() }}
                    </router-link>
                  </h4>
                  <p class="fw-medium fs-14">{{ productGetters.getCategory(productCoupon.product).slug }}</p>
                  <div class="fs-15">
                    Code:
                    <div class="tooltip-s1">
                      <button v-clipboard:copy="productCoupon.code" v-clipboard:success="onCopy"
                              class="copy-text" type="button">
                        <span class="tooltip-s1-text tooltip-text">Copy</span>
                        <span class="btn-link text-decoration-none fw-medium">{{ productCoupon.code }}</span>
                        <em class="ni ni-copy"></em>
                      </button>
                    </div>
                  </div>
                </div><!-- end card-media-body -->
              </div><!-- end card-media -->
              <div class="card-media mb-3">
                <div class="card-media-body">
                  <span class="fw-medium fs-13">Discount %</span>
                  <p class="fw-medium text-black fs-14">
                    {{ productCoupon.discount_percent }} %</p>
                </div>
                <div class="card-media-body">
                  <span class="fw-medium fs-13">Discount Cap</span>
                  <p class="fw-medium text-black fs-14 text-capitalize">
                    {{ productCoupon.max_discount }} NMR</p>
                </div>
              </div><!-- end d-flex -->
              <ul class="btns-group">
                <li>
                  <a href="javascript:void(0);" @click="handleDeleteCoupon(productCoupon.id)"
                     class="btn-link fw-medium fs-13 text-danger"
                     title="Delete coupon">Delete
                  </a>
                </li>
              </ul>
            </div><!-- end card-body -->
          </div><!-- end card -->
        </div><!-- end col -->
      </div><!-- end row -->
      <!-- pagination -->
      <div class="text-center mt-4 mt-md-5">
        <Pagination :records="createdProductCoupons.length" v-model="createdCouponsPage"
                    :per-page="perPage"></Pagination>
      </div>
    </div><!-- end profile-setting-panel-wrap-->
  </div><!-- end col-lg-8 -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import Pagination from "vue-pagination-2";

// Composables
import {onSSR} from '@vue-storefront/core';
import {computed} from '@vue/composition-api';
import {
  useCoupon,
  productGetters,
  useProduct,
  useUser,
  userGetters
} from '@vue-storefront/numerbay';

export default {
  name: 'CouponsSection',
  components: {
    Pagination
  },
  data() {
    return {
      page: 1,
      createdCouponsPage: 1,
      perPage: 6
    };
  },
  computed: {
    displayedProductCoupons() {
      const startIndex = this.perPage * (this.page - 1);
      const endIndex = startIndex + this.perPage;
      return this.productCoupons?.slice(startIndex, endIndex);
    },
    displayedCreatedProductCoupons() {
      const startIndex = this.perPage * (this.createdCouponsPage - 1);
      const endIndex = startIndex + this.perPage;
      return this.createdProductCoupons?.slice(startIndex, endIndex);
    }
  },
  setup() {
    const {user, load: loadUser, loading: userLoading} = useUser();
    const {products, search, loading: productLoading} = useProduct('coupons');
    const {deleteCoupon} = useCoupon('coupons');

    const couponProductIds = [...new Set(user?.value.coupons.map(c => c.applicable_product_ids || []).flat()), ...new Set(user?.value.created_coupons.map(c => c.applicable_product_ids || []).flat())];

    onSSR(async () => {
      await search({filters: {id: {in: couponProductIds}}, sort: 'latest'});
    });

    const productLookUp = computed(() => Object.assign({}, ...(products?.value?.data ? products.value.data : []).map(({
                                                                                                                        id,
                                                                                                                        ...rest
                                                                                                                      }) => ({[id]: {id, ...rest}}))));

    const productCoupons = computed(() => {
      const productCoupons = [];
      user?.value.coupons.forEach((coupon) => {
        (coupon.applicable_product_ids || []).forEach((product_id) => {
          productCoupons.push({...coupon, product: productLookUp.value[parseInt(product_id)]})
        });
      });
      return productCoupons;
    });

    const createdProductCoupons = computed(() => {
      const createdProductCoupons = [];
      user?.value.created_coupons.forEach((coupon) => {
        (coupon.applicable_product_ids || []).forEach((product_id) => {
          createdProductCoupons.push({...coupon, product: productLookUp.value[parseInt(product_id)]})
        });
      });
      return createdProductCoupons;
    });

    const onCopy = (e) => {
      const target = e.trigger.querySelector('.tooltip-text');
      const prevText = target.innerHTML;
      target.innerHTML = 'Copied';
      setTimeout(function () {
        target.innerHTML = prevText;
      }, 1000);
    };

    const handleDeleteCoupon = async (id) => {
      await deleteCoupon({id: id})
      await loadUser();
    }

    return {
      handleDeleteCoupon,
      productCoupons,
      createdProductCoupons,
      productGetters,
      user: computed(() => user?.value ? user.value : null),
      userLoading,
      userGetters,
      onCopy
    };
  }
};
</script>
