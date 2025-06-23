# Use a lightweight Python image
FROM python:3.13-slim

# System dependencies for Jupyter and others
RUN apt-get update && apt-get install -y \
build-essential \
git \
iproute2 \
curl \
&& rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /workspace

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt
