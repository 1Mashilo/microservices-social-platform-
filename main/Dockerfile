# Dockerfile Configuration
FROM python:3.12

# Set Python unbuffered mode
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the entire application code to the working directory
COPY . /app

# Set the default command
CMD ["python", "main.py"]
