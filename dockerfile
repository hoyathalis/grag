# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only the required files
COPY requirements.txt .
COPY .env .
COPY firebase.json .
COPY app/ ./app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
