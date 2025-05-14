# build stage
FROM node:20-bookworm-slim as build-stage

WORKDIR /app

COPY ./package.json /app/
COPY ./package-lock.json /app/package-lock.json
RUN npm install

COPY ./public /app/public
COPY ./src /app/src
COPY ./babel.config.js /app/babel.config.js
COPY ./vue.config.js /app/vue.config.js
COPY ./jsconfig.json /app/jsconfig.json

RUN npm run build

FROM nginx:alpine

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]