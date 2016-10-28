from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from datetime import datetime


class rabbit2cass(object):
    """
	  Configure Log
    """
    log = logging.getLogger()
    log.setLevel('INFO')
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    log.addHandler(handler)


    def __init__(self,queue_name, exchange_name):
        """
        """
	self.log = logging.getLogger()
    	self.log.setLevel('INFO')
	self.s_list=[]
    	self.handler = logging.StreamHandler()
    	self.handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    	self.log.addHandler(self.handler)
        super(rabbit2cass,self).__init__()
	# Write to a temp csv file
	self.f_handle=open('/tmp/stock_daily.csv', 'w+')
	self.f_handle.write("symbol,tradetime,open,high,low,close,volume"+'\n')
        # Set up the Rabbit connection
        self.username="guest"
        self.password="guest"
	self.queue_name=queue_name if len(queue_name) > 1 else 'yfinance'
	self.exchange_name=exchange_name if len(exchange_name) > 1 else 'realtime_stocks'
        self.amqp_host="172.20.13.162"
        self.port='5672'
	self.credentials = pika.PlainCredentials(self.username, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.amqp_host, credentials=self.credentials))
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)

	# Connect to Cassandra
	self.cassandra_connect('stocks', 'realtime_yfinance')
	#self.batch = BatchStatement()
        # Declare this process's queue
	self.channel.exchange_declare(exchange=self.exchange_name, exchange_type="direct", passive=False, durable=True, auto_delete=False)
	self.cluster = Cluster(["172.20.13.168", "172.20.13.167", "172.20.13.166"], port=9042)
        self.session = self.cluster.connect('stocks')
        #self.rows = self.session.execute_async("select sector from symbols")
        #self.sectors = self.dedupe(self.rows.result())
	#for self.sector in self.sectors:
        #  if self.sector[0] != "Technology": continue
	#  self.query = "SELECT symbol from symbols where sector='"+ self.sector[0] +"' ALLOW FILTERING"
        #  self.rows = self.session.execute_async(self.query)
        #  self.symbols=self.dedupe(self.rows.result())
	try:
        #    for self.symbol in self.symbols:
            self.channel.queue_declare(queue=self.queue_name,auto_delete=True)
            self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange_name, routing_key=self.queue_name)
            self.channel.basic_consume(self.callback, queue=self.queue_name, no_ack=True)
            print(' [*] Waiting for messages. To exit press CTRL+C')
            self.channel.start_consuming()
        except Exception as e:
            print str(e)
            print "Consume Failed!"
            self.channel.stop_consuming()
        self.connection.close()
	self.f_handle.close()

    def dedupe(self,seq):
        self.seen = set()
        self.seen_add = self.seen.add
        return [x for x in seq if not (x in self.seen or self.seen_add(x))]

    def callback(self,ch,method,props,body):
        """
        """
	#print(" [x] Received  %r" % ( body))
	#self.cassandra_insert('realtime_quotes', body)
	#print("-----")
        try:
        #  self.cassandra_insert(header,msg)
	  self.cassandra_insert('realtime_yfinance', body)
	  if body not in self.s_list:
	    self.f_handle.write(body+'\n')
	    self.s_list.append(body)
        except Exception:
          print "Cassandra connection failed. Will retry soon..."
          ch.basic_nack(delivery_tag = method.delivery_tag)
          time.sleep(1)
          self.cassandra_connect('stocks', 'realtime_yfinance')
          return

    def cassandra_insert(self,table,data):
        """
            Insert a list of data into the currently connected Cassandra database.
        """
	#import pdb; pdb.set_trace()
        try:
	    #self.fields=data.split(',')
	    self.fields=json.loads(data)
	    n_Symbol=self.fields['Symbol'].replace("\"","")
	    n_Date=self.fields['Date'].replace("\"","")
	    n_TradeTime=self.fields['Tradetime'].replace("\"","")
	    map(lambda x: self.fields.pop(x, None), ['Symbol', 'Tradetime', 'Date'])
            self.query = SimpleStatement("""
                INSERT INTO realtime_yfinance (symbol, date, tradetime, values)
                VALUES (%(symbol)s, %(date)s, %(tradetime)s, %(values)s)
                """, consistency_level=ConsistencyLevel.ONE)
            #self.log.info("inserting into %s" % table)
            self.session.execute(self.query, dict(symbol=n_Symbol, date=n_Date, tradetime=n_TradeTime, values=str(self.fields)))

        except Exception as e:
            raise


    def cassandra_connect(self, keyspaceName, tableName):
        """
            Try to establish a new connection to Cassandra.
        """
        try:
            self.cluster.shutdown()
        except:
            pass
        #self.cluster = Cluster(contact_points=[CASSANDRA_IP])
	self.cluster = Cluster(['172.20.13.163', '172.20.13.164', '172.20.13.165'], port=9042)

        try: # Might not immediately connect. That's fine. It'll try again if/when it needs to.
            self.session = self.cluster.connect(keyspaceName)
        except:
            print "WARNING: Cassandra connection to " + "CASSANDRA_IP" + " failed."
            print "The process will attempt to re-connect at a later time."

	self.rows = self.session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
	if keyspaceName not in [row[0] for row in self.rows]:
          self.log.info("creating keyspace...")
          self.session.execute("""
                CREATE KEYSPACE %s
                WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                """ % keyspaceName)
        self.rows =  self.session.execute("SELECT table_name FROM system_schema.tables")
        if tableName not in [row[0] for row in self.rows]:
          self.log.info("creating keyspace...")
          self.session.execute("""
                CREATE table %s (
                symbol text,
                date text,
                tradetime  text,
                values text,
                PRIMARY KEY (symbol, date, tradetime)
                )
                """ % tableName)
	else:
	  print("Table "+tableName+" has already existed!")


def main(args_str=None):
    rabbit2cass("", "")

if __name__ == "__main__":
    main()
