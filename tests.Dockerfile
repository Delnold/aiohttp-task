FROM python:3.10
WORKDIR /aiohttp-task_tests
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
ENV PYTHONPATH=/aiohttp-task_tests
ENV PYTHONUNBUFFERED=1
CMD ["pytest", "tests/"]