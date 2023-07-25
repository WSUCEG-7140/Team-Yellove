# Use the official Python 3.9 image as the base image for this container
FROM python:3.9

# Set environment variables to configure Python behavior
# PYTHONDONTWRITEBYTECODE prevents Python from creating .pyc files
# PYTHONUNBUFFERED ensures that Python output is sent directly to the terminal without buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file from the host (your local machine) to the container's /app/ directory
COPY requirements.txt /app/

# Install Python packages specified in requirements.txt
# --no-cache-dir disables caching to keep the image size smaller
# -r requirements.txt specifies the file to install dependencies from
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files from the host to the container's /app/ directory
COPY . /app/

# Change the working directory to /app/restaurant_management inside the container
WORKDIR /app/restaurant_management

# Expose port 8000 on the container to make it accessible from the host or other containers
EXPOSE 8000

# Define the command to start the Django development server when the container runs
# "python manage.py runserver 0.0.0.0:8000" starts the Django app and binds it to all available network interfaces
# allowing connections from outside the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
