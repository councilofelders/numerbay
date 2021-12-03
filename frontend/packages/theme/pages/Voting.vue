<template>
  <div id="product">
    <!--<SfBreadcrumbs
      class="breadcrumbs desktop-only"
      :breadcrumbs="breadcrumbs"
    />-->
    <SfLoader :class="{ pollLoading }" :loading="pollLoading">
      <div class="product" v-if="!pollLoading">
        <div class="product__info_full">
          <div class="product__header">
            <SfHeading
              :title="poll.topic"
              :level="1"
              class="sf-heading--no-underline sf-heading--left"
            />
            <SfIcon
              icon="drag"
              size="xxl"
              color="var(--c-text-disabled)"
              class="product__drag-icon smartphone-only"
            />
          </div>
          <div class="product__subheader">
            <div class="sf-heading__title h5 sf-heading--no-underline sf-heading--left">
              <div class="product__meta">
                <span class="product__meta__item">Owner:&nbsp;<span class="product__subheader__highlight">{{ pollGetters.getOwner(poll) ? pollGetters.getOwner(poll).toUpperCase() : '-' }}</span></span>
                <span class='divider-pipe desktop-only'>|</span>
                <span class="product__meta__item">Weight Mode:&nbsp;<span class="product__subheader__highlight">{{ poll.weight_mode ? poll.weight_mode.toUpperCase() : '-' }}</span></span>
                <span class='divider-pipe desktop-only'>|</span>
                <span class="product__meta__item">End Date:&nbsp;<span class="product__subheader__highlight">{{ pollGetters.getEndDate(poll) }}</span></span>
                <span class='divider-pipe desktop-only'>|</span>
                <span class="product__meta__item">Anonymous Vote:&nbsp;<span class="product__subheader__highlight">{{ poll.is_anonymous ? 'YES':'NO' }}</span></span>
              </div>
            </div>
          </div>
          <LazyHydrate when-idle>
            <SfTabs id="tabs" :open-tab="1" class="product__tabs">
              <SfTab title="Poll">
                {{ poll.description }}
                <vue-poll :can-show-results="!poll.is_blind || poll.is_finished" :multiple="poll.is_multiple" :maxOptions="poll.max_options" :answers="poll.options" @addvote="addVote" :showResults="poll.has_voted || poll.is_finished"/>
              </SfTab>
            </SfTabs>
          </LazyHydrate>
        </div>
      </div>
    </SfLoader>
  </div>
</template>
<script>
import {
  SfHeading,
  SfTabs,
  SfIcon,
  SfAlert,
  SfBreadcrumbs,
  SfBadge,
  SfLoader
} from '@storefront-ui/vue';

import { computed } from '@vue/composition-api';
import { pollGetters, usePoll, useUser } from '@vue-storefront/numerbay';
import { useUiState, useUiNotification } from '~/composables';
import { onSSR } from '@vue-storefront/core';
import LazyHydrate from 'vue-lazy-hydration';

export default {
  name: 'Voting',
  transition: 'fade',
  setup(props, context) {
    const { id } = context.root.$route.params;
    const { polls, search, vote, loading: pollLoading, error: pollError } = usePoll(String(id));
    const { user, isAuthenticated } = useUser();
    const { toggleLoginModal } = useUiState();
    const { send } = useUiNotification();

    const poll = computed(() => {
      return polls?.value?.data ? polls?.value?.data[0] : {};
    });

    onSSR(async () => {
      await search({ id });
    });

    return {
      pollGetters,
      poll,
      vote,
      pollLoading,
      pollError,
      user,
      isAuthenticated,
      send,
      toggleLoginModal,
      search,
      id
    };
  },
  components: {
    SfBadge,
    SfAlert,
    SfHeading,
    SfTabs,
    SfIcon,
    SfBreadcrumbs,
    SfLoader,
    LazyHydrate
  },
  // test
  methods: {
    async addVote(obj) {
      if (!this.isAuthenticated) {
        await this.search({ id: this.id });
        this.send({
          message: 'You need to log in to vote',
          type: 'info'
        });
        this.toggleLoginModal();
        return;
      }
      // if (!this.user.numerai_api_key_public_id) {
      //   this.search({ id: this.id });
      //   this.send({
      //     message: 'This action requires Numerai API Key',
      //     type: 'info',
      //     action: {text: 'Set Numerai API Key', onClick: ()=>this.$router.push('/my-account/numerai-api')},
      //     persist: true
      //   });
      //   return;
      // }
      if (this.poll.is_multiple) {
        await this.vote({id: this.poll.id, options: obj.arSelected});
        if (this.pollError.voting) {
          await this.send({
            message: this.pollError.voting.message,
            type: 'danger'
          });
        }
      } else {
        await this.vote({id: this.poll.id, options: [obj]});
        if (this.pollError.voting) {
          this.send({
            message: this.pollError.voting.message,
            type: 'danger'
          });
        }
      }
    }
  },
  data() {
    return {
      breadcrumbs: [
        {
          text: 'Home',
          route: {
            link: '/'
          }
        },
        {
          text: 'Category',
          route: {
            link: '#'
          }
        },
        {
          text: 'Numerai',
          route: {
            link: '#'
          }
        }
      ]
    };
  }
};
</script>

<style lang="scss" scoped>
#product {
  box-sizing: border-box;
  @include for-desktop {
    max-width: 1272px;
    margin: 0 auto;
  }
}
.divider-pipe {
  padding: var(
    --breadcrumbs-list-item-before-padding,
    0 var(--spacer-sm)
  );
  color: var(--breadcrumbs-list-item-before-color, var(--c-text-muted));
}
.product {
  @include for-desktop {
    display: block;
    width: 60rem;
    margin: var(--spacer-lg) auto;
  }
  &__info {
    margin: var(--spacer-sm) auto;
    @include for-desktop {
      max-width: 32.625rem;
      margin: 0 0 0 7.5rem;
    }
  }
  &__info_full {
    margin: var(--spacer-sm) auto;
  }
  &__header {
    --heading-title-color: var(--c-link);
    --heading-title-font-weight: var(--font-weight--bold);
    --heading-padding: 0;
    margin: 0 var(--spacer-sm);
    display: flex;
    justify-content: space-between;
    @include for-desktop {
      --heading-title-font-weight: var(--font-weight--semibold);
      margin: 0 auto;
    }
  }
  &__subheader {
    --heading-title-color: var(--c-text-muted);
    --heading-title-font-weight: var(--font-weight--bold);
    --heading-padding: 0;
    margin: 0 var(--spacer-sm);
    display: flex;
    justify-content: space-between;
    @include for-desktop {
      --heading-title-font-weight: var(--font-weight--semibold);
      margin: 0 auto;
    }
    @include for-mobile {
      display: block;
    }
    &__highlight {
      color: var(--c-primary);
    }
  }
  &__meta {
    display: flex;
    @include for-mobile {
      flex-direction: column;
      //flow: block;
    }
  }
  &__meta__item {
    display: flex;
  }
  &__pricing {
    margin: 0 var(--spacer-sm);
    display: flex;
    justify-content: space-between;
    @include for-desktop {
      margin: var(--spacer-sm) 0 var(--spacer-lg) 0;
    }
    @include for-mobile {
      align-items: flex-start;
      flex-direction: column;
    }
  }
  &__drag-icon {
    animation: moveicon 1s ease-in-out infinite;
  }
  &__tabs {
    --tabs-title-z-index: 0;
    margin: var(--spacer-base) auto var(--spacer-2xl);
    --tabs-title-font-size: var(--font-size--lg);
    @include for-desktop {
      margin-top: var(--spacer-xl);
    }
  }
}
.breadcrumbs {
  margin: var(--spacer-base) auto var(--spacer-lg);
}
@keyframes moveicon {
  0% {
    transform: translate3d(0, 0, 0);
  }
  50% {
    transform: translate3d(0, 30%, 0);
  }
  100% {
    transform: translate3d(0, 0, 0);
  }
}
</style>
