####  Steps
#####  1) Allocate VM resources to simupate clients
#####  2) Assign different sector for each and every client
#####  3) Run containerized image with slected sectors on each and every client
######     Example:
######	     docker run -d -v /home/ubuntu/bin:/opt/bin -u worker bootstrap.crd.xx.com:5000/python:2.7.1 python /opt/bin/stock_intraday_client.py Energy,Finance,Health,Industries,Capital,Consumer
