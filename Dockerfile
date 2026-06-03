FROM python:3.12-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ .

# Expose port for the application
EXPOSE 5000

# Run the application via gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
