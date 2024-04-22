# Use Python 3.9 image as the base
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements file
#COPY requirements.txt .
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application files to the container
#COPY app.py .
#COPY templates templates

# Expose port 80
EXPOSE 80

# Command to run the Flask application
CMD ["python", "app.py"]
