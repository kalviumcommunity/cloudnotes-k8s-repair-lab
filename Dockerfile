FROM python:3.12.7-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY app/app.py /app/app.py

USER appuser

EXPOSE 5000

CMD ["python", "/app/app.py"]
