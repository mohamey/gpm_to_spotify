FROM python:3.7-stretch

# Create the volumes for dev work
VOLUME ["/migrate-service", "/gmusicapi"]

# Change the Working Directory to our source code
WORKDIR /migrate-service

# replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# update the repository sources list
# and install dependencies
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get -y autoclean

# nvm environment variables
RUN mkdir /usr/local/nvm
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 12.14.1

# install nvm
RUN curl --silent -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.2/install.sh | bash

# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# confirm installation
RUN node -v
RUN npm -v

# Install Nodemon
RUN ["npm", "install", "-g", "nodemon"]

# Expose our Kafka Port
EXPOSE 9092

CMD [ "nodemon", "--watch", "../gmusicapi", "--exec", "./startService.sh" ]
