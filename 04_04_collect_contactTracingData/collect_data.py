#!/usr/bin/env python
# coding: utf-8


# import deep_learning_api
# import serial
# import redis
import sys
import time
import random
from datetime import datetime
import time
from scipy import stats
from collections import defaultdict
import requests

channel = "heart-rate"
# patient_id = "2"
# patient_name = "Zhenghao"
# location = "Room A"
# host_name = "192.168.50.121"
host_name = "127.0.0.1"



#####################################################
###CHANGE THE IP ADDRESS FOR THE PATIENT DEVICE######
URL_host_list = ["http://192.168.4.2","http://192.168.4.3","http://192.168.4.4"] # retrieve bph data
####################################################

raw_data_path = '/raw-data'


start_sending_location = False

db = dict()
patient_files = dict()

patient_record_temp = defaultdict(list)

start_time = time.time()



loops = 0
num_data = 0

with open("04_03_exp4_data.txt","w") as f:
    while num_data<300:
        print(f"num data: {num_data+1}")
        num_data+=1
        try:
            for device_URL in URL_host_list:
                cur_time = datetime.now()
                timestamp = f"{cur_time.month}-{cur_time.day}-{cur_time.hour}-{cur_time.minute}-{cur_time.second}"

                r = requests.get(device_URL+raw_data_path)
                data = eval(r.text)
                data['timestamp'] = timestamp
                if (1):
                    print(str(data))
                f.write(str(data)+"\n")
                            
        except UnicodeDecodeError:
            print("decode exception once")
    