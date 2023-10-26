FROM python:3.9

WORKDIR /app
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1

# First copy only requirements.txt to cache dependencies independently
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app


ENTRYPOINT ["python", "server.py"]

