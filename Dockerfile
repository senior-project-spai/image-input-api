FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-alpine3.8

# Install python package first
COPY ./requirements.txt /.
RUN pip install -r /requirements.txt

COPY ./app /app