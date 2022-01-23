<template>
  <SfTabs :open-tab="1">
    <SfTab title="My polls">
      <div v-if="currentPoll">
        <SfButton class="sf-button--text all-polls" @click="currentPoll = null">All Listings</SfButton>
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
        <div v-if="polls.length === 0" class="no-polls">
          <p class="no-polls__title">{{ $t('You currently have no polls') }}</p>
        </div>
        <SfTable v-else class="polls">
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
              <div class="poll-actions">
                <SfButton class="sf-button--text action__element" @click="handlePollClick(poll)" :disabled="!!numeraiError.getModels || !userGetters.getNumeraiApiKeyPublicId(user) || numeraiLoading || userLoading">
                  {{ $t('Edit') }}
                </SfButton>
                <SfButton v-if="pollGetters.getIsActive(poll)" class="sf-button--text action__element" @click="handlePollClose(poll)" :disabled="!!numeraiError.getModels || !userGetters.getNumeraiApiKeyPublicId(user) || numeraiLoading || userLoading">
                  {{ $t('Close') }}
                </SfButton>
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
  SfButton,
  SfLink,
  SfNotification,
  SfProperty,
  SfTable,
  SfTabs
} from '@storefront-ui/vue';
import { computed, ref } from '@vue/composition-api';
import {
  pollGetters,
  useGlobals,
  useNumerai,
  usePoll,
  useUser,
  userGetters
} from '@vue-storefront/numerbay';
import { onSSR } from '@vue-storefront/core';
import { useUiState } from '~/composables';

export default {
  name: 'MyPolls',
  components: {
    SfTabs,
    SfTable,
    SfButton,
    SfProperty,
    SfLink,
    SfNotification
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
    const { polls, search, closePoll } = usePoll('polls');
    const { togglePollModal } = useUiState();
    const currentPoll = ref(null);

    const handlePollClick = async (poll) => {
      togglePollModal(poll);
    };

    const handlePollClose = async (poll) => {
      await closePoll({id: poll.id});
      await search({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
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

    return {
      tableHeaders,
      numeraiLoading,
      userLoading,
      getNumeraiModels,
      user: computed(() => user?.value ? user.value : null),
      polls: computed(() => polls?.value?.data ? polls.value.data : []),
      handlePollClick,
      handlePollClose,
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
.no-polls {
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
.polls {
  @include for-desktop {
    &__element {
      &--right {
        --table-column-flex: 0;
        text-align: right;
      }
    }
  }
}
.all-polls {
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
.poll-actions {
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
