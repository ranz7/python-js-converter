# Stage 1: Build React frontend
FROM node:16 AS frontend-builder

# Set working directory
WORKDIR /src/frontend

# Copy package.json and install dependencies
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install

# Copy the rest of the frontend code
COPY frontend/ ./

# Build the frontend
RUN yarn build

# Stage 2: Build Python backend with ANTLR
FROM python:3.9 AS backend-builder

# Set working directory
WORKDIR /src/backend

# Copy requirements and install dependencies
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt

# Install ANTLR
RUN pip install antlr4-python3-runtime

# Copy the rest of the backend code
COPY backend/ ./

# Optionally, run ANTLR to generate the parser
# (This assumes you have ANTLR grammar files in the backend/ directory)
RUN java -jar /path/to/antlr-4.x-complete.jar -Dlanguage=Python3 -o generated/ your_grammar.g4

# Stage 3: Final stage to combine frontend and backend
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the backend code and dependencies from the backend-builder stage
COPY --from=backend-builder /src/backend /src/backend

# Copy the built frontend from the frontend-builder stage
COPY --from=frontend-builder /src/frontend/build /src/frontend/build

# Set the working directory to the backend
WORKDIR /src/backend

# Expose the port the app runs on
EXPOSE 8000

# Set the environment variable to indicate the production environment
ENV PYTHONUNBUFFERED=1

# Run the backend server
CMD ["python", "app.py"]
