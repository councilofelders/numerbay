# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:12

WORKDIR /var/www

COPY yarn.lock .
COPY package*.json .
COPY packages/api-client/package*.json ./packages/api-client/
COPY packages/composables/package*.json ./packages/composables/
COPY packages/theme/package*.json ./packages/theme/

RUN yarn install

COPY . .

RUN yarn build && yarn cache clean --all

ARG FRONTEND_ENV=production

ENV VUE_APP_ENV=${FRONTEND_ENV}

ENTRYPOINT ["yarn", "start"]