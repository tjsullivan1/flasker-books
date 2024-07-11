# gunicorn.conf.py

max_requests = 1000
max_requests_jitter = 50

log_file = "-"

bind = "0.0.0.0:50505"

threads = 1

timeout = 120
