# Use Python 3.9 image as the base
FROM python:3.9

# Set working directory
WORKDIR /app

COPY requirements.txt .

# Install Flask and dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Flask application files to the container
# fast dev lifecycle of this image layer
COPY app.py /app/app.py

# Expose port 5000
EXPOSE 5000

# Command to run the Flask application
CMD ["python3", "app.py"]
