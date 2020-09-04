# fog-edge
# ai

Following the guidance from ECG Heartbeat Classification: A Deep Transferable Representation, I trained a deep residual convolutional neural network and setup a data normalization procedure to preprocess input data. 

The classification report is 

class | precision | recall | f1-score  
N     | 0.83      | 1.00   | 0.91  
S     | 1.00      | 0.87   | 0.93  
V     | 0.96      | 0.95   | 0.95  
F     | 0.99      | 0.94   | 0.96  
Q     | 1.00      | 0.99   | 0.99  
avg   | 0.96      | 0.95   | 0.95  



Then, I cooperated with Zhenghao and successfully implemented the deep learning model in the fog-edge device. 
