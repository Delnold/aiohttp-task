FROM python:3.10-slim
WORKDIR /aiohttp-task
COPY . /aiohttp-task
RUN pip install --no-cache-dir --upgrade -r requirements.txt
ENV PYTHONPATH=/aiohttp-task
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
CMD ["sh", "-c", "python /aiohttp-task/migrations/migrate.py && python /aiohttp-task/src/main.py"]
