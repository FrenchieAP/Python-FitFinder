# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app files into the container
COPY . .

# Expose the port the app will run on
EXPOSE 80

# Start the Flask app
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:80", "server:app", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-"]
