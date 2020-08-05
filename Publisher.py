#!/usr/bin/env python
# coding: utf-8

# # Publisher

# In[ ]:


# simulate edge devices
import redis
import sys
import time
import random
from datetime import datetime

channel = "heart-rate"
patient_id = sys.argv[1]
patient_name = sys.argv[2]
location = "Room A"
# host_name = "192.168.50.121"
host_name = "127.0.0.1"

publisher = redis.Redis(host = host_name, port = 6379)

date = str(datetime.date(datetime.now()))
count = 0
file_number = 1
file = open(date+"_record_"+ str(file_number) +".txt", "w")

while True:
    bpm = random.randint(80, 100)
    alarm = 1 if bpm > 90 else 0

    # fill in sent_data to simulate strings
    sent_data = patient_id+"|"+patient_id+"|"+patient_name+"|"+str(bpm)+"|"+str(alarm)
    file.write(sent_data + '\n')
    count += 1
    publisher.publish(channel, sent_data)
    if count == 20:
        count = 0
        file_number += 1
        file.close()
        file = open(date+"_record_"+ str(file_number) +".txt", "w")
    time.sleep(2)


# In[ ]:




