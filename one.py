import time
from celery.utils.log import get_task_logger
from celery import Celery, chain, group

app = Celery('one', broker="amqp://guest:guest@localhost:5672", backend='rpc://')

'''app.conf.update(
    task_time_limit=60,
    task_soft_time_limit=50,
    worker_concurrency=70,
    worker_prefetch_multiplier=1,
    task_ignore_result=True,
    task_always_eager=True,
    task_acks_late=True
)'''

logger = get_task_logger(__name__)


@app.task(name='one.adding')
def add(a, b):
    time.sleep(5)
    return a + b


@app.task(name='one.divide', bind=True, default_retry_delay=300)
def divide(self, a, b):
    try:
        return a / b
    except ZeroDivisionError:
        logger.info('sorry..')
        self.retry(countdown=10, max_retries=2)


@app.task(name='one.subbing')
def sub(a, b):
    return a - b


add.apply_async((8, 4), link=sub.signature((5, 3), immutable=True))

# chain
result = chain(add.s(3, 4), sub.s(6))
print(result().get())
# group
result2 = group(add.s(3, 4), sub.s(6, 4)).apply_async()
print(result2.get())
