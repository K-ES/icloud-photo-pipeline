FROM python:3.12-slim

WORKDIR /app

# небуферизованный stdout → видно в docker logs
ENV PYTHONUNBUFFERED=1

# контракт
ENV PHOTO_OPT_INPUT_DIR=/input
ENV PHOTO_OPT_OUTPUT_DIR=/output

COPY unzip_zip.py .

CMD ["python", "unzip_zip.py"]
