# fog-edge middleware docomentation

## Introduction
Fog-edge serves as a middleware that communicates the fog-fog(server) layer and edge layer. It receives raw data (bpm and location data) from edge devices, then processes them and sends them to the fog-fog layer. The Fog-edge layer also stores copies of historical data locally. 

## How to Use Fog Server
1. Open Redis, go to Redis directory, run `src/redis-server`.
2. Run `/dev/tty*` in command to check usb id for bpm receiver and location receiver.
3. In `Publisher.py`, replace the `ser` with the usb connection id of bpm receiver and replace `ser2` with location receiver's id.
3. Run `Publisher.py`.

## Main Function of Fog-Edge layer
1. Connecting the edge layer and the fog-fog layer:
  The fog-edge uses `Redis` library to build a publisher-subscriber socket connection between fog-edge and the fog-fog layers. When it receives a message from edge devices, it will analyze the content of the message and process it into the expected format, then send the processed message to the fog-fog layer via `Redis` server. 

2. Local Data Storage:
  Since the edge layer will send all the raw data to the fog-edge layer, it is very important for us to store the data in a proper way. The fog-edge layer will sort all the data by different patient. It will store every 30 data for a same person in a `.txt` file and put the `patient id` and `date time` in the file name.
  
3.Machine Learning Predicton
  The fog-edge layer has a build in machine learning algoritm that predicts patients heart disease condition based on their bpm data. For more infomation on the AI, please go to `README_wws.md`.
