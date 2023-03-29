import requests
import json
import random
import os
import time
import uuid
import io
from datetime import datetime

def handle(req):
    gateway=os.environ.get('gateway', '10.43.144.91:8080')
    data = json.loads(req)
    payload ={"metadata":{"user_id":data['user_id'],"name": data['name'],"topic":"aeneas", "rawaeneas": str(datetime.now())}}
#    requests.post("http://"+gateway+"/function/pubrabbitmq",data=json.dumps(payload))
    return json.dumps(payload)
