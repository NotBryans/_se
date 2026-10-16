FROM python:3.11-slim

WORKDIR /app

# Install Flask and PostgreSQL driver
RUN pip install --no-cache-dir flask psycopg2-binary

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]