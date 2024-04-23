# Use Python image as the base
FROM python:3.8-slim-buster

# Metadata as defined at http://label-schema.org
LABEL maintainer="your-email@example.com" \
      version="2.0" \
      description="This is a Flask application running on Docker."




# Set working directory
WORKDIR /app

COPY requirements.txt .

# Install Flask and dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Flask application files to the container
# fast dev lifecycle of this image layer
COPY app.py /app/app.py

# Expose port 5100
EXPOSE 5100


# Healthcheck with retries and grace period
HEALTHCHECK --start-period=10s --retries=3 CMD curl --fail http://localhost:5100/health || exit 1

# Command to run the Flask application
CMD ["python3", "app.py"]
