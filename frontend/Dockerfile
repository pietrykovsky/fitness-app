# Use the official Node.js image from DockerHub
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app/frontend

# Copy package.json and package-lock.json
COPY ./package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the frontend files
COPY ./ ./

# If DEV is false, create a production build
CMD if [ "$DEV" = "false" ] ; then npm run build && npm install -g serve && serve -s build ; fi

# If DEV=true, we'll run the React development server
CMD if [ "$DEV" = "true" ] ; then npm start ; fi
