# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files into the container
COPY . .

# Expose the port Django runs on
EXPOSE 8000

# Run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
