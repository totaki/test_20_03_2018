FROM node

RUN yarn global add serve
RUN mkdir /srv/app
WORKDIR /srv/app

RUN cd /srv/app
COPY ./yarn.lock /srv/app/yarn.lock
COPY ./package.json /srv/app/package.json
RUN yarn install


COPY ./src /srv/app/src
COPY ./public /srv/app/public
RUN yarn build
EXPOSE 5000
CMD serve -s build
