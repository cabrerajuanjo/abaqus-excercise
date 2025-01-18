FROM node:22 AS ui-build

WORKDIR /app/ui

COPY ./package.json ./package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

RUN ls

FROM nginx:1.27.2-alpine3.20-slim

COPY --from=ui-build /app/ui/dist /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d/default.conf
