# Use an official Node.js runtime as the base image
FROM node:14 as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the Svelte application
RUN npm run build

# Copy the built SvelteKit files from .svelte-kit/output directory
COPY .svelte-kit/output ./public

# Use NGINX as the web server
FROM nginx:alpine

# Copy the built SvelteKit files to NGINX HTML directory
COPY --from=build /app/public /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Command to run NGINX
CMD ["nginx", "-g", "daemon off;"]
