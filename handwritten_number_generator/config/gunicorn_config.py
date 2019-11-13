"""Gunicorn configuration."""

bind = '127.0.0.1:5000'

workers = 8
worker_class = 'gevent'
timeout = 7200

accesslog = '-'