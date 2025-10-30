"""
Gunicorn configuration for Appointment360
"""
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 300  # 5 minutes for CSV processing
keepalive = 5

# Logging
accesslog = os.path.join(os.path.dirname(__file__), 'logs', 'gunicorn_access.log')
errorlog = os.path.join(os.path.dirname(__file__), 'logs', 'gunicorn_error.log')
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'appointment360'

# Server mechanics
daemon = False
pidfile = '/tmp/gunicorn.pid'
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (uncomment for HTTPS)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

