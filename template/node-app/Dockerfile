# Base image
FROM node:22-slim

# Working directory
WORKDIR /app

# Copy project files
COPY package.json /app/
COPY package-lock.json /app/

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Command to run the Node.js application
CMD ["node", "index.js"]