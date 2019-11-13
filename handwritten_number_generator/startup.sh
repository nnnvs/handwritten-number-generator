#!/bin/bash
nohup gunicorn api_controller:app \
	--log-level=DEBUG \
	--error-logfile config/gunicorn-logs.log \
	--access-logfile config/gunicorn-digit-logs.log \
	-t 600 \
	-k gevent \
	-b localhost:5000 \
	--reload \
	--workers 4 \
	&>config/gunicorn_nohup.out&