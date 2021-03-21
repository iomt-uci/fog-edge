#!/usr/bin/env python
# coding: utf-8

# # Publisher

# In[ ]:


# simulate edge devices
import deep_learning_api
import serial
import redis
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



#publisher = redis.Redis(host = host_name, port = 6379)
publisher = redis.Redis.from_url('redis://3.tcp.ngrok.io:23327')

date = str(datetime.now())
URL_host_list = ["http://192.168.0.148"] # retrieve bph data
raw_data_path = '/raw-data'


start_sending_location = False

db = dict()
patient_files = dict()

patient_record_temp = defaultdict(list)

start_time = time.time()

# sample retrieved data
# {
#     "Patient_id":"01", 
#     "Device_id":"ESP32-USR03",
#     "Patient_first_name":"Lu",
#     "Patient_last_name":"Lu",
#     "BPM":"0",
#     "SPO2":"-999","TEMP":"0.00",
#     "AP":{"AP1":-90,"AP2":-90,"AP3":-90,"AP4":-90,"AP5":-90,"AP6":-90,"AP7":-90,"AP8":-90,"AP9":-90,"AP10":-90},
#     "USR":{"USR0":-90,"USR1":-90,"USR2":-90,"USR3":-90}
# }
while True:
    try:
        for device_URL in URL_host_list:
            r = requests.get(device_URL+raw_data_path)
            data = eval(r.text)
            Patient_id = data['Patient_id']
            Device_id = data['Device_id']
            patient_name = data['Patient_first_name']+" "+data['Patient_last_name']
            bpm = data['BPM']

            xPosition, yPosition = get_current_position(AP)
            sdAlarm0,sdAlarm1,sdAlarm2 = get_SD_Alarms(USR)
            infos = [Patient_id, Device_id, patient_name,xPosition,yPosition,sdAlarm0,sdAlarm1,sdAlarm2]
            publisher.publish(channel, "|".join(infos))

            location = (xPosition,yPosition)
            location_data = Device_id+"|"+str(location) #+"|"+str(time.time())
            publisher.publish(channel, location_data)
            print(location_data)

            if Patient_id not in patient_files:
                file = open(date+"_record_"+ Patient_id +".txt", "w")
                patient_files[Patient_id] = file

            if Patient_id in db and len(patient_record_temp[Patient_id])>30:
                # start recording after receiving 30 data; 
                line = '|'.join([Patient_id, Device_id, patient_name, bpm])
                db[Patient_id].append(line)
            else:
                db[Patient_id] = [line]
                patient_record_temp[Patient_id].append(line)
                
            if Patient_id in db and len(db[Patient_id])!=0 and len(db[Patient_id]) % 30==0:
                ml_result = deep_learning_api.ml_prediction( db[Patient_id] )#patient_file[Patient_id])
                print("ml result is:      ",ml_result)
                if ml_result is -1:
                    pass
                else:
                    publisher.publish(channel, Device_id+"|"+ deep_learning_api.convert(ml_result) +"|"+"00")
                    patient_files[Patient_id].write("\n".join(db[Patient_id]))
                    db[Patient_id] = list()
                    print("Result;  ", deep_learning_api.convert(ml_result))
            
        time.sleep(5)
                        

    except UnicodeDecodeError:
        print("decode exception once")







        



