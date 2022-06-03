<template>
  <div class="page-wrap">
    <!-- create -->
    <section class="create-section section-space-b pt-4 pt-md-5 mt-md-4">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-8">
            <div class="section-head-sm">
              <router-link :to="`/coupons`" class="btn-link fw-semibold"><em class="ni ni-arrow-left"></em> My coupons
              </router-link>
              <h1 class="mt-2">Create new coupon</h1>
            </div>
          </div><!-- end col -->
          <div class="col-lg-8">
            <ValidationObserver v-slot="{ handleSubmit }">
              <form action="#" class="form-create mb-5 mb-lg-0">
                <ValidationProvider key="username" v-slot="{ errors }" rules="required|min:2" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Username of
                        recipient</label>
                      <input v-model="form.username" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                             placeholder="Username of recipient of coupons (case sensitive)"
                             type="text">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <div class="form-item mb-4">
                  <label class="mb-2 form-label">Applicable products</label>
                  <client-only>
                    <multiselect ref="couponMultiSelect" v-model="form.applicable_products"
                                 :close-on-select="false" :group-select="true"
                                 :multiple="true" :options="groupedProducts" class="coupon-multiselect"
                                 group-label="category" group-values="products" label="sku" placeholder="Applicable Products"
                                 track-by="id"
                    >
                      <template slot="option" slot-scope="props">
                        <span>{{ props.option.$isLabel ? props.option.$groupLabel : props.option.name }}</span>
                      </template>
                    </multiselect>
                  </client-only>
                </div>
                <ValidationProvider key="discountPercent" v-slot="{ errors }"
                                    rules="required|integer|min_value:1|max_value:100" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Discount %</label>
                      <input v-model="form.discount_percent" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                             min="1" placeholder="Coupon Discount % (0-100, 100 being free)"
                             type="number">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider key="quantityTotal" v-slot="{ errors }" rules="required|integer|min_value:1" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Number of
                        redemptions</label>
                      <input v-model="form.quantity_total" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                             min="1" placeholder="Number of times this coupon can be redeemed"
                             type="number">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider key="maxDiscount" v-slot="{ errors }" rules="required|decimal|min_value:0" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Max discount</label>
                      <input v-model="form.max_discount" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                             min="0" placeholder="Coupon Max Discount (in NMR)" type="number">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider key="minSpend" v-slot="{ errors }" rules="decimal|min_value:0" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Min spend for
                        redemption</label>
                      <input v-model="form.min_spend" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                             min="0" placeholder="(Optional) Min Spend (in NMR) for Redeeming Coupon"
                             type="number">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider key="code" v-slot="{ errors }" rules="min:6" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Custom coupon
                        code</label>
                      <input v-model="form.code" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                             placeholder="(Optional) Leave empty to auto-generate coupon code"
                             type="text">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider key="dateExpiration" v-slot="{ errors }" rules="" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Expiration
                        date</label>
                      <input v-model="form.date_expiration" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                             placeholder="Expiration Date in UTC" type="date">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <button :disabled="productLoading" class="btn btn-dark" type="button"
                        @click="handleSubmit(saveCoupon)">
                  <span v-if="productLoading"><span class="spinner-border spinner-border-sm me-2" role="status"></span>Saving...</span>
                  <span v-else>Save</span>
                </button>
              </form>
            </ValidationObserver>
          </div><!-- endn col -->
        </div><!-- row-->
      </div><!-- container -->
    </section><!-- create-section -->
  </div><!-- end page-wrap -->
</template>

<script>
// Composables
import {computed, ref} from '@vue/composition-api';
import {onSSR} from '@vue-storefront/core';
import {
  productGetters,
  useCategory,
  useCoupon,
  useNumerai,
  useProduct,
  useUser,
  userGetters
} from '@vue-storefront/numerbay';
import {useUiNotification} from '~/composables';
import {extend} from 'vee-validate';

extend('decimal', {
  validate: (value, {decimals = '*', separator = '.'} = {}) => {
    if (value === null || value === undefined || value === '') {
      return {
        valid: false
      };
    }
    if (Number(decimals) === 0) {
      return {
        valid: /^-?\d*$/.test(value)
      };
    }
    const regexPart = decimals === '*' ? '+' : `{1,${decimals}}`;
    const regex = new RegExp(`^[-+]?\\d*(\\${separator}\\d${regexPart})?([eE]{1}[-]?\\d+)?$`);

    return {
      valid: regex.test(value)
    };
  },
  message: 'The {_field_} field must contain only decimal values'
});

export default {
  name: 'CreateCoupon',
  middleware: [
    'is-authenticated'
  ],
  mounted() {
    if (this.userGetters.getNumeraiApiKeyPublicId(this.user)) {
      this.getNumeraiModels().catch((e) => {
        this.send({
          message: e?.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle',
          persist: true,
          action: {
            text: 'Change Numerai API Key',
            onClick: async () => {
              await this.$router.push('/numerai-settings');
            }
          }
        });
      })
    }
  },
  beforeDestroy() {
    if (this.$refs.couponMultiSelect) {
      this.$refs.couponMultiSelect.deactivate();
    }
  },
  setup(props, context) {
    const {id} = context.root.$route.params;
    const {user, load: loadUser, loading: userLoading} = useUser();
    const {categories, search: categorySearch} = useCategory();
    const {createCoupon, error: couponError} = useCoupon();
    const {
      products,
      search: productSearch,
      loading: productLoading,
      error: productError
    } = useProduct('products');
    const {numerai, getModels: getNumeraiModels, error: numeraiError} = useNumerai('my-coupons');
    const {send} = useUiNotification();

    const currentListing = ref(null);

    onSSR(async () => {
      await loadUser();
      await categorySearch();
      await productSearch({filters: {user: {in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
    });

    const groupProducts = (products) => {
      const groupedProducts = products.reduce((rv, x) => {
        (rv[x.category.slug] = rv[x.category.slug] || []).push(x);
        return rv;
      }, {});
      return Object.keys(groupedProducts).map((key) => ({category: key, products: groupedProducts[key]}));
    };

    const productsData = computed(() => products?.value?.data ? products?.value?.data : []);

    const groupedProducts = computed(() => groupProducts(productsData.value));

    const resetForm = () => ({
      applicability: 'specific_products',
      username: null,
      applicable_products: [],
      discount_percent: null,
      quantity_total: 1,
      max_discount: null,
      min_spend: null,
      code: null,
      date_expiration: null
    })

    const form = ref(resetForm());

    const handleForm = (fn) => async () => {
      console.log(fn)
      // resetErrorValues();
      await fn({coupon: form.value});
      const hasCouponErrors = couponError.value.create;
      if (hasCouponErrors) {
        send({
          message: couponError.value.create?.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
        return;
      }

      await productSearch({filters: {user: {in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});

      await context.root.$router.push('/coupons', () => context.root.$router.go(0)); // todo fix coupon product lookup
    };

    const saveCoupon = async () => {
      form.value.applicable_product_ids = form.value.applicable_products ? form.value.applicable_products.map(p => p.id) : [];
      return handleForm(createCoupon)();
    };

    return {
      id,
      currentListing,
      form,
      leafCategories: computed(() => categories ? categories.value.filter((category) => {
        return category.items.length === 0;
      }).sort((a, b) => -a.slug.localeCompare(b.slug)) : []),
      numerai: computed(() => numerai ? numerai.value : null),
      groupedProducts,
      products,
      productLoading,
      productError,
      user,
      productGetters,
      userGetters,
      getNumeraiModels,
      resetForm,
      saveCoupon,
      send
    };
  }
};
</script>

<style lang="scss" scoped>
.featured-products-multiselect::v-deep {
  .multiselect__select {
    &:before {
      top: 30%;
      border-style: none;
      position: relative;
      content: "\e9c5";
      font-family: "Nioicon";
      font-size: 22px;
      color: #8091a7;
    }
  }

  .multiselect__tag {
    color: var(--vs-selected-color);
    background: var(--vs-selected-bg);
    border: var(--vs-selected-border-width) var(--vs-selected-border-style) var(--vs-selected-border-color);
  }

  .multiselect__option {
    color: #8091a7;

    &--highlight {
      color: #1c2b46;
      background: var(--vs-selected-bg);
    }

    &--highlight:after {
      color: #1c2b46;
      background: var(--vs-selected-bg);
    }
  }
}

.editor::v-deep {
  .ql-editor {
    min-height: 150px;
  }
}

.is-invalid::v-deep .vs__dropdown-toggle {
  border-color: #dc3545 !important;
  border-top-color: rgb(220, 53, 69) !important;
  border-right-color: rgb(220, 53, 69) !important;
  border-bottom-color: rgb(220, 53, 69) !important;
  border-left-color: rgb(220, 53, 69) !important;
}
</style>
