"""Gunicorn configuration for Contact Manager"""
import multiprocessing
import os

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
accesslog = '-'
errorlog = '-'
loglevel = 'info'
capture_output = True
enable_stdio_inheritance = True
preload_app = True

