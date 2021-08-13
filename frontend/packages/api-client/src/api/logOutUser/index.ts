import { CustomQuery } from '@vue-storefront/core';

// eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/explicit-module-boundary-types
export default async function logOutUser(context, params, customQuery?: CustomQuery) {
  await context.config.auth.onTokenRemove();
}

