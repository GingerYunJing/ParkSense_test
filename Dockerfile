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

# # Accept build arguments from GitHub Actions
# ARG MONGO_URI
# ARG MONGO_DB
# ARG SECRET_KEY

# # Set environment variables inside the container
# ENV MONGO_URI=$MONGO_URI
# ENV MONGO_DB=$MONGO_DB
# ENV SECRET_KEY=$SECRET_KEY


# Expose the port Cloud Run uses
EXPOSE 8080

# Make sure the entrypoint script is executable
RUN chmod +x run_parksense.sh

# Start the app
CMD ["./run_parksense.sh"]
