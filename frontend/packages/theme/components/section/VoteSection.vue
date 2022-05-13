<template>
  <section class="explore-section pt-4 section-space">
    <div class="container">
      <div class="row g-gs">
        <div v-if="poll.options" class="col-lg-6 mx-auto">
          <client-only>
            <vue-poll
              :answers="poll.options"
              :can-show-results="!poll.is_blind || poll.is_finished"
              :deadline="pollGetters.getEndDate(poll)"
              :description="poll.description"
              :loading="pollLoading"
              :maxOptions="poll.max_options"
              :multiple="poll.is_multiple"
              :owner="pollGetters.getOwner(poll) ? pollGetters.getOwner(poll).toUpperCase() : '-'"
              :question="poll.topic"
              :showResults="poll.has_voted || poll.is_finished"
              :weightMode="poll.weight_mode ? poll.weight_mode.toUpperCase() : '-'"
              @addvote="addVote"/>
          </client-only>
        </div>
      </div><!-- Poll -->
    </div><!-- .container -->
  </section><!-- end explore-section -->
</template>

<script>
// Composables
import {onSSR} from '@vue-storefront/core';
import {pollGetters, usePoll, useUser} from '@vue-storefront/numerbay';
import {useUiNotification} from '~/composables';
import {computed} from '@vue/composition-api';

export default {
  name: 'VoteSection',
  methods: {
    async addVote(obj) {
      if (!this.isAuthenticated) {
        this.send({
          message: 'You need to log in to vote',
          type: 'bg-warning',
          icon: 'ni-alert-circle'
        });
        await this.$router.push('/login-v2');
        return;
      }
      if (this.poll.is_multiple) {
        await this.vote({id: this.poll.id, options: obj.arSelected});
        if (this.pollError.voting) {
          await this.send({
            message: this.pollError.voting.message,
            type: 'bg-danger',
            icon: 'ni-alert-circle'
          });
        }
      } else {
        await this.vote({id: this.poll.id, options: [obj]});
        if (this.pollError.voting) {
          this.send({
            message: this.pollError.voting.message,
            type: 'bg-danger',
            icon: 'ni-alert-circle'
          });
        }
      }
      await this.search({id: this.id});
    }
  },
  setup(props, context) {
    const {id} = context.root.$route.params;
    const {polls, search, vote, loading: pollLoading, error: pollError} = usePoll(String(id));
    const {user, isAuthenticated} = useUser();
    const {send} = useUiNotification();

    const poll = computed(() => {
      return polls?.value?.data ? polls?.value?.data[0] : {};
    });

    onSSR(async () => {
      await search({id});
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
      search,
      id
    };
  }
};
</script>

<style lang="scss" scoped>

</style>
