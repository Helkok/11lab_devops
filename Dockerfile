FROM python:3.12 AS builder

WORKDIR /usr/src/app

COPY requirements.txt .

COPY . .

FROM python:3.12

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /usr/src/app /usr/src/app

EXPOSE 80

ENTRYPOINT ["sh", "-c", "alembic upgrade heads && uvicorn main:app --host 0.0.0.0 --port 80"]