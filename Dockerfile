# Use a lightweight Python base image with Debian base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file (if you have one)
COPY requirements.txt ./

# Update package lists and install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-flask \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the application's port (default Flask port is 5000)
EXPOSE 5000

# Set the environment variable to ensure Flask listens on all interfaces
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the Flask application
CMD ["flask", "run"]
