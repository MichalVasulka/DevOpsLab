# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy the Flask application files to the container
COPY app.py /app/app.py

# Install Flask and dependencies
RUN pip3 install Flask

# Expose port 5000
EXPOSE 5000

# Command to run the Flask application
CMD ["python3", "app.py"]
