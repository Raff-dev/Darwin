FROM node:21-alpine as build

WORKDIR /darwin

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:stable-alpine

COPY --from=build /darwin/dist /usr/share/nginx/html

EXPOSE $PORT

CMD ["nginx", "-g", "daemon off;"]
