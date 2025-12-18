# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy only the script
COPY heartbeat.py .

# Run the script when container starts
CMD ["python", "heartbeat.py"]
