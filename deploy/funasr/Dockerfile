FROM python:3.12-slim
WORKDIR /service
RUN pip install --no-cache-dir funasr fastapi uvicorn python-multipart modelscope
COPY deploy/funasr/server.py ./server.py
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
