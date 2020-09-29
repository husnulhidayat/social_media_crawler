import requests
import json
import pandas as pd
import sys
from pyspark.sql import SparkSession
import os

start = int(sys.argv[1])
end = int(sys.argv[2])
table_nm = sys.argv[3]

dir_loc = f'{dir_loc}'
sub_domain = f'{sub_domain}'

def get_json(start_page, max_page):
    uname = f'{username}'
    passw = f'{password}'
    ticket_metrics = []
    print('dumping json...')
    for page in range(start_page,max_page+1):
        print('iterating page:',page)
        url = '{}/api/v2/ticket_metrics.json?page={}'.format(sub_domain,page)
        response = requests.get(url, auth=(uname,passw))
        data = response.json()
        ticket_metrics.extend(data['ticket_metrics'])
        if 'url' in str(ticket_metrics):
            with open('{}/ticket_metrics.json'.format(dir_loc),'w') as f:
                m = json.dump(ticket_metrics, f)
        else:
            print(False)
            break
    print('done!')
        
def start_ingest():
    spark = SparkSession.builder.appName('zendesk_dump_ticket_metrics')\
            .config("parquet.compression", "SNAPPY")\
            .config('hive.exec.dynamic.partition.mode','nonstrict')\
            .enableHiveSupport()\
            .getOrCreate()
        
    with open('{}/ticket_metrics.json'.format(dir_loc),'r') as f:
        data = json.load(f)
    
    #load data to spark dataframe
    print('creating temp dataframe...')
    df_pd = pd.DataFrame(data)
    
    col_list = ['created_at','updated_at','assignee_updated_at','requester_updated_at','status_updated_at',
                'latest_comment_added_at','initially_assigned_at','assigned_at',
                'solved_at']
    for x in col_list:
        df_pd[x] = pd.to_datetime(df_pd[x], format="%Y-%m-%dT%H:%M:%SZ", errors='coerce')

    df_spark = spark.createDataFrame(df_pd)    
    print('start ingesting')
    df_spark.write.mode('overwrite').format('parquet').saveAsTable('{}'.format(table_nm))
    print('done ingesting')
    spark.stop()

get_json(start_page=start, max_page=end)
start_ingest()

