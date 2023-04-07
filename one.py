import time
from celery.utils.log import get_task_logger
from celery import Celery

app = Celery('one', broker="amqp://guest:guest@localhost:5672")
logger = get_task_logger(__name__)


@app.task(name="one.adding", bind=True)
def add(self, a, b):
    time.sleep(5)
    print(self.request)
    return a + b


@app.task(name='one.divide', bind=True, default_retry_delay=300)
def divide(self, a, b):
    try:
        return a / b
    except ZeroDivisionError:
        logger.info('sorry..')
        self.retry(countdown=10, max_retries=2)
