# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get clean

# Set working directory
WORKDIR /app

# Copy the Flask application files to the container
#COPY app.py /app/app.py
COPY . .

# Install Flask and dependencies
RUN pip3 install Flask

# Expose port 5100
EXPOSE 5100

# Command to run the Flask application
CMD ["python3", "app.py"]
