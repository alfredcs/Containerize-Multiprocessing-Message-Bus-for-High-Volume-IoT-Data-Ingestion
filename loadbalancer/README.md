#### Start load balancer containers on multiple nodes

docker run -d --hostname lb01 --name lb01 -v /usr/local/etc/haproxy/haproxy.cfg.rabbitmq:/usr/local/etc/haproxy/haproxy.cfg -p 15672:15672 -p19042:19042 bootstrap.crd.xx.com:5000/haproxy:1.6
