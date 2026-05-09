FROM python:3.13-slim

WORKDIR /app

# Install streamlit directly
RUN pip install --no-cache-dir streamlit

# Copy app
COPY . /app/

EXPOSE 8501

CMD ["streamlit", "run", "examples/app.py", "--server.port=8501", "--server.address=0.0.0.0"]