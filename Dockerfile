FROM python:3.10.9-slim

WORKDIR /app

COPY /src /app/src
COPY /requirements-api.txt /app

RUN pip install --upgrade pip && \
    pip install -r requirements-api.txt

ENV PORT 8080

EXPOSE 8080

# alembic upgrade head && 
CMD ["sh", "-c", "uvicorn src.api.main:app --host 0.0.0.0 --port $PORT"]
