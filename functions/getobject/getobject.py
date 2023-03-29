import os
import json
from datetime import datetime
from minio import Minio
import time
def handle(req):
     dt = datetime.today()
     file = time.time_ns()
     minio = os.getenv("minio",'172.17.141.197:9001')
     accesskey = os.getenv("access_key",'minio')
     secretkey = os.getenv("secret_key",'minio123')
     mc = Minio(minio,
                 access_key=accesskey,
                  secret_key=secretkey,
                  secure=False)
     mc.fget_object("aeneas", req, "/tmp/"+req+str(file))
     with open("/tmp/"+req+str(file),'rb') as f:
         contents = f.read()
     return contents