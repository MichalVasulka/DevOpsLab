# Use Python image as the base
FROM python:3.8-slim-buster

# Metadata as defined at http://label-schema.org
LABEL maintainer="your-email@example.com" \
      version="2.0" \
      description="This is a Flask application running on Docker."




# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application files to the container
# expecting templates to have slower layer lifecycle
COPY templates templates
COPY app.py .


# Expose port 8080
EXPOSE 8080

# Healthcheck with retries and grace period
HEALTHCHECK --start-period=10s --retries=3 CMD curl --fail http://localhost:8080/health || exit 1

# Command to run the Flask application
CMD ["python", "app.py"]
