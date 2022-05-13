<template>
  <div class="page-wrap">
    <!-- create -->
    <section class="create-section section-space-b pt-4 pt-md-5 mt-md-4">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-8">
            <div class="section-head-sm">
              <router-link :to="`/polls`" class="btn-link fw-semibold"><em class="ni ni-arrow-left"></em> My polls
              </router-link>
              <h1 class="mt-2">{{ !id ? `Create new poll` : `Edit poll` }}</h1>
            </div>
          </div><!-- end col -->
          <div class="col-lg-8">
            <ValidationObserver v-slot="{ handleSubmit }">
              <form action="#" class="form-create mb-5 mb-lg-0">
                <ValidationProvider v-slot="{ errors }" rules="required|min:2" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Poll topic</label>
                      <p :class="{ 'text-danger': Boolean(errors[0]) }" class="form-text mb-3">Set the poll topic. This
                        cannot be changed later.</p>
                      <input v-model="form.topic" :class="!errors[0] ? '' : 'is-invalid'" :disabled="Boolean(currentPoll)"
                             class="form-control form-control-s1" placeholder="Poll Topic" type="text">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider v-slot="{ errors }" rules="required" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">End date</label>
                      <input v-model="form.dateFinish" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                             placeholder="End Date in UTC" type="date">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider v-slot="{ errors }" rules="min:2" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Description</label>
                      <input v-model="form.description" :class="!errors[0] ? '' : 'is-invalid'" class="form-control form-control-s1"
                             placeholder="(Optional) Short Description" type="text">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <ValidationProvider v-slot="{ errors }" rules="min:2|alpha_dash" slim>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Short link</label>
                      <p :class="{ 'text-danger': Boolean(errors[0]) }" class="form-text mb-3">Set a short URL for the
                        poll. This cannot be changed later.</p>
                      <input v-model="form.id" :class="!errors[0] ? '' : 'is-invalid'" :disabled="Boolean(currentPoll)"
                             class="form-control form-control-s1" placeholder="(Optional) Custom Poll ID for Shorthand URL"
                             type="text">
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div>
                  </div><!-- end form-item -->
                </ValidationProvider>
                <div class="form-item mb-4">
                  <div class="mb-4">
                    <div class="d-flex align-items-center justify-content-between">
                      <div class="me-2">
                        <h5 class="mb-1">Multiple choice</h5>
                        <p class="form-text">Voter can choose multiple options. This cannot be changed later</p>
                      </div>
                      <div class="form-check form-switch form-switch-s1">
                        <input v-model="form.isMultiple" :disabled="Boolean(currentPoll)" class="form-check-input"
                               type="checkbox" @change="onIsMultipleChange(form.isMultiple)">
                      </div><!-- end form-check -->
                    </div><!-- end d-flex -->
                  </div>
                </div><!-- end form-item -->
                <div v-if="form.isMultiple">
                  <ValidationProvider v-slot="{ errors }" rules="required|integer|min_value:1" slim>
                    <div class="form-item mb-4">
                      <div class="mb-4">
                        <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Maximum options to
                          select</label>
                        <input v-model="form.maxOptions" :class="!errors[0] ? '' : 'is-invalid'"
                               :disabled="Boolean(currentPoll)" class="form-control form-control-s1" min="1"
                               placeholder="Maximum Options for a Vote" type="number">
                        <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                      </div>
                    </div><!-- end form-item -->
                  </ValidationProvider>
                </div>
                <div class="form-item mb-4">
                  <div class="mb-4">
                    <div class="d-flex align-items-center justify-content-between">
                      <div class="me-2">
                        <h5 class="mb-1">Show advanced settings</h5>
                      </div>
                      <div class="form-check form-switch form-switch-s1">
                        <input v-model="showAdvanced" class="form-check-input" type="checkbox">
                      </div><!-- end form-check -->
                    </div><!-- end d-flex -->
                  </div>
                </div><!-- end form-item -->
                <div v-show="showAdvanced">
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <div class="d-flex align-items-center justify-content-between">
                        <div class="me-2">
                          <h5 class="mb-1">Blind results</h5>
                          <p class="form-text">Results will be kept blind until poll ends</p>
                        </div>
                        <div class="form-check form-switch form-switch-s1">
                          <input v-model="form.isBlind" :disabled="Boolean(currentPoll)" class="form-check-input"
                                 type="checkbox" @change="onIsBlindChange(form.isBlind)">
                        </div><!-- end form-check -->
                      </div><!-- end d-flex -->
                    </div>
                  </div><!-- end form-item -->
                  <div v-if="form.isBlind">
                    <div class="form-item mb-4">
                      <div class="mb-4">
                        <div class="d-flex align-items-center justify-content-between">
                          <div class="me-2">
                            <h5 class="mb-1">Pre-determine stake</h5>
                            <p class="form-text">Determine NMR stake for weight calculation as of poll creation</p>
                          </div>
                          <div class="form-check form-switch form-switch-s1">
                            <input v-model="form.isStakePredetermined" :disabled="Boolean(currentPoll) || !form.isBlind" class="form-check-input"
                                   type="checkbox">
                          </div><!-- end form-check -->
                        </div><!-- end d-flex -->
                      </div>
                    </div><!-- end form-item -->
                  </div>
                  <div class="form-item mb-4">
                    <div class="mb-4">
                      <div class="d-flex align-items-center justify-content-between">
                        <div class="me-2">
                          <h5 class="mb-1">Anonymous votes</h5>
                          <p class="form-text">Voter IDs will be anonymized in the backend</p>
                        </div>
                        <div class="form-check form-switch form-switch-s1">
                          <input v-model="form.isAnonymous" :disabled="Boolean(currentPoll)" class="form-check-input"
                                 type="checkbox">
                        </div><!-- end form-check -->
                      </div><!-- end d-flex -->
                    </div>
                  </div><!-- end form-item -->
                  <ValidationProvider v-slot="{ errors }" rules="" slim>
                    <div class="form-item mb-4">
                      <h5 :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-1">Choose min participation</h5>
                      <p :class="{ 'text-danger': Boolean(errors[0]) }" class="form-text mb-3">Select the minimum
                        duration of staked participation required to vote.</p>
                      <v-select v-model="form.minRounds" :class="!errors[0] ? '' : 'is-invalid'"
                                :clearable=false :disabled="Boolean(currentPoll)" :options="minParticipationOptions"
                                :reduce="option => option.value" class="generic-select"
                                label="label" placeholder="Select Minimum Participation"></v-select>
                      <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                    </div><!-- end form-item -->
                  </ValidationProvider>
                  <ValidationProvider v-slot="{ errors }" rules="integer|min_value:0" slim>
                    <div class="form-item mb-4">
                      <div class="mb-4">
                        <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Stake basis
                          round</label>
                        <input v-model="form.stakeBasisRound" :class="!errors[0] ? '' : 'is-invalid'"
                               :disabled="Boolean(currentPoll)"
                               class="form-control form-control-s1" min="0"
                               placeholder="(Optional) Use Stake Snapshot as of Tournament Round" type="number">
                        <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                      </div>
                    </div><!-- end form-item -->
                  </ValidationProvider>
                  <ValidationProvider v-slot="{ errors }" rules="decimal|min_value:0" slim>
                    <div class="form-item mb-4">
                      <div class="mb-4">
                        <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Min stake</label>
                        <input v-model="form.minStake" :class="!errors[0] ? '' : 'is-invalid'"
                               :disabled="Boolean(currentPoll)"
                               class="form-control form-control-s1" min="0" placeholder="(Optional) Minimum Staked NMR Required for Voter"
                               step=0.0001 type="number">
                        <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                      </div>
                    </div><!-- end form-item -->
                  </ValidationProvider>
                  <ValidationProvider v-slot="{ errors }" rules="decimal|min_value:0" slim>
                    <div class="form-item mb-4">
                      <div class="mb-4">
                        <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Clipping for low
                          stake</label>
                        <input v-model="form.clipLow" :class="!errors[0] ? '' : 'is-invalid'"
                               :disabled="Boolean(currentPoll)"
                               class="form-control form-control-s1" min="0" placeholder="(Optional) Clip lower NMR values to this value"
                               step=0.0001 type="number">
                        <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                      </div>
                    </div><!-- end form-item -->
                  </ValidationProvider>
                  <ValidationProvider v-slot="{ errors }" rules="decimal|min_value:0" slim>
                    <div class="form-item mb-4">
                      <div class="mb-4">
                        <label :class="{ 'text-danger': Boolean(errors[0]) }" class="mb-2 form-label">Clipping for high
                          stake</label>
                        <input v-model="form.clipHigh" :class="!errors[0] ? '' : 'is-invalid'"
                               :disabled="Boolean(currentPoll)"
                               class="form-control form-control-s1" min="0" placeholder="(Optional) Clip higher NMR values to this value"
                               step=0.0001 type="number">
                        <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                      </div>
                    </div><!-- end form-item -->
                  </ValidationProvider>
                </div>
                <div class="form-item mb-4">
                  <h5 class="mb-3">Select mode</h5>
                  <ul id="myTab" class="row g-3 nav nav-tabs nav-tabs-s2" role="tablist">
                    <li v-for="mode in weightModes" :key="mode.id"
                        class="nav-item col-4 col-sm-4 col-lg-3 tooltip-s1" role="presentation">
                      <button :id="mode.value" :class="form.weightMode === mode.value ? 'active':''" :disabled="Boolean(currentPoll)"
                              class="nav-link" data-bs-toggle="tab" type="button"
                              @click="form.weightMode = mode.value">
                        <span class="tooltip-s1-text tooltip-s1-text-lg tooltip-text">{{ mode.description }}</span>
                        <em :class="mode.icon" class="ni nav-link-icon"></em>
                        <span class="nav-link-title mt-1 d-block">{{ mode.title }}</span>
                      </button>
                    </li>
                  </ul>
                </div><!-- end form-item -->
                <div class="form-item mb-4">
                  <h5 class="mb-3">Poll options</h5>
                  <div v-for="(option, index) in form.options" :key="index" class="row">
                    <div class="col-11">
                      <ValidationProvider v-slot="{ errors }" rules="required" slim>
                        <div class="form-item mb-4">
                          <div class="mb-4">
                            <input v-model="option.text" :class="!errors[0] ? '' : 'is-invalid'"
                                   class="form-control form-control-s1" placeholder="Option" type="text">
                            <div :class="{ 'show': Boolean(errors[0]) }" class="text-danger fade">{{ errors[0] }}</div>
                          </div>
                        </div><!-- end form-item -->
                      </ValidationProvider>
                    </div>
                    <div class="col-1">
                      <button class="icon-btn ms-auto" title="Delete" type="button" @click="deleteOption(index)"><em
                        class="ni ni-trash"></em></button>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-12">
                      <button class="btn btn-outline-dark" type="button" @click="addOption"><em class="ni ni-plus"></em>
                        Add Option
                      </button>
                    </div>
                  </div>
                </div><!-- end form-item -->
                <div class="form-item">
                  <button :disabled="pollLoading" class="btn btn-dark" type="button" @click="handleSubmit(savePoll)">
                    <span v-if="pollLoading"><span class="spinner-border spinner-border-sm me-2" role="status"></span>Saving...</span>
                    <span v-else>Save</span>
                  </button>
                </div><!-- end form-item -->
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
import {ref} from '@vue/composition-api';
import {onSSR} from '@vue-storefront/core';
import {
  pollGetters,
  useGlobals,
  usePoll,
  useUser,
  userGetters
} from '@vue-storefront/numerbay';
import {useUiNotification} from '~/composables';

export default {
  name: 'CreatePoll',
  middleware: [
    'is-authenticated'
  ],
  data() {
    return {
      weightModes: [
        {
          id: 1,
          title: 'Equal Weights for All',
          description: 'Equal weights, allows non-staked participants to vote',
          value: 'equal',
          icon: 'ni-equal'
        },
        {
          id: 2,
          title: 'Equal Weights for Staked',
          description: 'Equal weights for all staked participants',
          value: 'equal_staked',
          icon: 'ni-equal'
        },
        {
          id: 3,
          title: 'Log Staked NMR',
          description: 'Log-transformed weights by NMR staked on models',
          value: 'log_numerai_stake',
          icon: 'ni-coins'
        }
      ],
      minParticipationOptions: [
        {label: 'All Active Participants', value: 0},
        {label: 'Min 3 Month Participation', value: 13},
        {label: 'Min 1 Year Participation', value: 52}
      ],
      optionForm: {},
      showAdvanced: false
    };
  },
  methods: {
    onIsMultipleChange(isMultiple) {
      if (!isMultiple) {
        this.form.maxOptions = null;
      }
    },
    onIsBlindChange(isBlind) {
      if (!isBlind) {
        this.form.isStakePredetermined = true;
      }
    },
    onPollsLoaded(polls) {
      this.currentPoll = polls?.data?.find((p) => String(p.id) === String(this.id));
      this.form = this.resetForm(this.currentPoll);
      this.showAdvanced = (this.form.isBlind) || (!this.form.isStakePredetermined) || (this.form.isAnonymous) || Number(this.form.minRounds) > 0 || Number(this.form.stakeBasisRound) > 0 || Number(this.form.minStake) > 0 || Number(this.form.clipLow) > 0 || Number(this.form.clipHigh) > 0;
    },
    deleteOption(index) {
      this.form.options.splice(index, 1);
    },
    addOption() {
      this.form.options.push({text: ''});
    }
  },
  watch: {
    polls(newPolls) {
      this.onPollsLoaded(newPolls);
    }
  },
  mounted() {
    if (this.id && !this.currentPoll) {
      this.onPollsLoaded(this.polls);
    }
  },
  setup(props, context) {
    const {id} = context.root.$route.params;
    const {user, load: loadUser, loading: userLoading} = useUser();
    const {globals, getGlobals} = useGlobals();
    const {
      polls,
      search: pollSearch,
      createPoll,
      updatePoll,
      deletePoll,
      loading: pollLoading,
      error: pollError
    } = usePoll('polls');
    const {send} = useUiNotification();

    const currentPoll = ref(null);

    onSSR(async () => {
      await loadUser();
      await pollSearch({filters: {user: {in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
      await getGlobals();

      if (id) {
        currentPoll.value = polls?.value?.data?.find((p) => String(p.id) === String(id));
      }
    });

    const resetForm = (poll) => ({
      topic: poll ? pollGetters.getTopic(poll) : null,
      id: poll ? pollGetters.getId(poll) : null,
      description: poll ? pollGetters.getDescription(poll) : null,
      dateFinish: poll?.date_finish ? (new Date(Date.parse(poll.date_finish))).toISOString().split('T')[0] : null,
      isMultiple: poll ? poll.is_multiple : false,
      maxOptions: poll ? poll.max_options : null,
      isAnonymous: poll ? poll.is_anonymous : false,
      isBlind: poll ? poll.is_blind : false,
      weightMode: poll ? pollGetters.getWeightMode(poll) : 'equal',
      isStakePredetermined: poll ? poll.is_stake_predetermined : true,
      stakeBasisRound: poll ? poll.stake_basis_round : null,
      minStake: poll ? poll.min_stake : null,
      minRounds: poll ? poll.min_rounds : 0,
      clipLow: poll ? poll.clip_low : null,
      clipHigh: poll ? poll.clip_high : null,
      options: poll ? poll.options : [{text: ''}, {text: ''}]
    });

    const form = ref(resetForm(currentPoll.value));

    const handleForm = (fn) => async () => {
      await fn({id: currentPoll.value ? currentPoll.value.id : null, poll: form.value});
      const hasPollErrors = pollError.value.pollModal;
      if (hasPollErrors) {
        send({
          message: pollError.value.pollModal?.message,
          type: 'bg-danger',
          icon: 'ni-alert-circle'
        });
        return;
      }

      await pollSearch({filters: {user: {in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
      await context.root.$router.push('/polls');
    };

    const savePoll = async () => {
      form.value.options.map((o, i) => o.value = i);
      if (!currentPoll.value) {
        return handleForm(createPoll)();
      } else {
        return handleForm(updatePoll)();
      }
    };

    return {
      id,
      currentPoll,
      form,
      globals,
      polls,
      pollLoading,
      user,
      userGetters,
      resetForm,
      savePoll
    };
  }
};
</script>

<style lang="scss" scoped>
.is-invalid::v-deep .vs__dropdown-toggle {
  border-color: #dc3545 !important;
  border-top-color: rgb(220, 53, 69) !important;
  border-right-color: rgb(220, 53, 69) !important;
  border-bottom-color: rgb(220, 53, 69) !important;
  border-left-color: rgb(220, 53, 69) !important;
}
</style>
