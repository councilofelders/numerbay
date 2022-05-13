import { CustomQuery, Context, FactoryParams } from '@vue-storefront/core';
import { Ref, computed } from '@vue/composition-api';
import { sharedRef, Logger, configureFactoryParams } from '@vue-storefront/core';
import { UseCoupon, UseCouponErrors } from '../types/composables';

export interface UseCouponFactoryParams<COUPONS, COUPON_SEARCH_PARAMS extends any> extends FactoryParams {
  createCoupon: (context: Context, params: any) => Promise<any>;
  deleteCoupon: (context: Context, params: any) => Promise<any>;
}

export function useCouponFactory<COUPONS, COUPON_SEARCH_PARAMS>(
  factoryParams: UseCouponFactoryParams<COUPONS, COUPON_SEARCH_PARAMS>
) {
  return function useCoupon(id: string): UseCoupon<COUPONS, COUPON_SEARCH_PARAMS> {
    const loading = sharedRef(false, `useCoupon-loading-${id}`);
    const _factoryParams = configureFactoryParams(factoryParams);

    const errorsFactory = (): UseCouponErrors => ({
      create: null,
      delete: null
    });

    const error: Ref<UseCouponErrors> = sharedRef(errorsFactory(), `useCoupon-error-${id}`);

    const resetErrorValue = () => {
      error.value = errorsFactory();
    };

    const createCoupon = async ({coupon: providedCoupon}) => {
      Logger.debug('useCouponFactory.createCoupon', providedCoupon);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.createCoupon({coupon: providedCoupon});
        error.value.create = null;
      } catch (err) {
        error.value.create = err;
        Logger.error('useCoupon/createCoupon', err);
      } finally {
        loading.value = false;
      }
    };

    const deleteCoupon = async ({id}) => {
      Logger.debug('useCouponFactory.deleteCoupon', id);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.deleteCoupon({id});
        error.value.delete = null;
      } catch (err) {
        error.value.delete = err;
        Logger.error('useCoupon/deleteCoupon', err);
      } finally {
        loading.value = false;
      }
    };

    return {
      createCoupon,
      deleteCoupon,
      loading: computed(() => loading.value),
      error: computed(() => error.value)
    };
  };
}
