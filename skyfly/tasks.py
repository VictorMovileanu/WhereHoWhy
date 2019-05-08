from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def query_kiwi():
    print('doing query')
