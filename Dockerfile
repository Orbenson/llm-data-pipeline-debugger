# Dockerfile
FROM python:3.9-slim

# Set a working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port 8501 for Streamlit (if using the web UI)
EXPOSE 8501

# Set environment variable for production (if needed)
ENV PYTHONUNBUFFERED=1

# Default command: launch the CLI. To run the web UI, override the command.
CMD ["python", "cli.py", "--config", "config.yaml"]
