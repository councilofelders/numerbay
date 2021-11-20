<template>
  <SfModal
    v-e2e="'poll-modal'"
    :visible="isPollModalOpen"
    class="modal"
    @close="togglePollModal"
  >
    <template #modal-bar>
      <SfBar
        class="sf-modal__bar smartphone-only"
        :close="true"
        :title="currentPoll?`Editing Poll`:'New Poll'"
        @click:close="togglePollModal"
      />
    </template>
    <transition name="sf-fade" mode="out-in">
      <SfTabs :open-tab="1">
        <SfTab :title="currentPoll?`Editing Poll`:'New Poll'">
          <div>
            <ValidationObserver v-slot="{ handleSubmit }" key="log-in">
              <div class="form">
<!--                <ValidationProvider rules="required" v-slot="{ errors }">
                  <SfSelect label="Category" v-model="form.category" v-e2e="'listing-modal-category'"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]" :disabled="!!currentPoll" required @input="onCategoryChange">
                    <SfSelectOption value=""></SfSelectOption>
                    <SfSelectOption v-for="category in leafCategories" :key="category.id" :value="category.id">{{category.slug}}</SfSelectOption>
                  </SfSelect>
                </ValidationProvider>-->
                <ValidationProvider rules="required|min:2" v-slot="{ errors }">
                  <SfInput
                    v-model="form.topic"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="name"
                    label="Poll Topic, Cannot be Changed Later"
                    class="form__element"
                    :disabled="!!currentPoll"
                  />
                </ValidationProvider>
                <ValidationProvider rules="min:2|alpha_dash" v-slot="{ errors }">
                  <SfInput
                    v-model="form.id"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="id"
                    label="(Optional) Custom Poll ID for Shorthand URL, Cannot be Changed Later"
                    class="form__element"
                    :disabled="!!currentPoll"
                  />
                </ValidationProvider>
                <ValidationProvider rules="min:2" v-slot="{ errors }">
                  <SfInput
                    v-model="form.description"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="description"
                    label="(Optional) Description"
                    class="form__element"
                  />
                </ValidationProvider>
                <ValidationProvider rules="required" v-slot="{ errors }">
                  <SfInput
                    v-model="form.dateFinish"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="name"
                    type="date"
                    label="End Date (UTC)"
                    class="form__element"
                  />
                </ValidationProvider>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isMultiple"
                      value="false"
                      label="Single Choice"
                      details="Voter can only choose one option, this cannot be changed later"
                      v-model="form.isMultiple"
                      @change="onIsMultipleChange(form.isMultiple)"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                    <SfRadio
                      name="isMultiple"
                      value="true"
                      label="Multiple Choice"
                      details="Voter can choose options up to the limit below, this cannot be changed later"
                      v-model="form.isMultiple"
                      @change="onIsMultipleChange(form.isMultiple)"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                  </ValidationProvider>
                </div>
                <div v-if="form.isMultiple === 'true'">
                  <ValidationProvider rules="integer|required|min_value:0"  v-slot="{ errors }">
                    <SfInput
                      v-model="form.maxOptions"
                      :valid="!errors[0]"
                      :errorMessage="errors[0]"
                      name="maxOptions"
                      label="Maximum Options for a Vote, Cannot be Changed Later"
                      type="number"
                      step=1.0
                      class="form__element"
                      :disabled="!!currentPoll"
                    />
                  </ValidationProvider>
                </div>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isAnonymous"
                      value="true"
                      label="Anonymous Votes"
                      details="Voter IDs will be anonymized"
                      v-model="form.isAnonymous"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                    <SfRadio
                      name="isAnonymous"
                      value="false"
                      label="Named Votes"
                      details="Voter IDs will be plain Numerai usernames"
                      v-model="form.isAnonymous"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                  </ValidationProvider>
                </div>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isBlind"
                      value="true"
                      label="Blind Results"
                      details="Results will be kept blind until poll ends"
                      v-model="form.isBlind"
                      @change="onIsBlindChange(form.isBlind)"
                      class="form__radio"
                    />
                    <SfRadio
                      name="isBlind"
                      value="false"
                      label="Observable Results"
                      details="Results will be visible to voters anytime"
                      v-model="form.isBlind"
                      @change="onIsBlindChange(form.isBlind)"
                      class="form__radio"
                    />
                  </ValidationProvider>
                </div>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="weightMode"
                      value="equal"
                      label="Equal Weights"
                      details="Equal weights for all voters"
                      v-model="form.weightMode"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                    <SfRadio
                      name="weightMode"
                      value="log_numerai_stake"
                      label="Log Staked NMR"
                      details="Log-transformed weights by NMR staked on models"
                      v-model="form.weightMode"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                    <SfRadio
                      name="weightMode"
                      value="log_numerai_balance"
                      label="Log Numerai Balance"
                      details="Log-transformed weights by NMR balance in Numerai wallet [Coming Soon]"
                      v-model="form.weightMode"
                      class="form__radio"
                      disabled
                    />
                    <SfRadio
                      name="weightMode"
                      value="log_balance"
                      label="Log Balance"
                      details="Log-transformed weights by NMR balance in any wallet [Coming Soon]"
                      v-model="form.weightMode"
                      class="form__radio"
                      disabled
                    />
<!--                    <SfRadio
                      name="weightMode"
                      value="log_clip"
                      label="Log Weighted with Clipping"
                      details="Log-transformed weights by NMR stake or balance, clipped by min or max weight"
                      v-model="form.weightMode"
                      class="form__radio"
                    />-->
                  </ValidationProvider>
                </div>
<!--                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isNumeraiOnly"
                      value="stake"
                      label="Numerai Staked Only"
                      details="Weighting based only on staked NMR amount in Numerai accounts"
                      v-model="form.isNumeraiOnly"
                      class="form__radio"
                    />
                    <SfRadio
                      name="isNumeraiOnly"
                      value="numerai_total"
                      label="Numerai Total Balance"
                      details="Weighting based on all available NMR amount in Numerai accounts"
                      v-model="form.isNumeraiOnly"
                      class="form__radio"
                    />
                    <SfRadio
                      name="isNumeraiOnly"
                      value="total"
                      label="Total Balance"
                      details="Weighting based on available NMR amount in any wallet (Coming soon)"
                      v-model="form.isNumeraiOnly"
                      class="form__radio"
                      disabled
                    />
                  </ValidationProvider>
                </div>-->
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="isStakePredetermined"
                      value="true"
                      label="Pre-determine Stake"
                      details="NMR stake and balance will be snapshotted before poll creation, this cannot be changed later"
                      v-model="form.isStakePredetermined"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                    <SfRadio
                      name="isStakePredetermined"
                      value="false"
                      label="Post-determine Stake"
                      details="NMR stake and balance will be snapshotted after poll ends, this cannot be changed later [Coming Soon]"
                      v-model="form.isStakePredetermined"
                      class="form__radio"
                      :disabled="!!currentPoll || form.isBlind === 'false' || true"
                    />
                  </ValidationProvider>
                </div>
                <div class="form__radio-group">
                  <ValidationProvider v-slot="{ errors }" class="form__horizontal">
                    <SfRadio
                      name="minRounds"
                      value="0"
                      label="All Active Participants"
                      details="No minimum staked rounds requirement"
                      v-model="form.minRounds"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                    <SfRadio
                      name="minRounds"
                      value="13"
                      label="Min 3 Month Participation"
                      details="Requires staked participation for the past 13 weeks"
                      v-model="form.minRounds"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                    <SfRadio
                      name="minRounds"
                      value="52"
                      label="Min 1 Year Participation"
                      details="Requires staked participation for the past 52 weeks"
                      v-model="form.minRounds"
                      class="form__radio"
                      :disabled="!!currentPoll"
                    />
                  </ValidationProvider>
                </div>
                <!--<ValidationProvider rules="integer|min_value:0"  v-slot="{ errors }">
                  <SfInput
                    v-model="form.minRounds"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="minRounds"
                    label="(Optional) Minimum Staked & Resolved Rounds Required for Voter"
                    type="number"
                    step=1.0
                    min=0
                    class="form__element"
                    :disabled="!!currentPoll"
                  />
                </ValidationProvider>-->
                <ValidationProvider rules="decimal|min_value:0"  v-slot="{ errors }">
                  <SfInput
                    v-model="form.minStake"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="minStake"
                    label="(Optional) Minimum Staked NMR Required for Voter"
                    type="number"
                    step=0.0001
                    min=0
                    class="form__element"
                    :disabled="!!currentPoll"
                  />
                </ValidationProvider>
                <ValidationProvider rules="decimal|min_value:0"  v-slot="{ errors }">
                  <SfInput
                    v-model="form.clipLow"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="clipLow"
                    label="(Optional) Clip lower NMR values to this value"
                    type="number"
                    step=0.0001
                    min=0
                    class="form__element"
                    :disabled="!!currentPoll"
                  />
                </ValidationProvider>
                <ValidationProvider rules="decimal|min_value:0"  v-slot="{ errors }">
                  <SfInput
                    v-model="form.clipHigh"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="clipHigh"
                    label="(Optional) Clip higher NMR values to this value"
                    type="number"
                    step=0.0001
                    min=0
                    class="form__element"
                    :disabled="!!currentPoll"
                  />
                </ValidationProvider>
                <SfTable class="orders">
                  <SfTableHeading>
                    <SfTableHeader>Option</SfTableHeader>
                    <SfTableHeader>Action</SfTableHeader>
                  </SfTableHeading>
                  <SfTableRow v-for="(option, index) in form.options" :key="index">
                    <SfTableData>
                      <ValidationProvider rules="required"  v-slot="{ errors }">
                        <SfInput
                          v-model="option.text"
                          :valid="!errors[0]"
                          :errorMessage="errors[0]"
                          name="option"
                          label="Option"
                          class="form__element"
                        />
                      </ValidationProvider>
                    </SfTableData>
                    <SfTableData class="orders__view orders__element--right">
                      <div class="listing-actions">
                        <SfButton class="sf-button--text action__element" @click="deleteOption(index)">
                          {{ $t('Delete') }}
                        </SfButton>
                      </div>
                    </SfTableData>
                  </SfTableRow>
                  <SfTableRow>
                    <SfTableData>
                      <SfButton
                        class="action-button color-secondary"
                        data-testid="add-new-option"
                        @click="addOption"
                        type="button"
                      >Add Option</SfButton>
                    </SfTableData>
<!--                    <SfTableData class="orders__view orders__element&#45;&#45;right">
                      <div class="listing-actions">
                        <SfButton class="sf-button&#45;&#45;text action__element" @click="deleteOption(option.value)">
                          {{ $t('Delete') }}
                        </SfButton>
                      </div>
                    </SfTableData>-->
                  </SfTableRow>
                </SfTable>
<!--                <ProductOptionsForm
                  ref="optionsForm"
                  optionsTabTitle="Poll options"
                  changeOptionTabTitle="Update option"
                  :options="form.options"
                  transition="sf-fade"
                  changeOptionDescription="Update pricing option."
                  changeButtonText="Change"
                  deleteButtonText="Delete"
                  addNewOptionButtonText="Add new option"
                  updateOptionButtonText="Update option"
                  selectLabel="Country"
                  optionsTabDescription="Manage all the pricing options, the first one will be the default for buyers. Please save the overall form after modifying options."
                  :user="user"
                  :category="form.category"
                  :isTournamentCategory="isTournamentCategory(form.category)"
                  :isSubmissionCategory="isSubmissionCategory(form.category)"
                  :isPerRoundCategory="isPerRoundCategory(form.category)"
                ></ProductOptionsForm>-->
                <!--<ValidationProvider v-slot="{ errors }">
                  <SfTextarea
                    v-e2e="'listing-modal-description'"
                    v-model="form.description"
                    :valid="!errors[0]"
                    :errorMessage="errors[0]"
                    name="description"
                    label="Description"
                    class="form__element"
                    :cols="60"
                    :rows="10"
                  />
                </ValidationProvider>-->
                <div v-if="error.listingModal">
                  {{ error.listingModal }}
                </div>
                <SfButton v-e2e="'listing-modal-submit'"
                  type="submit"
                  class="sf-button--full-width"
                  :disabled="loading || !!numeraiError.getModels || !(form.options && form.options.length > 0)"
                  v-if="!currentPoll"
                  @click="handleSubmit(handlePollForm)"
                >
                  <SfLoader :class="{ loader: loading }" :loading="loading">
                    <div>{{ $t('Save') }}</div>
                  </SfLoader>
                </SfButton>
                <div class="form__horizontal" v-if="!!currentPoll">
                  <SfButton v-e2e="'listing-modal-submit'"
                    type="submit"
                    class="sf-button form__button"
                    :disabled="loading || !!numeraiError.getModels || !(form.options && form.options.length > 0)"
                    @click="handleSubmit(handlePollForm)"
                  >
                    <SfLoader :class="{ loader: loading }" :loading="loading">
                      <div>{{ $t('Save') }}</div>
                    </SfLoader>
                  </SfButton>
                  <SfButton v-e2e="'listing-modal-submit'"
                    type="button"
                    class="sf-button color-danger"
                    :disabled="loading || !!numeraiError.getModels"
                    @click="handleDeletePoll"
                  >
                    <SfLoader :class="{ loader: loading }" :loading="loading">
                      <div>{{ $t('Delete') }}</div>
                    </SfLoader>
                  </SfButton>
                </div>
              </div>
            </ValidationObserver>
            <div class="bottom">
            </div>
          </div>
        </SfTab>
      </SfTabs>
    </transition>
  </SfModal>
</template>
<script>
import { ref, watch, reactive, computed } from '@vue/composition-api';
import { SfModal, SfTabs, SfInput, SfTextarea, SfSelect, SfButton, SfCheckbox, SfLoader, SfAlert, SfBar, SfRadio, SfBadge, SfTable } from '@storefront-ui/vue';
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate';
// eslint-disable-next-line camelcase
import { required, min_value, integer, min, alpha_dash } from 'vee-validate/dist/rules';
import {
  userGetters,
  pollGetters,
  productGetters,
  useUser,
  useCategory,
  usePoll,
  useProduct,
  useNumerai,
  useGlobals
} from '@vue-storefront/numerbay';
import { onSSR } from '@vue-storefront/core';
import { useUiState } from '~/composables';
import ProductOptionsForm from '~/components/ProductOptionsForm';

extend('required', {
  ...required,
  message: 'This field is required'
});

extend('min_value', {
  // eslint-disable-next-line camelcase
  ...min_value,
  message: 'This must be greater than 1'
});

extend('integer', {
  ...integer,
  message: 'This field must be an integer'
});

extend('decimal', {
  validate: (value, { decimals = '*', separator = '.' } = {}) => {
    if (value === null || value === undefined || value === '') {
      return {
        valid: false
      };
    }
    if (Number(decimals) === 0) {
      return {
        valid: /^-?\d*$/.test(value)
      };
    }
    const regexPart = decimals === '*' ? '+' : `{1,${decimals}}`;
    const regex = new RegExp(`^[-+]?\\d*(\\${separator}\\d${regexPart})?([eE]{1}[-]?\\d+)?$`);

    return {
      valid: regex.test(value)
    };
  },
  message: 'The {_field_} field must contain only decimal values'
});

extend('url', {
  validate: (value) => {
    if (value) {
      // eslint-disable-next-line
      return /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(value);
    }

    return false;
  },
  message: 'This must be a valid URL'
});

extend('secureUrl', {
  validate: (value) => {
    if (value) {
      // eslint-disable-next-line
      return /^(https:\/\/www\.|https:\/\/)[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(value);
    }

    return false;
  },
  message: 'This must be a valid HTTPS URL'
});

extend('min', {
  ...min,
  message: 'The field should have at least {length} characters'
});

extend('alpha_dash', {
  // eslint-disable-next-line camelcase
  ...alpha_dash,
  message: 'The field should only contain alphabetic characters, numbers, dashes or underscores'
});

export default {
  name: 'PollModal',
  components: {
    SfModal,
    SfTabs,
    SfInput,
    SfTextarea,
    SfSelect,
    SfButton,
    SfCheckbox,
    SfLoader,
    SfAlert,
    SfBar,
    SfRadio,
    SfBadge,
    SfTable,
    ProductOptionsForm,
    ValidationProvider,
    ValidationObserver
  },
  methods: {
    isSubmissionCategory(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c=>c.id === Number(categoryId))[0];
        return category?.is_submission;
      }
      return false;
    },
    isPerRoundCategory(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c=>c.id === Number(categoryId))[0];
        return category?.is_per_round;
      }
      return false;
    },
    isTournamentCategory(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c=>c.id === Number(categoryId))[0];
        if (Boolean(category) && Boolean(category.tournament)) {
          return true;
        }
      }
      return false;
    },
    onCategoryChange(categoryId) {
      const category = this.leafCategories.filter(c=>c.id === Number(categoryId))[0];

      if (category) {
        this.form.options = (this.currentPoll?.options ? this.currentPoll?.options : (this.form?.options || [])).filter((option) => {
          if (!category.tournament) {
            this.$refs.optionsForm.isOnPlatform = 'false';
            return !option.is_on_platform;
          }
          if (option.is_on_platform && !category.is_submission) {
            this.$refs.optionsForm.mode = 'file';
            return option.mode === 'file';
          }
          return true;
        });
      }
    },
    getFilteredModels(categoryId) {
      if (categoryId) {
        const category = this.leafCategories.filter(c=>c.id === Number(categoryId))[0];
        let tournament = 8;
        if (category.slug.startsWith('signals-')) {
          tournament = 11;
        }
        const models = userGetters.getModels(this.numerai, tournament, false);
        return models;
      }
      return [];
    },
    onPlatformChange(isOnPlatform) {
      if (isOnPlatform === 'true') {
        this.form.currency = 'NMR';
        this.form.wallet = this.currentPoll ? this.currentPoll.wallet : null;
        this.form.mode = this.currentPoll?.mode || 'file';
        this.form.stakeLimit = this.currentPoll?.stake_limit;
      } else {
        this.form.currency = 'USD';
        this.form.wallet = null;
        this.form.mode = null;
        this.form.stakeLimit = null;
      }
    },
    onIsMultipleChange(isMultiple) {
      if (isMultiple === 'false') {
        this.form.maxOptions = null;
      }
    },
    onIsBlindChange(isBlind) {
      if (isBlind === 'false') {
        this.form.isStakePredetermined = 'true';
      }
    },
    encodeURL() {
      if (this.form.avatar) {
        this.form.avatar = encodeURI(decodeURI(this.form.avatar));
      }
      if (this.form.thirdPartyUrl) {
        this.form.thirdPartyUrl = encodeURI(decodeURI(this.form.thirdPartyUrl));
      }
    },
    deleteOption(index) {
      this.form.options.splice(index, 1);
    },
    addOption() {
      this.form.options.push({'text': ''})
    }
  },
  setup() {
    const { isPollModalOpen, currentPoll, togglePollModal } = useUiState();
    const { categories, search: categorySearch } = useCategory();
    const { search: pollSearch, createPoll, updatePoll, deletePoll, loading, error: pollError } = usePoll('polls');
    const { numerai, error: numeraiError } = useNumerai('my-listings');
    const { user } = useUser();
    const { globals } = useGlobals();
    onSSR(async () => {
      await categorySearch();
    });

    const resetForm = (poll) => ({
      topic: poll ? pollGetters.getTopic(poll) : null,
      id: poll ? pollGetters.getId(poll) : null,
      description: poll ? pollGetters.getDescription(poll) : null,
      dateFinish: poll?.date_finish ? (new Date(Date.parse(poll.date_finish))).toISOString().split('T')[0] : null,
      isMultiple: poll ? String(poll.is_multiple) : 'false',
      maxOptions: poll ? poll.max_options : null,
      isAnonymous: poll ? String(poll.is_anonymous) : 'true',
      isBlind: poll ? String(poll.is_blind) : 'true',
      weightMode: poll ? pollGetters.getWeightMode(poll) : 'equal',
      isStakePredetermined: poll ? String(poll.is_stake_predetermined) : 'true',
      minStake: poll ? poll.min_stake : null,
      minRounds: poll ? String(poll.min_rounds) : '0',
      clipLow: poll ? poll.clip_low : null,
      clipHigh: poll ? poll.clip_high : null,
      // expirationRound: pollGetters.getExpirationRound(poll),
      options: poll ? poll.options : [{"text":""}, {"text":""}]
    });
    const form = ref(resetForm(currentPoll));

    const error = reactive({
      listingModal: null
    });

    const resetErrorValues = () => {
      error.listingModal = null;
    };

    watch(currentPoll, (poll) => {
      if (currentPoll) {
        form.value = resetForm(poll);
        resetErrorValues();
      }
    });

    const handleForm = (fn) => async () => {
      resetErrorValues();
      await fn({ id: currentPoll.value ? currentPoll.value.id : null, poll: form.value });

      const hasPollErrors = pollError.value.listingModal;
      if (hasPollErrors) {
        error.listingModal = pollError.value.listingModal?.message;
        return;
      }

      togglePollModal();

      await pollSearch({filters: { user: { in: [`${userGetters.getId(user.value)}`]}}, sort: 'latest'});
    };

    const handlePollForm = async () => {
      form.value.options.map((o, i)=>o.value=i);

      if (!currentPoll.value) {
        return handleForm(createPoll)();
      } else {
        return handleForm(updatePoll)();
      }
    };

    const handleDeletePoll = async () => handleForm(deletePoll)();

    return {
      form,
      error,
      user,
      pollError,
      loading,
      isPollModalOpen,
      currentPoll,
      togglePollModal,
      userGetters,
      globals,
      numerai: computed(() => numerai ? numerai.value : null),
      numeraiError,
      leafCategories: computed(() => categories ? categories.value.filter((category) => {
        return category.items.length === 0;
      }).sort((a, b) => -a.slug.localeCompare(b.slug)) : []),
      resetForm,
      handlePollForm,
      deletePoll,
      handleDeletePoll
    };
  }
};
</script>

<style lang="scss" scoped>

.modal {
  --modal-index: 3;
  --overlay-z-index: 3;
  --modal-width: 70%;
  @include for-mobile {
    --modal-width: 100%;
  }
}
.form {
  margin-top: var(--spacer-sm);
  &__button {
    display: block;
    width: 100%;
    @include for-desktop {
      width: 17.5rem;
    }
  }
  &__element {
    margin: 0 0 var(--spacer-xl) 0;
  }
  &__horizontal {
    @include for-desktop {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
    }
    .form__element {
      @include for-desktop {
        flex: 1;
        margin-right: var(--spacer-2xl);
      }

      &:last-child {
        margin-right: 0;
      }
    }
  }
  &__radio {
    width: 50%;
    @include for-mobile {
      width: 100%
    }
  }
  &__radio-group {
    flex: 0 0 100%;
    margin: 0 0 var(--spacer-xl) 0;
    @include for-desktop {
      margin: 0 0 var(--spacer-xl) 0;
    }
  }
}
.action {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: var(--spacer-xl) 0 var(--spacer-xl) 0;
  font: var(--font-weight--light) var(--font-size--base) / 1.6 var(--font-family--secondary);
  & > * {
    margin: 0 0 0 var(--spacer-xs);
  }
}
.action {
  margin: var(--spacer-xl) 0 var(--spacer-xl) 0;
}
.checkbox {
  margin-bottom: var(--spacer-2xl);
}
.bottom {
  text-align: center;
  margin-bottom: var(--spacer-lg);
  font-size: var(--h3-font-size);
  font-weight: var(--font-weight--semibold);
  font-family: var(--font-family--secondary);
  &__paragraph {
    color: var(--c-primary);
    margin: 0 0 var(--spacer-base) 0;
    @include for-desktop {
      margin: 0;
    }
  }
}
.editor {
  margin: 0 0 var(--spacer-xl) 0;
  height: 300px;
  .quill-editor {
    height: 250px;
  }
}
.flag {
  margin-left: 0.4em;
  padding: 0.15em;
}
</style>
