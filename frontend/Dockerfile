# Build stage
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci --legacy-peer-deps || npm install --legacy-peer-deps

COPY . .

# Build-time env for React (CRA embeds REACT_APP_* at build)
ARG REACT_APP_BASE_URL=/api/v1
ARG REACT_APP_GITHUB_CLIENT_ID=
ARG REACT_APP_GOOGLE_CLIENT_ID=
ARG REACT_APP_REDIRECT_URI=

ENV REACT_APP_BASE_URL=$REACT_APP_BASE_URL \
    REACT_APP_GITHUB_CLIENT_ID=$REACT_APP_GITHUB_CLIENT_ID \
    REACT_APP_GOOGLE_CLIENT_ID=$REACT_APP_GOOGLE_CLIENT_ID \
    REACT_APP_REDIRECT_URI=$REACT_APP_REDIRECT_URI

RUN npm run build

# Runtime: nginx serves static SPA
FROM nginx:1.27-alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
