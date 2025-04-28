FROM node:18 AS builder
WORKDIR /app

ARG NODE_ENV
ENV NODE_ENV=$NODE_ENV

ARG REACT_APP_BASE_URL
ENV REACT_APP_BASE_URL=$REACT_APP_BASE_URL

COPY package*.json ./
RUN npm install

COPY . .

RUN if [ "$NODE_ENV" = "production" ]; then npm run build; fi

FROM nginx:alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

FROM node:18 AS development
WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
