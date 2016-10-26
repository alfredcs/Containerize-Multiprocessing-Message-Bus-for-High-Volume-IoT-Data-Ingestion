Congestion bottleneck is one of the common problems in high volume, realtime IoT data ingestions. Top causes include 

###### 1) Synchronous data uploads from multiple clients 
###### 2) Large data in the messages 
###### 3) Hytrogenious data formats 
###### 4) Heavy compression/decompression on the message bus and lastly 
###### 5) hardware and network bandwidth limitation 

Asynchronous multiprocessing message ingestion gateway is widly considered as an effective soltuion to alleviate congestion. This post illustrates a simple solution for distributed message gateway by leveraging Celery along with AMQP in Docker containers. 

![alt tag] (https://cloud.githubusercontent.com/assets/3374971/19624524/c38c4d74-98ae-11e6-9eac-230c3a474306.png)

#### Build Docker images for Python 2.7 with all needed packages, Rabbitmq and Cassandra along with Nginx and/or Haproxy for load balancing.

#### Developer worker/client(publisher) codes and make both container ready

#### Deploy a multi-node Rabbitmq clsuter and a multi-node Cassandra cluster based on the Docker images    

#### Deploy a multi-node load balancer cluster  to dispatching TCP requests based on Nginx or HAproxy Docker image 

#### Run multiple containerized workers 
The wrokers are multi-threaded processors runing in different conatiners on a distributed cluster. The worker processors respond to the client requests and perform asynchrnous data ingestion in high volume. Data from different clients are asynchrnously published on the AMQP in the distributed cluster and contents in the mesage queue iare replicated across multiple Rabbitmq instances.  

#### Simulate IoT data feeds from client (publisher) side by querying stock market data

#### Simulate ETL jobs by ennebling multiple data import processes in idifferent containers to process and store AMQP messages onto the corresponding Cassandra keyspaces.
