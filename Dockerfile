FROM python:3.9

WORKDIR /app
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
RUN pip uninstall aiogram==3.0.5b aiohttp==3.8.3
# First copy only requirements.txt to cache dependencies independently
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 80
EXPOSE 443

ENTRYPOINT ["python", "server_2.py"]

