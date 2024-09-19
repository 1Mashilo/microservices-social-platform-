# Use the official Python 3.9 image as the base image
FROM python:3.9

# Set environment variable to ensure unbuffered output for logs
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file from the host to the container
COPY requirements.txt /app/requirements.txt

# Install the project dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Copy all files from the current directory on the host to the /app directory in the container
COPY . /app