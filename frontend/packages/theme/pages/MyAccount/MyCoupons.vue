<template>
  <SfTabs :open-tab="1">
    <SfTab title="My coupons">
      <p class="message">
        {{ $t('List of coupons') }}
<!--        <SfButton class="sf-button color-secondary" @click="refresh" :disabled="loading">
          Refresh
        </SfButton>-->
      </p>
      <div v-if="!user.coupons || user.coupons.length === 0" class="no-orders">
        <p class="no-orders__title">{{ $t('You currently have no coupons') }}</p>
        <SfButton class="no-orders__button" @click="$router.push('/c/numerai')">{{ $t('Start shopping') }}</SfButton>
      </div>
      <SfTable v-else class="orders">
        <SfTableHeading>
          <SfTableHeader
            v-for="tableHeader in tableHeaders"
            :key="tableHeader"
            >{{ tableHeader }}</SfTableHeader>
        </SfTableHeading>
        <SfTableRow v-for="coupon in user.coupons" :key="coupon.id">
          <SfTableData>{{ coupon.code }}</SfTableData>
          <SfTableData>{{ coupon.date_expiration }}</SfTableData>
          <SfTableData>{{ coupon.applicable_product_ids }}</SfTableData>
          <SfTableData>{{ coupon.discount_percent }} %</SfTableData>
          <SfTableData>{{ coupon.max_discount }} NMR</SfTableData>
          <SfTableData>{{ coupon.quantity_remaining }} / {{ coupon.quantity_total }}</SfTableData>
<!--          <SfTableData>{{ coupon.state }}</SfTableData>-->
        </SfTableRow>
      </SfTable>
    </SfTab>
  </SfTabs>
</template>

<script>
import {
  SfTabs,
  SfTable,
  SfButton,
  SfProperty,
  SfLink
} from '@storefront-ui/vue';
import { useUser } from '@vue-storefront/numerbay';
import OrderInfoPanel from '../../components/Molecules/OrderInfoPanel';

export default {
  name: 'MyCoupons',
  components: {
    SfTabs,
    SfTable,
    SfButton,
    SfProperty,
    SfLink,
    OrderInfoPanel
  },
  setup() {
    const { user, loading } = useUser();

    const tableHeaders = [
      'Coupon Code',
      'Valid Until',
      'Applicable Product IDs',
      'Discount %',
      'Max Discount',
      'Remaining'
      // 'State'
    ];

    return {
      tableHeaders,
      user,
      loading
    };
  }
};
</script>

<style lang='scss' scoped>
.no-orders {
  &__title {
    margin: 0 0 var(--spacer-lg) 0;
    font: var(--font-weight--normal) var(--font-size--base) / 1.6 var(--font-family--primary);
  }
  &__button {
    --button-width: 100%;
    @include for-desktop {
      --button-width: 17,5rem;
    }
  }
}
.orders {
  @include for-desktop {
    &__element {
      &--right {
        --table-column-flex: 0;
        text-align: right;
      }
    }
  }
}
.all-orders {
  --button-padding: var(--spacer-base) 0;
}
.message {
  margin: 0 0 var(--spacer-xl) 0;
  font: var(--font-weight--light) var(--font-size--base) / 1.6 var(--font-family--primary);
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  &__link {
    color: var(--c-primary);
    font-weight: var(--font-weight--medium);
    font-family: var(--font-family--primary);
    font-size: var(--font-size--base);
    text-decoration: none;
    &:hover {
      color: var(--c-text);
    }
  }
}
</style>
