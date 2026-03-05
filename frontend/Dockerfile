# Dockerfile frontend — Build React + serveur Nginx
# Étape 1 : on compile le React en fichiers statiques
FROM node:20-slim AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Étape 2 : on sert les fichiers compilés avec Nginx
# Nginx est un serveur web ultra-léger et rapide
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]