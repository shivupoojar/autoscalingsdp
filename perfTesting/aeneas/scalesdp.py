import sys
import json
import  datetime
import os
from minio import Minio
import csv
import pandas as pd
import time
import subprocess
from subprocess import Popen, PIPE
import requests
from IPython.display import display
import numpy as np
from IPython import get_ipython
import subprocess
import time


with open('config.json') as f:
   config = json.load(f)
bucket_name = config['bucket']
minio_host=config['minio_host']
PROMETHEUS=config['PROMETHEUS']
approaches=config['approaches']

success_rate = pd.DataFrame()
import copy 
def getdataprometheus(url):
    headers= {"Accept": "application/json"}
    res = json.loads(requests.post(url=url, headers=headers).content.decode('utf8', 'ignore'))
    #data2=res.get('data').get('result')[0].get('values')
    data_dict={}
    metric_list = []
    # print(data['data']['result']['values'])
    # exit()
    for i in res['data']['result']:
        for j in i['values']:
            data_dict = copy.deepcopy(i['metric'])
            data_dict['time'] = j[0]
            data_dict['value'] = j[1]
            metric_list.append(data_dict)
    df_metric = pd.DataFrame(metric_list)
    return df_metric


def get_function_execution_time(cmd):
    with Popen(cmd, stdout=PIPE, stderr=None, shell=True) as process:
        return (process.communicate()[0].decode("utf-8"))

def delete_scaling(approach):
   if approach == 'no+keda':
      print("Deleting",approach)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd /home/ubuntu/rabbitmq-testing/sample-go-rabbitmq/deploy;sudo kubectl delete -f deploy-consumer-aeneas.yaml;sudo kubectl delete -f deploy-consumer-getobject.yaml;sudo kubectl delete -f deploy-consumer-rawaeneas.yml;sudo kubectl delete -f deploy-consumer-tocloud.yaml;"',shell=True)
   elif approach == 'keda+keda':
      print("Deleting",approach)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd /home/ubuntu/rabbitmq-testing/sample-go-rabbitmq/deploy;sudo kubectl delete -f deploy-consumer.yaml;"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd /home/ubuntu/rabbitmq-testing/sample-go-rabbitmq/deploy;sudo kubectl delete -f deploy-consumer-aeneas.yaml;sudo kubectl delete -f deploy-consumer-getobject.yaml;sudo kubectl delete -f deploy-consumer-rawaeneas.yml;sudo kubectl delete -f deploy-consumer-tocloud.yaml;"',shell=True)

   elif approach == 'no+k8shpa':
      print("Deleting",approach)
      subprocess.run('ssh ubuntu@172.17.141.197 "sudo kubectl delete hpa/aeneas -n openfaas-fn;sudo kubectl delete hpa/scaling-aeneas-tocloud -n openfaas-fn;sudo kubectl delete hpa/rawaeneas -n openfaas-fn;sudo kubectl delete hpa/getobject -n openfaas-fn;"',shell=True)
   elif approach == 'keda+k8shpa':
      print("Deleting",approach)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd /home/ubuntu/rabbitmq-testing/sample-go-rabbitmq/deploy;sudo kubectl delete -f deploy-consumer.yaml;"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "sudo kubectl delete hpa/aeneas -n openfaas-fn;sudo kubectl delete hpa/scaling-aeneas-tocloud -n openfaas-fn;sudo kubectl delete hpa/rawaeneas -n openfaas-fn;sudo kubectl delete hpa/getobject -n openfaas-fn;"',shell=True)
   elif approach == 'no+rps':
      print("Deleting",approach)
      subprocess.run('ssh ubuntu@172.17.141.197 "sudo kubectl scale --replicas=0 deployment alertmanager -n openfaas"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd scalingsdp;faas deploy  -f aeneas.yml  --env max_inflight=10 --annotation topic="aeneas" --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=1"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd scalingsdp;faas deploy  -f getobject.yml --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=1;faas deploy  -f rawaeneas.yml --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=1"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd scalingsdp;faas deploy  -f scaling-aeneas-tocloud.yml --env max_inflight=50  --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=1;"',shell=True)
   elif approach == 'keda+rps':
      print("Deleting",approach)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd /home/ubuntu/rabbitmq-testing/sample-go-rabbitmq/deploy;sudo kubectl delete -f deploy-consumer.yaml;"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "sudo kubectl scale --replicas=0 deployment alertmanager -n openfaas"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd scalingsdp;faas deploy  -f aeneas.yml  --env max_inflight=10 --annotation topic="aeneas" --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=1"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd scalingsdp;faas deploy  -f getobject.yml --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=1;faas deploy  -f rawaeneas.yml --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=1"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd scalingsdp;faas deploy  -f scaling-aeneas-tocloud.yml --env max_inflight=50  --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=1;"',shell=True)



def deploy_scaling(approach):
   if approach == 'no+keda':
      print("Configuring",approach)
      subprocess.run('ssh ubuntu@172.17.141.197 "sudo kubectl scale --replicas=1 deployment amqp-connector-aeneas -n openfaas"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd /home/ubuntu/rabbitmq-testing/sample-go-rabbitmq/deploy;sudo kubectl apply -f deploy-consumer-aeneas.yaml;sudo kubectl apply -f deploy-consumer-getobject.yaml;sudo kubectl apply -f deploy-consumer-rawaeneas.yml;sudo kubectl apply -f deploy-consumer-tocloud.yaml"',shell=True)
   elif approach == 'keda+keda':
      print("Configuring",approach)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd /home/ubuntu/rabbitmq-testing/sample-go-rabbitmq/deploy;sudo kubectl apply -f deploy-consumer.yaml"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd /home/ubuntu/rabbitmq-testing/sample-go-rabbitmq/deploy;sudo kubectl apply -f deploy-consumer-aeneas.yaml;sudo kubectl apply -f deploy-consumer-getobject.yaml;sudo kubectl apply -f deploy-consumer-rawaeneas.yml;sudo kubectl apply -f deploy-consumer-tocloud.yaml"',shell=True)
   elif approach == 'no+k8shpa':
      print("Configuring",approach)
      subprocess.run('ssh ubuntu@172.17.141.197 "sudo kubectl scale --replicas=1 deployment amqp-connector-aeneas -n openfaas"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "sudo kubectl autoscale deployment -n openfaas-fn aeneas --cpu-percent=50 --min=1 --max=10;sudo kubectl autoscale deployment -n openfaas-fn scaling-aeneas-tocloud --cpu-percent=50 --min=1 --max=10;sudo kubectl autoscale deployment -n openfaas-fn rawaeneas --cpu-percent=50 --min=1 --max=5;sudo kubectl autoscale deployment -n openfaas-fn getobject --cpu-percent=50 --min=1 --max=5;"',shell=True)
   elif approach == 'keda+k8shpa':
      print("Configuring",approach)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd /home/ubuntu/rabbitmq-testing/sample-go-rabbitmq/deploy;sudo kubectl apply -f deploy-consumer.yaml"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "sudo kubectl autoscale deployment -n openfaas-fn aeneas --cpu-percent=50 --min=1 --max=10;sudo kubectl autoscale deployment -n openfaas-fn scaling-aeneas-tocloud --cpu-percent=50 --min=1 --max=10;sudo kubectl autoscale deployment -n openfaas-fn rawaeneas --cpu-percent=50 --min=1 --max=5;sudo kubectl autoscale deployment -n openfaas-fn getobject --cpu-percent=50 --min=1 --max=5;"',shell=True)
   elif approach == 'no+rps':
      print("Configuring",approach)
      subprocess.run('ssh ubuntu@172.17.141.197 "sudo kubectl scale --replicas=1 deployment amqp-connector-aeneas -n openfaas"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "sudo kubectl scale --replicas=1 deployment alertmanager -n openfaas"',shell=True)
      # Deploy functions
      subprocess.run('ssh ubuntu@172.17.141.197 "cd scalingsdp;faas deploy  -f aeneas.yml  --env max_inflight=10 --annotation topic="aeneas" --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=10"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd scalingsdp;faas deploy  -f getobject.yml --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=10;faas deploy  -f rawaeneas.yml --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=10"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd scalingsdp;faas deploy  -f scaling-aeneas-tocloud.yml --env max_inflight=50  --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=10;"',shell=True)
   elif approach == 'keda+rps':
      print("Configuring",approach)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd /home/ubuntu/rabbitmq-testing/sample-go-rabbitmq/deploy;sudo kubectl apply -f deploy-consumer.yaml"',shell=True)      
      subprocess.run('ssh ubuntu@172.17.141.197 "sudo kubectl scale --replicas=1 deployment alertmanager -n openfaas"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd scalingsdp;faas deploy  -f aeneas.yml  --env max_inflight=10 --annotation topic="aeneas" --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=10"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd scalingsdp;faas deploy  -f getobject.yml --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=10;faas deploy  -f rawaeneas.yml --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=10"',shell=True)
      subprocess.run('ssh ubuntu@172.17.141.197 "cd scalingsdp;faas deploy  -f scaling-aeneas-tocloud.yml --env max_inflight=50  --label com.openfaas.scale.min=1 --label com.openfaas.scale.max=10;"',shell=True)


def cpu_metric(metric_type,pod_name,namespace):
    if metric_type == 'requested':
        query = 'sum(kube_pod_container_resource_requests{job="kube-state-metrics", namespace="'+namespace+'", resource="cpu",pod=~"'+pod_name+'.*"''})&start='+str(start)+'&end='+str(end)+'&step=1s'
    else:
        query = 'sum(rate(container_cpu_usage_seconds_total{container_name!="POD",namespace="'+namespace+'",pod=~"'+pod_name+'.*"''}[60s]))&start='+str(start)+'&end='+str(end)+'&step=1s'
    data = getdataprometheus(pre_url+query)
    return data

def memory_metric(metric_type,pod_name,namespace):
    if metric_type == 'requested':
        query = 'sum(kube_pod_container_resource_requests{job="kube-state-metrics", namespace="'+namespace+'", resource="memory",pod=~"'+pod_name+'.*"''})&start='+str(start)+'&end='+str(end)+'&step=1s'
    else:
        query = 'sum(rate(container_memory_usage_bytes{container_name!="POD",namespace="'+namespace+'",pod=~"'+pod_name+'.*"''}[60s]))&start='+str(start)+'&end='+str(end)+'&step=1s'
    data = getdataprometheus(pre_url+query)
    return data

def pod_count(pod_name,namespace):
    query = 'sum(kube_pod_container_status_ready{namespace="'+namespace+'",pod=~"'+pod_name+'.*"''})&start='+str(start)+'&end='+str(end)+'&step=1s'
    data = getdataprometheus(pre_url+query)
    return data


def deleteMinio():
      client = Minio(minio_host, access_key = "minio", secret_key ="minio123",secure=False)
      objects = client.list_objects(bucket_name,recursive=True)
      for obj in objects:
         client.remove_object(bucket_name, obj.object_name)

def readMinio():
      client = Minio(minio_host, access_key = "minio", secret_key ="minio123",secure=False)
      objects = client.list_objects(bucket_name,recursive=True)
      outtime = []
      for obj in objects:
         data = {"outtime": obj.last_modified,"user_id": int((obj.object_name).split('.')[0])}
         outtime.append(data)
      return outtime

def locustTest():
   subprocess.run('rm input_data.csv',shell=True)
   subprocess.run('touch input_data.csv',shell=True)
   subprocess.run('echo "user_id,intime" > input_data.csv',shell=True)
   subprocess.run('locust --headless --only-summary -f k6_locust.py --host="127.0.0.1"',shell=True)

success_data = []
workload = sys.argv[1]
for i in range(len(approaches)):
   approach = approaches[i]
   deleteMinio()
   deploy_scaling(approach)
   locustTest()
   time.sleep(80)
   df= pd.read_csv('input_data.csv')
   success_data_dic = {'approach':approach,"total_users":df.axes[0]} 

   # Read from Minio
   success_data_dic = {'approach':approach,"total_users":df.axes[0]} 
   df_minio = pd.DataFrame(readMinio())
   df = pd.merge(df, df_minio, how='inner')
   # Commands for FET
   cmd1="ssh ubuntu@172.17.141.197 "+"sudo kubectl logs gateway-84b77b48c4-k2b64  -n openfaas -c gateway  | grep /function/aeneas |  grep POST |grep 200 | cut -c 68-71 | tail -"+str(len(df.axes[0]))
   cmd2="ssh ubuntu@172.17.141.197 "+"sudo kubectl logs gateway-84b77b48c4-k2b64 -n openfaas -c gateway  | grep /function/scaling-aeneas-tocloud |  grep POST |grep 200 |cut -c 84-88 | tail -"+str(len(df.axes[0]))
   cmd3="ssh ubuntu@172.17.141.197 "+"sudo kubectl logs gateway-84b77b48c4-k2b64 -n openfaas -c gateway  | grep /function/getobject | grep POST | grep 200 |cut -c 71-75  | tail -"+str(len(df.axes[0]))
   cmd4="ssh ubuntu@172.17.141.197 "+"sudo kubectl logs gateway-84b77b48c4-k2b64 -n openfaas -c gateway  | grep /function/rawaeneas | grep POST | grep 200 |cut -c 71-75 | tail -"+str(len(df.axes[0]))


   df['outtime']= pd.to_datetime(df['outtime'],errors='coerce').dt.tz_convert(None)
   df['intime']= pd.to_datetime(df['intime'],errors='coerce')
   df['aeneas']=(get_function_execution_time(cmd1)).split("\n")[:-1]
   df['tocloud']=(get_function_execution_time(cmd2)).split("\n")[:-1]
   df['getobject']=(get_function_execution_time(cmd3)).split("\n")[:-1]
   df['rawaeneas']=((get_function_execution_time(cmd4)).split("\n")[:-1])


   df['TPT']=(df['outtime']-df['intime'])
   df['TPT']=df['TPT'].values.astype('datetime64[ns]')
   df['TPT']= pd.to_datetime(df['TPT']).dt.strftime('%S.%f')
   df['TPT']=df['TPT'].astype(float)
   df['FET'] = (df['aeneas']).astype(float) + (df['tocloud']).astype(float) +(df['rawaeneas']).astype(float)+(df['getobject']).astype(float)
   df['Queue time']= ((df['TPT']).astype(float) - df['FET'])
   df["scenario"]= approach

   df.to_csv(workload+"_procTime_"+approach+'.csv')

   pre_url = PROMETHEUS + '/api/v1/query_range?query='
   timestamp= pd.to_datetime(df['outtime'].iloc[-1], format='%Y-%m-%d %H:%M:%S')
   time_interval = (time.mktime(timestamp.timetuple()))
   user=df.shape[0]
   end=(time.mktime(timestamp.timetuple()))
   start_time=pd.to_datetime(df['intime'].iloc[0], format='%Y-%m-%d %H:%M:%S')

   start=(time.mktime(start_time.timetuple()))


   interval = (df.loc[user-1, 'outtime'] - df.loc[0, 'intime']).total_seconds()
   interval= round(interval)

   user=df.shape[0]

   promo_metrics = pd.DataFrame()

   pods = ['aeneas','rawaeneas','getobject','scaling-aeneas-tocloud']
   concurreny = [3,50,50,50]
   connectors = ['amqp-connector-aeneas','amqp-connector-tocloud','amqp-connector-rawaeneas']

   promo_metrics['time']= cpu_metric('used','aeneas','openfaas-fn')['time']
   empty_array =np.empty(promo_metrics.shape[0])
   for i in range(len(pods)):
      con_data = empty_array.fill(concurreny[i])
      promo_metrics['cpu_used_'+pods[i]]= cpu_metric('used',pods[i],'openfaas-fn')['value']
      promo_metrics['cpu_requested_'+pods[i]]= cpu_metric('requested',pods[i],'openfaas-fn')['value']

      promo_metrics['memory_used_'+pods[i]]= memory_metric('used',pods[i],'openfaas-fn')['value']
      promo_metrics['memory_requested_'+pods[i]]= memory_metric('requested',pods[i],'openfaas-fn')['value']    

      promo_metrics['pod_count_'+pods[i]]= pod_count(pods[i],'openfaas-fn')['value']
      promo_metrics['mq_trigger_concurrency_'+pods[i]]= empty_array.tolist()  

   for i in range(len(connectors)):
      promo_metrics['cpu_used_mq_trigger_'+connectors[i]]= cpu_metric('used',connectors[i],'openfaas')['value']
    #  promo_metrics['cpu_requested_'+connectors[i]]= cpu_metric('requested',connectors[i],'openfaas')['value']

      promo_metrics['memory_used_mq_trigger_'+connectors[i]]= memory_metric('used',connectors[i],'openfaas')['value']
   #    promo_metrics['memory_requested_'+connectors[i]]= memory_metric('requested',connectors[i],'openfaas')['value']    

      promo_metrics['pod_count_mq_trigger_'+connectors[i]]= pod_count(connectors[i],'openfaas')['value']


   promo_metrics['throughput']= getdataprometheus('http://172.17.141.197:31376/api/v1/query_range?query=sum (rate(gateway_function_invocation_total{code="200"}[20s]))&start='+str(start)+'&end='+str(end)+'&step=1s')['value']

   promo_metrics.to_csv(workload+"_promo_metrics_"+approach+".csv",index=False)
   success_data_dic['processed_users'] = df.axes[0] 
   success_rate.append(success_data_dic, ignore_index=True)   
   delete_scaling(approach)
   print(success_rate)
   time.sleep(300)
success_rate.to_csv("success_rate.csv")






 

