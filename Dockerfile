FROM python:3.10.8-slim

WORKDIR /app
COPY . /app/

ENV PORT 8080

EXPOSE 8080

# alembic upgrade head && 
CMD ["sh", "-c", "uvicorn src.api.main:app --host 0.0.0.0 --port $PORT"]
