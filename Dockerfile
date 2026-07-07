# Dockerfile for Scheduled Concurrent Agent
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY scheduled_concurrent_agent.py .

# Create workspace directory
RUN mkdir -p /app/workspace

# Set environment variables
ENV LLM_API_KEY=""
ENV LLM_MODEL="claude-sonnet-4-5-20250929"
ENV PYTHONUNBUFFERED=1

# Run agent in interactive mode
CMD ["python", "scheduled_concurrent_agent.py", "--interactive"]
