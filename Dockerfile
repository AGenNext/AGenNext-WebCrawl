FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python and streamlit
RUN pip install --no-cache-dir streamlit

# Copy application
COPY . /app/

# Expose port
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "examples/app.py", "--server.port=8501", "--server.address=0.0.0.0"]