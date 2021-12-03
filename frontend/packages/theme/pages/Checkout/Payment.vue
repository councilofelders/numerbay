<template>
  <div>
    <SfHeading
      :level="3"
      title="Payment"
      class="sf-heading--left sf-heading--no-underline title"
    />
    <SfTable class="sf-table--bordered table desktop-only">
      <SfTableHeading class="table__row">
        <SfTableHeader class="table__header table__image">{{ $t('Item') }}</SfTableHeader>
        <SfTableHeader
          v-for="tableHeader in tableHeaders"
          :key="tableHeader"
          class="table__header"
          :class="{ table__description: tableHeader === 'Description' }"
        >
          {{ tableHeader }}
        </SfTableHeader>
      </SfTableHeading>
      <SfTableRow
        v-for="(product, index) in products"
        :key="index"
        class="table__row"
      >
        <SfTableData class="table__image">
          <SfImage :src="productGetters.getCoverImage(product)" :alt="productGetters.getName(product).toUpperCase()" />
        </SfTableData>
        <SfTableData class="table__data table__description table__data">
          <div class="product-title">{{ productGetters.getName(product).toUpperCase() }}</div>
          <div class="product-sku">{{ productGetters.getSlug(product).toUpperCase() }}</div>
          <div class="product-sku">{{ productGetters.getFormattedOption(productGetters.getOptionById(product, optionId)) }}</div>
        </SfTableData>
        <SfTableData class="table__data">
          {{ productGetters.getOwner(product).toUpperCase() }}
        </SfTableData>
        <SfTableData class="table__data">{{ qty }}</SfTableData>
        <SfTableData class="table__data price">
          <SfPrice
            :regular="productGetters.getOptionFormattedPrice(productGetters.getOptionById(product, optionId), true)"
            class="product-price"
          />
        </SfTableData>
      </SfTableRow>
    </SfTable>
    <div class="summary">
      <div class="summary__group">
        <!--<div class="summary__total">
          <SfProperty
            name="Subtotal"
            :value="productGetters.getFormattedPrice(products[0])"
            class="sf-property&#45;&#45;full-width property"
          />
        </div>

        <SfDivider />-->
        <SfLoader :class="{ loader: loading || productLoading }" :loading="loading || productLoading">
          <SfProperty
            name="Total"
            v-if="!loading && !productLoading && !!products[0]"
            :value="`${(productGetters.getOptionById(products[0], optionId).price * qty).toFixed(4)} ${productGetters.getOptionById(products[0], optionId).currency}`"
            class="sf-property--full-width sf-property--large summary__property-total"
          />
        </SfLoader>
<!--        <VsfPaymentProvider @status="isPaymentReady = true"/>-->

        <SfCheckbox v-e2e="'terms'" v-model="terms" name="terms" class="summary__terms">
          <template #label>
            <div class="sf-checkbox__label">
              I understand that I need to make payment in <b>1 single transaction in full that goes directly to the seller</b>, and <b>neither Numerai nor NumerBay is liable for any loss</b> resulted from this transaction.
            </div>
          </template>
        </SfCheckbox>
        <SfCheckbox v-model="submitModel" name="terms" class="summary__submit" v-if="productGetters.getMode(productGetters.getOptionById(products[0], optionId))==='file'">
          <template #label>
            <div class="sf-checkbox__label">
              (Optional) Submit this model to Numerai for me automatically if seller submits to NumerBay. [This will not happen if seller provides self-managed file URL]
            </div>
          </template>
        </SfCheckbox>
        <SfCheckbox disabled selected name="terms" class="summary__submit" v-else>
          <template #label>
            <div class="sf-checkbox__label">
              Submit this model to Numerai for me automatically.
            </div>
          </template>
        </SfCheckbox>
        <SfLoader :class="{ loader: loading || productLoading || numeraiLoading }" :loading="loading || productLoading || numeraiLoading">
          <SfSelect label="Model Name" v-model="submitModelId" v-if="!loading && !productLoading && !numeraiLoading && (submitModel || productGetters.getMode(productGetters.getOptionById(products[0], optionId))!=='file')">
            <SfSelectOption value=""></SfSelectOption>
            <SfSelectOption v-for="model in models" :key="`${model.id}`" :value="`${model.id}`">{{model.name}}</SfSelectOption>
          </SfSelect>
        </SfLoader>

        <div class="summary__action">
          <SfButton
            v-e2e="'make-an-order'"
            :disabled="loading || productLoading || numeraiLoading || !terms || ((submitModel || productGetters.getMode(productGetters.getOptionById(products[0], optionId))!=='file') && !submitModelId)"
            class="summary__action-button"
            @click="processOrder"
          >
            {{ $t('Pay') }}
          </SfButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  SfHeading,
  SfTable,
  SfCheckbox,
  SfButton,
  SfDivider,
  SfImage,
  SfPrice,
  SfProperty,
  SfSelect,
  SfLink,
  SfLoader
} from '@storefront-ui/vue';
import { onSSR } from '@vue-storefront/core';
import { ref, computed } from '@vue/composition-api';
import {
  useProduct,
  useMakeOrder,
  useCart,
  useUserOrder,
  useNumerai,
  productGetters,
  useGlobals,
  userGetters
} from '@vue-storefront/numerbay';
import { useUiNotification } from '~/composables';
// import Web3 from 'web3';

export default {
  name: 'ReviewOrder',
  components: {
    SfHeading,
    SfTable,
    SfCheckbox,
    SfButton,
    SfDivider,
    SfImage,
    SfPrice,
    SfProperty,
    SfSelect,
    SfLink,
    SfLoader,
    VsfPaymentProvider: () => import('~/components/Checkout/VsfPaymentProvider')
  },
  async mounted() {
    const id = this.$route.query.product;
    await this.getGlobals();
    // eslint-disable-next-line camelcase
    await this.orderSearch({ role: 'buyer', filters: {product: {in: [id]}, round_order: {in: [this.globals.selling_round]}, state: {in: ['pending', 'confirmed']}} });
    if (this.orders?.data?.length > 0) {
      this.send({
        message: 'You already bought this product for this round',
        type: 'info'
      });
      this.$router.push(`/checkout/confirmation?order=${this.orders.data[0].id}`);
    }
  },
  setup(props, context) {
    const id = context.root.$route.query.product;
    const optionId = parseInt(context.root.$route.query.option);
    const qty = parseInt(context.root.$route.query.qty) || 1;
    const { load, setCart } = useCart();
    const { order, make, loading, error: makeOrderError } = useMakeOrder();
    const { orders, search: orderSearch } = useUserOrder('order-history');
    const { products, search, loading: productLoading } = useProduct(String(id));
    const { globals, getGlobals } = useGlobals();
    const { numerai, getModels, loading: numeraiLoading } = useNumerai('my-listings'); // , error: numeraiError
    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    // const { web3User, initWeb3Modal, ethereumListener } = useUser();
    const { send } = useUiNotification();

    const isPaymentReady = ref(false);
    const terms = ref(false);
    const submitModel = ref(false);
    const submitModelId = ref(null);

    onSSR(async () => {
      await load();
      await search({ id });
    });

    getModels();

    // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
    const pay = async (successCallback, failureCallback) => {
      // await initWeb3Modal();
      // await ethereumListener();
      // const sender = web3User.value.activeAccount;
      // const receiver = web3User.value.activeAccount;
      // const web3 = new Web3(web3User.value.providerEthers.provider);
      // const paymentPromise = web3.eth.sendTransaction({
      //   from: sender,
      //   // gasPrice: '50',
      //   // gas: '50',
      //   to: receiver,
      //   value: '1000000000000000'
      //   // data: ''
      // });
      try {
        const paymentPromise = (async () => 'fake data')();
        await paymentPromise.then(() => {
          successCallback();
        });
      } catch (error) {
        failureCallback();
      }
      // web3.sendTransaction({to: receiver, from: sender, value: web3.toWei("0.5", "ether")})
    };

    const processOrder = async () => {
      await make({id, optionId, quantity: qty, submitModelId: submitModelId.value});
      if (makeOrderError.value.make) {
        const isNumeraiApiError = makeOrderError.value.make.message.includes('Numerai API');
        send({
          message: makeOrderError.value.make.message,
          type: 'danger',
          action: isNumeraiApiError ? {text: 'Change Numerai API Key', onClick: ()=>context.root.$router.push('/my-account/numerai-api')} : null,
          persist: isNumeraiApiError
        });
        return;
      }
      await pay(() => context.root.$router.push(`/checkout/confirmation?order=${order?.value?.id}`), () => console.log('Payment failed: '));
      setCart(null);
    };

    return {
      isPaymentReady,
      terms,
      submitModel,
      submitModelId,
      loading,
      orders,
      globals: computed(() => globals?.value ? globals?.value : {}),
      getGlobals,
      products: computed(() => products?.value?.data ? products?.value?.data : []),
      productLoading,
      models: computed(() => products?.value?.data ? userGetters.getModels(numerai.value, productGetters.getTournamentId(products?.value?.data[0]), false) : []),
      numeraiLoading,
      tableHeaders: ['Description', 'Seller', 'Order Quantity', 'Price'],
      productGetters,
      processOrder,
      orderSearch,
      send,
      optionId,
      qty
    };
  }
};
</script>

<style lang="scss" scoped>
.title {
  margin: var(--spacer-xl) 0 var(--spacer-base) 0;
}
.table {
  margin: 0 0 var(--spacer-base) 0;
  &__row {
    justify-content: space-between;
  }
  @include for-desktop {
    &__header {
      text-align: center;
      &:last-child {
        text-align: right;
      }
    }
    &__data {
      text-align: center;
    }
    &__description {
      text-align: left;
      flex: 0 0 12rem;
    }
    &__image {
      --image-width: 5.125rem;
      text-align: left;
      margin: 0 var(--spacer-xl) 0 0;
    }
  }
}
.product-sku {
  color: var(--c-text-muted);
  font-size: var(--font-size--sm);
}
.price {
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
}
.product-price {
  --price-font-size: var(--font-size--base);
}
.summary {
  &__terms {
    margin: var(--spacer-base) 0 0 0;
  }
  &__total {
    margin: 0 0 var(--spacer-sm) 0;
    flex: 0 0 16.875rem;
  }
  &__action {
    @include for-desktop {
      display: flex;
      margin: var(--spacer-xl) 0 0 0;
    }
  }
  &__action-button {
    margin: 0;
    width: 100%;
    margin: var(--spacer-sm) 0 0 0;
    @include for-desktop {
      margin: 0 var(--spacer-xl) 0 0;
      width: auto;
    }
    &--secondary {
      @include for-desktop {
        text-align: right;
      }
    }
  }
  &__back-button {
    margin: var(--spacer-xl) 0 0 0;
    width: 100%;
    @include for-desktop {
      margin: 0 var(--spacer-xl) 0 0;
      width: auto;
    }
    color:  var(--c-white);
    &:hover {
      color:  var(--c-white);
    }
  }
  &__property-total {
    margin: var(--spacer-xl) 0 0 0;
  }
}
.property {
  margin: 0 0 var(--spacer-sm) 0;
  &__name {
    color: var(--c-text-muted);
  }
}
.content {
  margin: 0 0 var(--spacer-xl) 0;
  color: var(--c-text);
  &:last-child {
    margin: 0;
  }
  &__label {
    font-weight: var(--font-weight--normal);
  }
}
</style>
