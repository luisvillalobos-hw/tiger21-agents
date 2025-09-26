# Multi-stage build: First stage for Python backend
FROM python:3.12-slim as backend-builder

# Install uv for Python dependency management
RUN pip install uv

# Set working directory for backend
WORKDIR /backend

# Copy Python project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY main.py config.py ./

# Create virtual environment and install dependencies
RUN uv venv && uv sync

# Second stage: Node.js for frontend with Python backend
FROM node:20-slim

# Install Python and pip for running the backend
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*

# Copy Python backend from first stage
COPY --from=backend-builder /backend /backend
COPY --from=backend-builder /backend/.venv /backend/.venv

# Install Python dependencies system-wide for production use
WORKDIR /backend
RUN python3 -m pip install crewai langchain-community langchain-google-genai python-dotenv requests beautifulsoup4

# Set working directory for frontend
WORKDIR /app

# Copy frontend package files
COPY frontend/package*.json ./

# Install ALL Node.js dependencies (including devDependencies for building)
RUN npm ci

# Copy frontend application code
COPY frontend/ ./

# Build the React application (this needs devDependencies)
RUN npm run build

# Remove devDependencies after build to reduce image size
RUN npm prune --production

# Copy environment file if it exists
COPY .env* ./

# Expose port
EXPOSE 8080

# Set production environment
ENV NODE_ENV=production
ENV PORT=8080
ENV ANALYSIS_PATH=/backend

# Start the server
CMD ["npm", "start"]