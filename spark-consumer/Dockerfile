FROM python:3.11-slim

WORKDIR /app

# Copy code
COPY insert-data-postgresDB.py /app/

# Install dependencies
RUN pip install --no-cache-dir psycopg2-binary pandas

# Mount CSV folder từ host
VOLUME ["/app/archive"]

CMD ["python", "/app/insert-data-postgresDB.py"]
