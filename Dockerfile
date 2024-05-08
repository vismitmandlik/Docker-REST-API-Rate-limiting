# Use Python 3.8 image
FROM python:3.8

# Set working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the source code into the container
COPY . .

# Command to run the API
CMD ["python", "app.py"]
