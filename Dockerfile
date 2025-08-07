FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/Pulso

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
