# build stage
FROM node:20-bookworm-slim as build-stage

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@10.33.0 --activate

COPY ./package.json /app/
COPY ./pnpm-lock.yaml /app/pnpm-lock.yaml
RUN pnpm install --frozen-lockfile

COPY ./public /app/public
COPY ./src /app/src
COPY ./babel.config.js /app/babel.config.js
COPY ./vue.config.js /app/vue.config.js
COPY ./jsconfig.json /app/jsconfig.json

ARG VUE_APP_HOST
ENV VUE_APP_HOST=$VUE_APP_HOST

RUN pnpm run build

FROM nginx:alpine

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]