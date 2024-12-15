FROM python:3.11-alpine
COPY . /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["run.py"]
