# Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /parksense

# Install system packages for image creation
RUN apt-get update && apt-get install -y gcc

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose the port Cloud Run uses
EXPOSE 8080

# Run FastAPI app with Uvicorn and Cloud Run listen on port 8080
RUN chmod +x run_parksense.sh
CMD ["./run_parksense.sh"]
