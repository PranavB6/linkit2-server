# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install PDM
RUN pip install pdm

# Copy the current directory contents into the container at /app
COPY . ./

# Install dependencies
RUN pdm install

# Command to run the FastAPI app with uvicorn
CMD ["pdm", "run", "start"]
