<template>
  <SfTabs :open-tab="1">
    <SfTab title="My polls">
      <div v-if="currentPoll">
        <SfButton class="sf-button--text all-orders" @click="currentPoll = null">All Listings</SfButton>
      </div>
      <div v-else>
        <div class="top-buttons">
          <SfButton class="sf-button--primary" @click="handlePollClick()" :disabled="!!numeraiError.getModels || !userGetters.getNumeraiApiKeyPublicId(user) || numeraiLoading || userLoading">
            {{ $t('New Poll') }}
          </SfButton>
          <SfButton class="sf-button" v-if="!userGetters.getNumeraiApiKeyPublicId(user)" :class="!userGetters.getNumeraiApiKeyPublicId(user)?'color-primary':'color-secondary'" @click="$router.push('/my-account/numerai-api')" :disabled="numeraiLoading || userLoading">
            {{ !userGetters.getNumeraiApiKeyPublicId(user)?$t('Set Numerai API Key'):$t('Change Numerai API Key') }}
          </SfButton>
        </div>
        <p class="message" v-if="numeraiError.getModels">
          {{ numeraiError.getModels }}
        </p>
        <div v-if="polls.length === 0" class="no-orders">
          <p class="no-orders__title">{{ $t('You currently have no polls') }}</p>
        </div>
        <SfTable v-else class="orders">
          <SfTableHeading>
            <SfTableHeader
              v-for="tableHeader in tableHeaders"
              :key="tableHeader"
              >{{ tableHeader }}</SfTableHeader>
          </SfTableHeading>
          <SfTableRow v-for="poll in polls" :key="pollGetters.getId(poll)">
            <SfTableData>
              <SfLink :link="'/v/'+pollGetters.getId(poll)" :style="pollGetters.getIsActive(poll) ? '' : 'color: var(--c-text-disabled)'">
                {{ pollGetters.getTopic(poll) }}
              </SfLink>
            </SfTableData>
            <SfTableData><span :style="pollGetters.getIsActive(poll) ? '' : 'color: var(--c-text-disabled)'">{{ pollGetters.getEndDate(poll) }}</span></SfTableData>
            <SfTableData><span :style="pollGetters.getIsActive(poll) ? '' : 'color: var(--c-text-disabled)'">{{ `${poll.is_multiple?'multiple':'single'}, ${poll.is_blind?'blind':'observable'}, ${poll.is_anonymous?'anonymous':'named'}, ${poll.weight_mode}, ${poll.is_stake_predetermined?'pre-determined':'post-determined'}` }}</span></SfTableData>
            <SfTableData>
              <div class="listing-actions">
                <SfButton class="sf-button--text action__element" @click="handlePollClick(poll)" :disabled="!!numeraiError.getModels || !userGetters.getNumeraiApiKeyPublicId(user) || numeraiLoading || userLoading">
                  {{ $t('Edit') }}
                </SfButton>
<!--                <SfButton class="sf-button&#45;&#45;text action__element" @click="handlePollDelete(poll)" :disabled="!!numeraiError.getModels || !userGetters.getNumeraiApiKeyPublicId(user) || numeraiLoading || userLoading">
                  {{ $t('Delete') }}
                </SfButton>-->
              </div>
            </SfTableData>
          </SfTableRow>
        </SfTable>
      </div>
    </SfTab>
  </SfTabs>
</template>

<script>
import {
  SfTabs,
  SfTable,
  SfButton,
  SfProperty,
  SfLink,
  SfNotification
} from '@storefront-ui/vue';
import { computed, ref } from '@vue/composition-api';
import { useUiState } from '~/composables';
import {
  pollGetters,
  useProduct,
  usePoll,
  useUser,
  userGetters,
  useCategory,
  useNumerai,
  useGlobals
} from '@vue-storefront/numerbay';
import { AgnosticOrderStatus } from '@vue-storefront/core';
import { onSSR } from '@vue-storefront/core';
import NumeraiApiForm from '../../components/MyAccount/NumeraiApiForm';
import ArtifactPanel from '../../components/Molecules/ArtifactPanel';

export default {
  name: 'MyPolls',
  components: {
    SfTabs,
    SfTable,
    SfButton,
    SfProperty,
    SfLink,
    SfNotification,
    NumeraiApiForm,
    ArtifactPanel
  },
  mounted() {
    if (this.userGetters.getNumeraiApiKeyPublicId(this.user)) {
      this.getNumeraiModels();
    }
  },
  setup() {
    const { user, loading: userLoading } = useUser();
    const { getModels: getNumeraiModels, loading: numeraiLoading, error: numeraiError } = useNumerai('my-listings');
    const { getGlobals } = useGlobals();

    onSSR(async () => {
    });
    const { polls, search } = usePoll('polls');
    const { togglePollModal } = useUiState();
    const currentPoll = ref(null);

    const handlePollClick = async (poll) => {
      togglePollModal(poll);
    };

    onSSR(async () => {
      await search({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
      await getGlobals();
    });

    const tableHeaders = [
      'Poll Topic',
      'End Date',
      'Config',
      'Action'
    ];

    const getStatusTextClass = (order) => {
      const status = orderGetters.getStatus(order);
      switch (status) {
        case AgnosticOrderStatus.Open:
          return 'text-warning';
        case AgnosticOrderStatus.Complete:
          return 'text-success';
        default:
          return '';
      }
    };

    return {
      tableHeaders,
      numeraiLoading,
      userLoading,
      getNumeraiModels,
      user: computed(() => user?.value ? user.value : null),
      polls: computed(() => polls?.value?.data ? polls.value.data : []),
      getStatusTextClass,
      handlePollClick,
      userGetters,
      pollGetters,
      currentPoll,
      numeraiError
    };
  }
};
</script>

<style lang='scss' scoped>
.top-buttons {
  @include for-desktop {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
}
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
.product {
  &__properties {
    margin: var(--spacer-xl) 0 0 0;
  }
  &__property,
  &__action {
    font-size: var(--font-size--sm);
  }
  &__action {
    color: var(--c-gray-variant);
    font-size: var(--font-size--sm);
    margin: 0 0 var(--spacer-sm) 0;
    &:last-child {
      margin: 0;
    }
  }
  &__qty {
    color: var(--c-text);
  }
}
.products {
  --table-column-flex: 1;
  &__name {
    margin-right: var(--spacer-sm);
    @include for-desktop {
      --table-column-flex: 2;
    }
  }
}
.highlighted {
  box-sizing: border-box;
  width: 100%;
  background-color: var(--c-light);
  padding: var(--spacer-sm);
  --property-value-font-size: var(--font-size--base);
  --property-name-font-size: var(--font-size--base);
  &:last-child {
    margin-bottom: 0;
  }
  ::v-deep .sf-property__name {
    white-space: nowrap;
  }
  ::v-deep .sf-property__value {
    text-align: right;
  }
  &--total {
    margin-bottom: var(--spacer-sm);
  }
  @include for-desktop {
    padding: var(--spacer-xl);
    --property-name-font-size: var(--font-size--lg);
    --property-name-font-weight: var(--font-weight--medium);
    --property-value-font-size: var(--font-size--lg);
    --property-value-font-weight: var(--font-weight--semibold);
  }
}
.listing-actions {
  display: flex; flex-direction: row;
  .action__element {
    @include for-desktop {
      flex: 1;
      margin-left: var(--spacer-2xs);
      margin-right: var(--spacer-2xs);
    }

    &:last-child {
      margin-right: 0;
    }
  }
}
</style>
