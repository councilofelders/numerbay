<template>
  <section class="explore-section pt-4 section-space">
    <div class="container">
      <div class="row g-gs">
        <div class="col-lg-6 mx-auto" v-if="poll.options">
          <client-only>
          <vue-poll
            :owner="pollGetters.getOwner(poll) ? pollGetters.getOwner(poll).toUpperCase() : '-'"
            :deadline="pollGetters.getEndDate(poll)"
            :weightMode="poll.weight_mode ? poll.weight_mode.toUpperCase() : '-'"
            :question="poll.topic"
            :description="poll.description"
            :loading="pollLoading"
            :can-show-results="!poll.is_blind || poll.is_finished"
            :multiple="poll.is_multiple"
            :maxOptions="poll.max_options"
            :answers="poll.options"
            @addvote="addVote"
            :showResults="poll.has_voted || poll.is_finished"/>
          </client-only>
        </div>
      </div><!-- Poll -->
    </div><!-- .container -->
  </section><!-- end explore-section -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component

// Composables
import { onSSR } from '@vue-storefront/core';
import { pollGetters, usePoll, useUser } from '@vue-storefront/numerbay';
import { useUiNotification } from '~/composables';
import { computed } from '@vue/composition-api';

export default {
  name: 'VoteSection',
  data() {
    return {

    };
  },
  methods: {
    async addVote(obj) {
      if (!this.isAuthenticated) {
        // await this.search({ id: this.id });
        this.send({
          message: 'You need to log in to vote',
          type: 'bg-warning',
          icon: 'ni-alert-circle'
        });
        await this.$router.push('/login-v2');
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
      await this.search({ id: this.id });
    }
  },
  setup(props, context) {
    const { id } = context.root.$route.params;
    const { polls, search, vote, loading: pollLoading, error: pollError } = usePoll(String(id));
    const { user, isAuthenticated } = useUser();
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
      search,
      id
    };
  }
};
</script>

<style lang="scss" scoped>

</style>
