import { CustomQuery } from '@vue-storefront/core';
import { authHeaders } from '../utils';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function userUpdateMe(context, params, customQuery?: CustomQuery) {
  // Create URL object containing full endpoint URL
  const url = new URL('users/me', context.config.api.url);
  const token = context.config.auth.onTokenRead();

  const payload = {
    username: params.username,
    password: params.password,
    email: params.email ? params.email : null,
    // eslint-disable-next-line camelcase
    social_discord: params.socialDiscord,
    // eslint-disable-next-line camelcase
    social_linkedin: params.socialLinkedIn,
    // eslint-disable-next-line camelcase
    social_twitter: params.socialTwitter,
    // eslint-disable-next-line camelcase
    social_website: params.socialWebsite,
    // eslint-disable-next-line camelcase
    numerai_api_key_public_id: params.numeraiApiKeyPublicId ? params.numeraiApiKeyPublicId : null,
    // eslint-disable-next-line camelcase
    numerai_api_key_secret: params.numeraiApiKeySecret ? params.numeraiApiKeySecret : null,
    // eslint-disable-next-line camelcase
    public_address: params.publicAddress,
    signature: params.signature,
    // eslint-disable-next-line camelcase
    public_key: params.publicKeyV2,
    // eslint-disable-next-line camelcase
    encrypted_private_key: params.encryptedPrivateKeyV2,
    factor: params.factor
  };

  // Use axios to send a PUT request
  const { data } = await context.client.put(url.href, payload, authHeaders(token)).catch((error) => {
    if (error.response) {
      error.response.data.error = error.response.status;
      return error.response;
    }
  });

  // Return data from the API
  return data;
}

