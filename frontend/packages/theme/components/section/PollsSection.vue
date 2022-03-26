<template>
    <div class="col-lg-8">
        <div class="user-panel-title-box">
            <h3>My Polls</h3>
        </div><!-- end user-panel-title-box -->
        <div class="alert alert-danger d-flex mb-4" role="alert" v-if="!userGetters.getNumeraiApiKeyPublicId(user)">
            <svg class="flex-shrink-0 me-3" width="30" height="30" viewBox="0 0 24 24" fill="#ff6a8e">
                <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"></path>
            </svg>
            <p class="fs-14">
              In order to create a poll, you must <router-link to="/numerai-settings" class="btn-link">set up a Numerai API key.</router-link> It only takes a few minutes!
            </p>
        </div><!-- end alert -->
        <div class="profile-setting-panel-wrap">
          <router-link :to="`/create-poll`" class="btn btn-outline-dark mb-4" :class="(!userGetters.getNumeraiApiKeyPublicId(user) || userLoading) ? 'disabled' : ''"><em class="ni ni-plus"></em> New Poll</router-link>
          <div class="table-responsive">
                <table class="table mb-0 table-s2">
                    <thead class="fs-14">
                        <tr>
                            <th scope="col" v-for="(list, i) in [
                              'Poll Topic',
                              'End Date',
                              'Config',
                              'Status',
                              'Action'
                            ]" :key="i">{{ list }}</th>
                        </tr>
                    </thead>
                    <tbody class="fs-13">
                        <tr v-if="!polls || polls.length === 0"><td colspan="3" class="text-secondary">You have not created any poll</td></tr>
                        <tr v-for="poll in polls" :key="pollGetters.getId(poll)">
                          <th scope="row"><router-link class="btn-link" :to="`/vote/${pollGetters.getId(poll)}`"><span class="text-break" style="white-space: normal;">{{ pollGetters.getTopic(poll) }}</span></router-link></th>
                          <td>{{ pollGetters.getEndDate(poll) }}</td>
                          <td><span class="text-break" style="white-space: normal;">{{ `${poll.is_multiple?'multiple':'single'}, ${poll.is_blind?'blind':'observable'}, ${poll.is_anonymous?'anonymous':'named'}, ${poll.weight_mode}, ${poll.is_stake_predetermined?'pre-determined':'post-determined'}` }}</span></td>
                          <td><span class="badge fw-medium" :class="getStatusTextClass(poll)">{{ getStatusText(poll) }}</span></td>
                          <td><div class="d-flex justify-content-between">
                            <button class="icon-btn ms-auto me-2" title="Close" @click="handleClosePoll(pollGetters.getId(poll))">
                              <span class="spinner-border spinner-border-sm text-secondary" role="status" v-if="Boolean(polls) && pollLoading"></span>
                              <em class="ni ni-power" v-else></em>
                            </button>
                            <router-link :to="{
                              name: 'edit-poll',
                              params: {id: pollGetters.getId(poll)}}" class="icon-btn ms-auto me-2" title="Edit"><em class="ni ni-edit"></em></router-link>
                            <button class="icon-btn ms-auto" title="Delete" @click="handleDeletePoll(pollGetters.getId(poll))">
                              <span class="spinner-border spinner-border-sm text-secondary" role="status" v-if="Boolean(polls) && pollLoading"></span>
                              <em class="ni ni-trash" v-else></em>
                            </button>
                          </div></td>
                        </tr>
                    </tbody>
                </table>
            </div><!-- end table-responsive -->
            <!-- pagination -->
            <div class="text-center mt-4 mt-md-5">
                <Pagination :records="polls.length" v-model="page" :per-page="perPage"></Pagination>
            </div>
        </div><!-- end profile-setting-panel-wrap-->
    </div><!-- end col-lg-8 -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import Pagination from "vue-pagination-2";

// Composables
import { onSSR } from '@vue-storefront/core';
import { computed } from '@vue/composition-api';
import {
  pollGetters,
  usePoll,
  useUser,
  userGetters
} from '@vue-storefront/numerbay';

export default {
  name: 'PollsSection',
  components: {
    Pagination
  },
  data () {
    return {
      page: 1,
      perPage: 6
    };
  },
  computed: {
    displayedOrders() {
      const startIndex = this.perPage * (this.page - 1);
      const endIndex = startIndex + this.perPage;
      return this.orders?.slice(startIndex, endIndex);
    }
  },
  setup() {
    const { user, loading: userLoading } = useUser();

    const { polls, search, closePoll, deletePoll, loading: pollLoading, error: pollError } = usePoll('polls');

    const handleClosePoll = async (id) => {
      await closePoll({id: id});
      await search({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
    };

    onSSR(async () => {
      await search({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
    });

    const handleDeletePoll = async (id) => {
      await deletePoll({ id: id })
      await search({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
    }

    const getStatusText = (poll) => {
      if (poll.is_finished) {
        return 'closed';
      } else {
        return 'open';
      }
    };

    const getStatusTextClass = (poll) => {
      if (poll.is_finished) {
        return 'bg-secondary';
      } else {
        return 'bg-success';
      }
    };

    return {
      polls: computed(() => polls?.value?.data ? polls.value.data : []),
      pollLoading,
      pollError,
      pollGetters,
      user: computed(() => user?.value ? user.value : null),
      userLoading,
      userGetters,
      handleClosePoll,
      handleDeletePoll,
      getStatusText,
      getStatusTextClass
    };
  }
};
</script>
