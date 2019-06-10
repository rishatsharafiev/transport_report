from celery import shared_task


@shared_task
def hello_periodic_task():
    """Periodic task"""
    return 'hello'
