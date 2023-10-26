FROM python:3.9

WORKDIR /app
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1

# First copy only requirements.txt to cache dependencies independently
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 80

ENTRYPOINT ["python", "server.py"]

