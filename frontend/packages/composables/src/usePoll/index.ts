import {Context, Logger} from '@vue-storefront/core';
import { usePollFactory, UsePollFactoryParams } from '../factories/usePollFactory';

const params: UsePollFactoryParams<any, any> = {
  pollsSearch: async (context: Context, params: any): Promise<any> => {
    Logger.debug('getPolls');
    return await context.$numerbay.api.getPoll(params);
  },

  createPoll: async (context: Context, {poll}) => {
    Logger.debug('createPoll');
    const response = await context.$numerbay.api.createPoll(poll);
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  updatePoll: async (context: Context, {id, poll}) => {
    Logger.debug('updatePoll');
    poll.id = id;
    const response = await context.$numerbay.api.updatePoll(poll);
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  },

  deletePoll: async (context: Context, {id}) => {
    Logger.debug('deletePoll');
    const response = await context.$numerbay.api.deletePoll({id});
    if (response?.error) {
      throw new Error(response.detail);
    }
    return response;
  }
};

export default usePollFactory<any, any>(params);
