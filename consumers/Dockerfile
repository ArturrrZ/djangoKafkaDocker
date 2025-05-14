FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /consumer
RUN pip install kafka-python
COPY consumer1.py .
CMD [ "python", "consumer1.py" ]
