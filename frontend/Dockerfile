FROM node:21-alpine as build

WORKDIR /darwin

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

RUN echo $PORT

FROM nginx:stable-alpine

COPY --from=build /darwin/dist /usr/share/nginx/html

EXPOSE $PORT

COPY nginx.conf /etc/nginx/conf.d/default.conf

CMD sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'

# heroku container:push web -a darwin-interface && heroku container:release web -a darwin-interface && heroku logs --tail -a darwin-interface
