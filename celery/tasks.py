from celery import Celery
import redis



app = Celery('tasks', broker='redis://localhost:6379')



@app.task
def add(x, y):
    return x + y