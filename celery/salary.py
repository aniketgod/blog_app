from celery import Celery

app = Celery('salary', broker='redis://localhost')



@app.task
def add(x, y):
    return x + y