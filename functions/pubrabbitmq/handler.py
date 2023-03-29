#from aeneas.executetask import ExecuteTask
import requests
import json
import random
import os
import pika
import time
from pika.exceptions import AMQPError
from datetime import datetime

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    gateway=os.environ.get('gateway', '172.17.141.197:8080')
    data = json.loads(req)
    topic = data['metadata']['topic']
    data['metadata']["pubrabbitmq_entry"] = str(datetime.now())  
    exchange = os.environ.get('exchange','Dex')
    RABBITMQ_CONNECTION = os.environ.get('RABBITMQ_CONNECTION','amqp://guest:guest@172.17.141.197:5672')
    params = pika.URLParameters(RABBITMQ_CONNECTION)
    _connection = pika.BlockingConnection(params)
    _channel = _connection.channel()
    data['metadata']["pubrabbitmq_exit"] = str(datetime.now())
    _channel.basic_publish('', topic, json.dumps(data))
    return str(data)
