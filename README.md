Congestion bottleneck is one of the common problems in high volume, realtime IoT data ingestions. Top causes include 

###### 1) Synchronous data uploads from multiple clients 
###### 2) Large data in the messages 
###### 3) Hytrogenious data formats 
###### 4) Heavy compression/decompression on the message bus and lastly 
###### 5) hardware and network bandwidth limitation 

Asynchronous multiprocessing message ingestion gateway is widly considered as an effective soltuion to alleviate congestion. This post illustrates a simple solution for distributed message gateway by leveraging Celery along with AMQP in Docker containers. 

![alt tag] (https://cloud.githubusercontent.com/assets/3374971/19624496/ed8770f0-98ad-11e6-85f2-11e965c49405.png)
