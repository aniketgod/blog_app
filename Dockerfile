FROM python:3.10.0

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY authentication ./authentication
COPY application ./application
COPY blog ./blog
COPY celery ./celery
COPY utilis ./utilis
COPY cache ./cache
COPY main.py .
COPY .env .
CMD ["python", "main.py"]