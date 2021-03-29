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
import distance_tracking_api

channel = "heart-rate"
# patient_id = "2"
# patient_name = "Zhenghao"
# location = "Room A"
# host_name = "192.168.50.121"
host_name = "127.0.0.1"



#publisher = redis.Redis(host = host_name, port = 6379)
publisher = redis.Redis.from_url('redis://3.tcp.ngrok.io:23327')

date = str(datetime.now()).replace("-","_").replace(".","_").replace(" ","_").replace(":", "_")

#####################################################
###CHANGE THE IP ADDRESS FOR THE PATIENT DEVICE######
URL_host_list = ["http://192.168.0.148"] # retrieve bph data
#####################################################

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

# send data Fog_edge -> fog_fog
# {
#   Patient_id: "1234",
#   Device_id: "0",
#   Patient_first_name: "Taiting",
#   Patient_last_name: "Lu",
#   BPM: "90",
#   BPM_Pred: “A”, 
#   SPO2: "95",
#   Room_num: "0", ##(0-> CT room, 1-> hall way)
#   Contact: 
#   [
#       {Device_id:”1”,value:"0-3"} ## (range: 0-3 feet, 3-6 feet, 6-9 feet)
#   ]
# }
record = open('RECORD'+date+'.txt', 'w')
while True:
    try:
        for device_URL in URL_host_list:
            r = requests.get(device_URL+raw_data_path)
            data = eval(r.text)
            Patient_id = data['Patient_id']
            Device_id = data['Device_id']
            Patient_first_name = data['Patient_first_name']
            Patient_last_name = data['Patient_last_name']
            BPM = data['BPM']
            SPO2 = data['SPO2']

            Room_num = distance_tracking_api.get_current_position(data['AP'])
            Contact = distance_tracking_api.get_SD_Alarms(data['USR'])
  
            message_to_server = {
                "Patient_id": Patient_id,
                "Device_id": Device_id,
                "Patient_first_name": Patient_first_name,
                "Patient_last_name": Patient_last_name,
                "BPM": BPM,
                "BPM_Pred": "None",
                "SPO2": SPO2,
                "Room_num": Room_num,
                "Contact": Contact
            }
            
            

            if Patient_id not in patient_files:
                file = open(date+"_record_"+ Patient_id +".txt", "w")
                patient_files[Patient_id] = file
                
            line = '|'.join([Patient_id, Device_id, Patient_first_name, Patient_last_name, BPM])
            
            if Patient_id in db and len(patient_record_temp[Patient_id])>30:
                # start recording after receiving 30 data; 
                db[Patient_id].append(line)
            else:
                db[Patient_id] = [line]
                patient_record_temp[Patient_id].append(line)
            
            if Patient_id in db and len(db[Patient_id])!=0 and len(db[Patient_id]) % 30==0:
                ml_result = deep_learning_api.ml_prediction( db[Patient_id] )#patient_file[Patient_id])
                print("ml result is:      ",ml_result)
                if ml_result == -1:
                    pass
                else:
                    # publisher.publish(channel, Device_id+"|"+ deep_learning_api.convert(ml_result) +"|"+"00")
                    message_to_server["BPM_Pred"] = deep_learning_api.convert(ml_result)
                    patient_files[Patient_id].write("\n".join(db[Patient_id]))
                    db[Patient_id] = list()
                    print("Result;  ", deep_learning_api.convert(ml_result))
                    
            print(message_to_server)
            record.write(str(message_to_server)+'\n')
            record.flush()
            #publisher.publish(channel, json.dumps(message_to_server))


            
        time.sleep(2)
                        

    except UnicodeDecodeError:
        print("decode exception once")
