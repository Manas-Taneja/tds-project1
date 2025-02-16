# Use Python 3.13-slim
FROM python:3.13-slim

# Install system dependencies required by Pillow, build tools, and Node.js/npm for Prettier
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    nodejs \
    npm \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Ensure /data directory exists and is writable
RUN mkdir -p /data && chmod 777 /data

# Upgrade pip, setuptools, and wheel for Python 3.13 compatibility
RUN pip install --upgrade pip setuptools wheel

# Copy requirements file and install dependencies (unconstrained versions)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# (Optional) Verify Pillow installation
RUN python -c "from PIL import Image; print('Pillow installed:', Image.__version__)"

# Copy application code and modules (including the provided datagen.py)
COPY app.py .
COPY tasksA.py .
COPY tasksB.py .
COPY datagen.py .

# (Optional) Copy your local data folder if available; datagen.py will create the files if not present
COPY data /data

# Expose port 8000
EXPOSE 8000

# Run the API using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
