import time

from celery import Celery

app = Celery('one', broker="amqp://guest:guest@localhost:5672")


@app.task(name="one.adding")
def add(a, b):
    time.sleep(5)
    return a + b
 