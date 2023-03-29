#from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from aeneas.tools.execute_task import ExecuteTaskCLI
import requests
import json
import random
import os
import uuid
from datetime  import datetime
#from minio import Minio
def save_file(filename, data):
    with open("/tmp/"+filename, "wb") as out_file:
      out_file.write(data)
def handle(req):

    json_data = json.loads(req)
 #   json_data = data['body']
    json_data['metadata']["aeneas_entry"]= str(datetime.now())
    gateway=os.environ.get('gateway', 'gateway')
    json_data['metadata']["topic"] = "tocloud"
    
    json_data["metadata"]["getobject_text_start"]= str(datetime.now())
    file = requests.post("http://"+gateway+"/function/getobject",data="p001.xhtml")
    json_data["metadata"]["getobject_text_end"]= str(datetime.now())
    save_file("p001.xhtml",file.content)

    json_data["metadata"]["getobject_audio_start"]= str(datetime.now())
    audio = requests.post("http://"+gateway+"/function/getobject",data=json_data['metadata']['name'])
    json_data["metadata"]["getobject_audio_end"]= str(datetime.now())
    save_file("a.wav",audio.content)


    output = str(uuid.uuid4())
    ExecuteTaskCLI(use_sys=False).run(arguments=[None, u"/tmp/a.wav",u"/tmp/p001.xhtml",
    u"task_language=eng|is_text_type=plain|os_task_file_format=json",
    u"/tmp/"+output+".json"])

    json_data["metadata"]["aeneas_end"]= str(datetime.now())
    f = open("/tmp/"+output+".json")
    payload = json.loads(f.read())
    payload.update(json_data)
#    requests.post("http://"+gateway+"/function/pubrabbitmq",data=json.dumps(payload))
    return  json.dumps(payload)
