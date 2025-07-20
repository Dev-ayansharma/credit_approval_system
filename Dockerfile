# Dockerfile
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Run Django server using Gunicorn
CMD ["gunicorn", "credit_system.wsgi:application", "--bind", "0.0.0.0:8000"]
