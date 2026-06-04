FROM python:3.10-alpine

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .

# FIX: Upgrade pip, setuptools, and wheel to the latest secure versions before installing requirements
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ .

# Expose port for the application
EXPOSE 5000

# Run the application via gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]