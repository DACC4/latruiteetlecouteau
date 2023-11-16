# Use Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install project dependencies
RUN pip install pyyaml

# Copy the Python script and YAML file into the container
COPY main.py .
COPY quotes.yaml .
COPY quotes.html .
COPY style.css .

# Expose the port the app runs on
EXPOSE 8080

# Run the Python script when the container launches
CMD ["python", "main.py"]