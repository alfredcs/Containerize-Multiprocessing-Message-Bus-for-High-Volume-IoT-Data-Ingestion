#!/bin/bash
celery worker --workdir=/opt/amqp -A amqp_pub -n 1.$(hostname) --loglevel=info
