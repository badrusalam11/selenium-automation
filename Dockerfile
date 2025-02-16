# Use Python 3.13-slim as the base image
FROM python:3.13-slim

# Install system dependencies required for Google Chrome and Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
 && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update \
 && apt-get install -y google-chrome-stable

# Install Chromedriver
# Ensure that the CHROMEDRIVER_VERSION is compatible with the installed version of Google Chrome.
ENV CHROMEDRIVER_VERSION 114.0.5735.90
RUN wget -q --continue -P /tmp https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip \
 && unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ \
 && rm /tmp/chromedriver_linux64.zip \
 && chmod +x /usr/local/bin/chromedriver

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container
COPY . .

# Define the command to run your application
CMD ["python", "run.py", "regression"]
