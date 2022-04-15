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
      <router-link :to="`/explore/numerai`" class="btn btn-outline-dark mb-4"
                   :class="(!userGetters.getNumeraiApiKeyPublicId(user) || userLoading) ? 'disabled' : ''">Start
        Shopping
      </router-link>
      <div class="table-responsive">
        <table class="table mb-0 table-s2">
          <thead class="fs-14">
          <tr>
            <th scope="col" v-for="(list, i) in [
                              'Code',
                              'Until',
                              'Allowed Product IDs',
                              'Off %',
                              'Max Discount',
                              'Remain'
                            ]" :key="i">{{ list }}
            </th>
          </tr>
          </thead>
          <tbody class="fs-13">
          <tr v-if="!user.coupons || user.coupons.length === 0">
            <td colspan="3" class="text-secondary">You currently have no coupon</td>
          </tr>
          <tr v-for="coupon in user.coupons" :key="coupon.id">
            <td>{{ coupon.code }}</td>
            <td>{{ coupon.date_expiration || '-' }}</td>
            <td>
              <span class="text-break" style="white-space: normal;"><a class="btn-link"
                                                                       v-for="product_id in coupon.applicable_product_ids"
                                                                       :href="`/p/${product_id}`"
                                                                       target="_blank">{{ product_id }}, </a></span>
            </td>
            <td>{{ coupon.discount_percent }} %</td>
            <td>{{ coupon.max_discount }} NMR</td>
            <td>{{ coupon.quantity_remaining }} / {{ coupon.quantity_total }}</td>
          </tr>
          </tbody>
        </table>
      </div><!-- end table-responsive -->
      <!-- pagination -->
      <div class="text-center mt-4 mt-md-5">
        <Pagination :records="user.coupons.length" v-model="page" :per-page="perPage"></Pagination>
      </div>
    </div><!-- end profile-setting-panel-wrap-->
  </div><!-- end col-lg-8 -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import Pagination from "vue-pagination-2";

// Composables
import {computed} from '@vue/composition-api';
import {
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
      perPage: 6
    };
  },
  setup() {
    const {user, loading: userLoading} = useUser();

    return {
      user: computed(() => user?.value ? user.value : null),
      userLoading,
      userGetters
    };
  }
};
</script>
