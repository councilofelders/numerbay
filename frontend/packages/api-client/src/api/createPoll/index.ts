import { CustomQuery } from '@vue-storefront/core';
import { authHeaders } from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function createPoll(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('polls/', context.config.api.url);
  const token = context.config.auth.onTokenRead();

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const payload = {
    id: params.id,
    topic: params.topic,
    description: params.description,
    date_finish: params.dateFinish,
    is_multiple: params.isMultiple,
    max_options: params.maxOptions,
    is_nonymous: params.isAnonymous,
    is_blind: params.isBlind,
    weight_mode: params.weightMode,
    is_stake_predetermined: params.isStakePredetermined,
    min_stake: params.minStake,
    min_rounds: params.minRounds,
    clip_low: params.clipLow,
    clip_high: params.clipHigh,
    options: params.options
  };

  // Use axios to send a POST request
  const { data } = await context.client.post(url.href, payload, authHeaders(token)).catch((error) => {
    if (error.response) {
      error.response.data.error = error.response.status;
      return error.response;
    }
  });
  // Return data from the API
  return data;
}

