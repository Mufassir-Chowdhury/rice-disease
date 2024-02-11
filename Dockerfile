# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Expose port 3000 to the outside world
EXPOSE 3000

# Run app.py when the container launches
CMD ["python", "-m", "http.server", "3000"]