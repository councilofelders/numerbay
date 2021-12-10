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
    // eslint-disable-next-line camelcase
    date_finish: params.dateFinish,
    // eslint-disable-next-line camelcase
    is_multiple: params.isMultiple,
    // eslint-disable-next-line camelcase
    max_options: params.maxOptions,
    // eslint-disable-next-line camelcase
    is_anonymous: params.isAnonymous,
    // eslint-disable-next-line camelcase
    is_blind: params.isBlind,
    // eslint-disable-next-line camelcase
    weight_mode: params.weightMode,
    // eslint-disable-next-line camelcase
    is_stake_predetermined: params.isStakePredetermined,
    // eslint-disable-next-line camelcase
    stake_basis_round: params.stakeBasisRound,
    // eslint-disable-next-line camelcase
    min_stake: params.minStake,
    // eslint-disable-next-line camelcase
    min_rounds: params.minRounds,
    // eslint-disable-next-line camelcase
    clip_low: params.clipLow,
    // eslint-disable-next-line camelcase
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

