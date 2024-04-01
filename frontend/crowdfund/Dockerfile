# Use an official Node.js runtime as the base image
FROM node:lts-alpine

# install simple http server for serving static content
RUN npm install -g http-server

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Vue.js application
RUN npm run build

# Expose the port your Vue.js app runs on
EXPOSE 8080

# Define the command to run your Vue.js app
CMD [ "http-server", "dist" ]