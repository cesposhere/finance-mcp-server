# Step 1: Use an official, lightweight Python runtime as a parent image
FROM python:3.12-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file into the container
COPY requirements.txt .

# Step 4: Install the specific dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the actual server script into the container
COPY server.py .

# Step 6: Run the server when the container launches
ENTRYPOINT ["python", "server.py"]