# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Metadata as defined at http://label-schema.org

LABEL maintainer="your-email@example.com" \
    version="1.0" \
    description="This is a Flask application running on Docker."

# The environment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED=1

# create root directory for our project in the container
WORKDIR /app

# set default environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install system dependencies
#RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get update

# Install python dependencies
RUN pip install --upgrade pip
# requirements do not change often, we can copy early
COPY requirements.txt .
RUN pip install -r requirements.txt



# Create a user to run our application. Use -M to not create a home directory and -r to create a system account

# adduser: This is the command to add a new user in a Linux system.
# --disabled-password: This option disables password login for the new user. This is useful for a Docker container as you typically don't need to log in.
# --gecos '': The gecos field is a set of comma-separated values that typically hold user information like a full name and contact details. In this case, we're setting it to an empty string because this information is not needed for the Docker container.
# --no-create-home: This option prevents the creation of a home directory for the new user. This is typically where user-specific configuration files are stored, but it's not needed for the Docker container.
# appuser: This is the name of the new user.
RUN adduser --disabled-password --gecos '' --no-create-home appuser

# copy code at later stages, so we do not invalidate cached layers
# Add current directory code to working directory
ADD . /app

# Change the ownership of our applications files to the newly created user
RUN chown -R appuser:appuser /app

# deactivate root user within container
RUN usermod -s /usr/sbin/nologin root

# Switch to unprivileged appuser
USER appuser

# Expose port 8000 to the Docker host, so we can access it
# from the outside.
EXPOSE 8000

# During runtime, this command will run
CMD ["flask", "run", "-p", "8000"]



------------------------------------------------


# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Metadata as defined at http://label-schema.org
LABEL maintainer="your-email@example.com" \
      version="1.0" \
      description="This is a Flask application running on Docker."

# The environment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED=1

# create root directory for our project in the container
WORKDIR /app


# set default environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --upgrade pip
# requirements do not change often, we can copy early
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create a user to run our application. Use -M to not create a home directory and -r to create a system account

# adduser: This is the command to add a new user in a Linux system.
# --disabled-password: This option disables password login for the new user. This is useful for a Docker container as you typically don't need to log in.
# --gecos '': The gecos field is a set of comma-separated values that typically hold user information like a full name and contact details. In this case, we're setting it to an empty string because this information is not needed for the Docker container.
# --no-create-home: This option prevents the creation of a home directory for the new user. This is typically where user-specific configuration files are stored, but it's not needed for the Docker container.
# appuser: This is the name of the new user.

RUN adduser --disabled-password --gecos '' --no-create-home appuser

# copy code at later stages, so we do not invalidate cached layers
# Add current directory code to working directory
ADD . /app

# Change the ownership of our applications files to the newly created user
RUN chown -R appuser:appuser /app


# Set root login to nologin
RUN usermod -s /usr/sbin/nologin root

# Switch to appuser
USER appuser

# Expose port 8000 to the Docker host, so we can access it
# from the outside.
EXPOSE 8000

# Healthcheck with retries and grace period
HEALTHCHECK --start-period=10s --retries=3 CMD curl --fail http://localhost:8000 || exit 1

# During runtime, this command will run
CMD ["flask", "run", "-p", "8000"]
