# Use an official Python runtime as a parent image
FROM library/python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Install required C++11 libraries and ca-certificates
RUN apt-get update \
      && apt-get install -y \
          --no-install-recommends \
            build-essential \
            python3-dev \
            ca-certificates \
            curl \
      && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run main when the container launches
ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:5000", "--master", "-p", "2", "-w", "main:app"]
USER nobody



# Dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start server
CMD python manage.py migrate && \
    gunicorn config.wsgi:application --bind 0.0.0.0:$PORT