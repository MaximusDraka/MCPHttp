FROM python:3.13-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY main.py .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Expose port
EXPOSE 8000

# Run the server
CMD ["python", "main.py"]
