FROM node:16.2.0-alpine3.13 as build-env
WORKDIR /app/
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

FROM alpine:3.13
WORKDIR /
COPY update-front-files.sh .
RUN chmod +x update-front-files.sh
COPY --from=build-env /app/build/ /app/
CMD /update-front-files.sh
