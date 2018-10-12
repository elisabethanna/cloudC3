from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('counter', broker='pyamqp://', backend='rpc://', include=['cloudC3.tasks'])

app.conf.update(result_expires=3600)

if __name__ == '__main__':
    app.start()
