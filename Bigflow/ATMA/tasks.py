from __future__ import absolute_import, unicode_literals
from celery import task, shared_task
from celery.task import periodic_task
# @shared_task()
from celery.schedules import crontab
@periodic_task(run_every=crontab(minute='09', hour='14'))
def task_number_one():
    print('vikkki')
    print("vsolv")