# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install the necessary Python packages
RUN pip install --no-cache-dir requests discord.py Flask

# Run bot.py when the container launches
CMD ["python", "./bot.py"]
