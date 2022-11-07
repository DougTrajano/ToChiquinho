FROM python:3.10.7-alpine3.16

WORKDIR /app
COPY . /app/

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt \
    && apk del .build-deps gcc libc-dev make

ENV PYTHONPATH=/app

EXPOSE 80

# alembic upgrade head && 
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
