# fog-edge middleware docomentation

## Introduction
Fog-edge serves as a middleware that communicates the fog-fog(server) layer and edge layer. It receives raw data (bpm and location data) from edge devices, then processes them and sends them to the fog-fog layer. The Fog-edge layer also stores copies of historical data locally. 

## How to Use Fog Server
1. Open Redis, go to Redis directory, run `src/redis-server`.
2. Run `/dev/tty*` in command to check usb id for bpm receiver and location receiver.
3. In `Publisher.py`, replace the `ser` with the usb connection id of bpm receiver and replace `ser2` with location receiver's id.
3. Run `Publisher.py`.

