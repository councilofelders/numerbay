import { CustomQuery, Context, FactoryParams } from '@vue-storefront/core';
import { Ref, computed } from '@vue/composition-api';
import { sharedRef, Logger, configureFactoryParams } from '@vue-storefront/core';
import { UsePoll, UsePollErrors } from '../types/composables';

export interface UsePollFactoryParams<POLLS, POLL_SEARCH_PARAMS extends any> extends FactoryParams {
  pollsSearch: (context: Context, params: POLL_SEARCH_PARAMS & { customQuery?: CustomQuery }) => Promise<POLLS>;
  createPoll: (context: Context, params: any) => Promise<any>;
  updatePoll: (context: Context, params: any) => Promise<any>;
  deletePoll: (context: Context, params: any) => Promise<any>;
  closePoll: (context: Context, params: any) => Promise<any>;
  vote: (context: Context, params: any) => Promise<any>;
}

export function usePollFactory<POLLS, POLL_SEARCH_PARAMS>(
  factoryParams: UsePollFactoryParams<POLLS, POLL_SEARCH_PARAMS>
) {
  return function usePoll(id: string): UsePoll<POLLS, POLL_SEARCH_PARAMS> {
    const polls: Ref<POLLS> = sharedRef([], `usePoll-polls-${id}`);
    const loading = sharedRef(false, `usePoll-loading-${id}`);
    const _factoryParams = configureFactoryParams(factoryParams);

    const errorsFactory = (): UsePollErrors => ({
      search: null,
      pollModal: null,
      voting: null
    });

    const error: Ref<UsePollErrors> = sharedRef(errorsFactory(), `usePoll-error-${id}`);

    const resetErrorValue = () => {
      error.value = errorsFactory();
    };

    const search = async (searchParams) => {
      Logger.debug(`usePoll/${id}/search`, searchParams);

      try {
        loading.value = true;
        polls.value = await _factoryParams.pollsSearch(searchParams);
        error.value.search = null;
      } catch (err) {
        error.value.search = err;
        Logger.error(`usePoll/${id}/search`, err);
      } finally {
        loading.value = false;
      }
    };

    const createPoll = async ({poll: providedPoll}) => {
      Logger.debug('usePollFactory.createPoll', providedPoll);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.createPoll({poll: providedPoll});
        error.value.pollModal = null;
      } catch (err) {
        error.value.pollModal = err;
        Logger.error('usePoll/createPoll', err);
      } finally {
        loading.value = false;
      }
    };

    const updatePoll = async ({id, poll: providedPoll}) => {
      Logger.debug('usePollFactory.updatePoll', providedPoll);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.updatePoll({id, poll: providedPoll});
        error.value.pollModal = null;
      } catch (err) {
        error.value.pollModal = err;
        Logger.error('usePoll/updatePoll', JSON.stringify(err));
      } finally {
        loading.value = false;
      }
    };

    const deletePoll = async ({id}) => {
      Logger.debug('usePollFactory.deletePoll', id);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.deletePoll({id});
        error.value.pollModal = null;
      } catch (err) {
        error.value.pollModal = err;
        Logger.error('usePoll/deletePoll', err);
      } finally {
        loading.value = false;
      }
    };

    const closePoll = async ({id}) => {
      Logger.debug('usePollFactory.closePoll', id);
      resetErrorValue();

      try {
        loading.value = true;
        await _factoryParams.closePoll({id});
        error.value.pollModal = null;
      } catch (err) {
        error.value.pollModal = err;
        Logger.error('usePoll/closePoll', err);
      } finally {
        loading.value = false;
      }
    };

    const vote = async ({id, options}) => {
      Logger.debug('usePollFactory.vote', options);
      resetErrorValue();

      try {
        loading.value = true;
        polls.value = await _factoryParams.vote({id, options});
        error.value.voting = null;
      } catch (err) {
        error.value.voting = err;
        Logger.error('usePoll/vote', JSON.stringify(err));
      } finally {
        loading.value = false;
      }
    };

    return {
      search,
      createPoll,
      updatePoll,
      deletePoll,
      closePoll,
      vote,
      polls: computed(() => polls.value),
      loading: computed(() => loading.value),
      error: computed(() => error.value)
    };
  };
}
