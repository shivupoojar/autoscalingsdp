from minio import Minio
import json
from random import randrange
import os
import io
import time 
def handle(req):
     minio = os.getenv("minio",'172.17.141.197:9001')
     accesskey = os.getenv("access_key",'minio')
     secretkey = os.getenv("secret_key",'minio123')
     mc = Minio(minio,access_key=accesskey,secret_key=secretkey,secure=False)
     res = json.loads(req)
#     res = data['body']
     filename = res['metadata']['user_id']
     json_file = json.dumps(res)
     data = json_file.encode('utf-8')
     data_stream = io.BytesIO(data)
#     f = open("/tmp/dict.json","w")
#     f.write(json_file)
#     f.close()
     mc.put_object('aeneas-output',str(filename)+'.json',data_stream, length=len(data))
     return json_file

