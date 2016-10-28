##### 1. Start multiple worker containers on different servers which have access to the Rabbitmq cluster
The worker containers will accept requests parallelly from different clients and post meassages on the designate queues.
###### Example: docker run -d --network pnet01 -v /usr/local/bin:/opt/amqp --hostname=ap01 --name=ap01 -u worker bootstrap.crd.xx.com:5000/python:2.7.1  /opt/amqp/run_amqp_pub_server.sh

##### 2. Start consumer containers on different servers which have access to the Cassandra cluster
The consumer will dequeue messages parallelly and upload the contents into Cassandra 
###### Example: docker run -d --network pnet02 -v /usr/local/bin:/opt/r2c -u worker bootstrap.crd.xx.com:5000/python:2.7.1 python /opt/r2c/r2c3.py 
