from celery import Celery

app = Celery('amqp_pub', backend='rpc://', broker='amqp://guest:guest@172.20.12.161/')

@app.task(ignore_result=True)
def amqp_pub(username='guest', password='guest', amqp_host='127.0.0.1',amqp_port='5672',bodies=[], queue_name='yfinance'):
    if len(bodies) < 1 :
      return False
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=amqp_host, credentials=credentials))
    try:
      channel = connection.channel()
      properties = pika.BasicProperties(user_id=username)
      channel.exchange_declare(exchange='realtime_stocks', exchange_type="direct", passive=False, durable=True, auto_delete=False)
      channel.queue_declare(queue=queue_name,auto_delete=True)
      channel.queue_bind(queue=queue_name, exchange='realtime_stocks', routing_key=queue_name)
      for body in bodies:
        channel.basic_publish(exchange='realtime_stocks', routing_key=queue_name, body=body, properties=pika.BasicProperties(content_type='application/json'))
      return True
    except Exception as e:
      print str(e)
    connection.close()
