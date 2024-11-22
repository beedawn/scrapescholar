FROM node:alpine

# Install curl
RUN apk add --no-cache curl

# Set working directory and install dependencies
WORKDIR /app
COPY package*.json ./
RUN npm install

# Copy the rest of your application
COPY . .

# Expose the port your app will run on
EXPOSE 3000

# Command to run your application
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]
