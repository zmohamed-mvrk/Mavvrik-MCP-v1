# Use an official lightweight Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN pip install uv

# Copy dependency definition
COPY pyproject.toml .

# Install dependencies
RUN uv pip install --system -r pyproject.toml

# Copy source code
COPY src/ src/

# Create a non-root user for security
RUN useradd -m appuser
USER appuser

# Expose port (default for SSE)
EXPOSE 8000

# Start command (Remote/Production Mode)
CMD ["uv", "run", "src/server.py", "--transport", "sse", "--port", "8000", "--host", "0.0.0.0"]