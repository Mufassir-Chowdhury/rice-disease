# Use an official lightweight Nginx image
FROM nginx:alpine

# Copy static files into the container
COPY . /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 3000