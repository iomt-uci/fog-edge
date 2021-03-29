
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
import math
import random
import pickle
import itertools

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, label_ranking_average_precision_score, label_ranking_loss, coverage_error 

from sklearn.utils import shuffle

from scipy.signal import resample

import matplotlib.pyplot as plt

np.random.seed(42)

import pickle
from sklearn.preprocessing import OneHotEncoder

from keras.models import Model
from keras.layers import Input, Dense, Conv1D, MaxPooling1D, Softmax, Add, Flatten, Activation# , Dropout
from keras import backend as K
from keras.optimizers import Adam
from keras.callbacks import LearningRateScheduler, ModelCheckpoint

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os

from sklearn.model_selection import train_test_split

# Any results you write to the current directory are saved as output.




#-------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------#

def get_signal(data_file):
    '''
        we use bpm for now.
        In future version, there will be one extra column called "signal"
            and we will use it
    '''
    l = []
    with open(data_file) as f:
        for line in f:
            patient_id, device_id, patient_name, bpm, alarm = line.strip().split("|")
            l.append(int(bpm))
    return l
            
            

def data_preprocessing(data_file):
    
    # 1) Splitting the continuous ECG signal to 10s windows
    #    and select a 10s window from an ECG signal.
    import numpy as np
    signal_list = np.array( get_signal(data_file) )
    
    # 2) Normalizing the amplitude values to the range of between zero and one.
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    ##db = scaler.fit_transform([signal_list])

    m = np.max(signal_list)
    # print(m)
    db = signal_list / m
    
    # 3) Finding the set of all local maximums based on zerocrossings of the ﬁrst derivative.
    from scipy.signal import argrelextrema
    local_max = argrelextrema(np.array([-1]+list(db)), np.greater)[0]-1#,argrelextrema(db, np.greater_equal)
    print("DB:   ", db)
    print("LOCAL MAX:   ", local_max)
    # 4) Finding the set of ECG R-peak candidates by applying a threshold of 0.9
    #    on the normalized value of the local maximums.
    R_peak_candidates = db[local_max][db[local_max]>0.9]
    R_peak_candidates_index = []
##    for each in R_peak_candidates:
##        print("NP :", np.where(db==each))
##        R_peak_candidates_index.append(int(np.where(db==each)[0]))
    for index in local_max:
        if db[index]>0.9:
            R_peak_candidates_index.append(index)
    # 5) Finding the median of R-R time intervals
    #    as the nominal heartbeat period of that window (T).
    intervals = [] 
    for i in range(1,len(R_peak_candidates_index)):
        intervals.append(R_peak_candidates_index[i]-R_peak_candidates_index[i-1])
    print("median:   ", median)
    median = np.median(intervals)

    # 6) For each R-peak, selecting a signal part with the length equal to 1.2T.
    signal_parts = []
    length = int(median*1.2)
    for i in R_peak_candidates_index:
        temp = []
        for v,l in zip(db[i:],range(length)):
            temp.append(v)
        signal_parts.append(temp)

    # 7) Padding each selected part with zeros to make its length equal to a predeﬁned ﬁxed length.
    padded_signal_part = []
    for each in signal_parts:
        padded_signal_part.append( np.pad(each, (0, 187-len(each)), 'constant', constant_values=(0, 0)) )

    X_real = np.array(padded_signal_part)
    X_real = np.expand_dims(X_real, 2)

    return X_real



def model_prediction(data):
    # read weights
    # predict
    K.clear_session()

    inp = Input(shape=(187, 1))
    C = Conv1D(filters=32, kernel_size=5, strides=1)(inp)

    C11 = Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(C)
    A11 = Activation("relu")(C11)
    C12 = Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(A11)
    S11 = Add()([C12, C])
    A12 = Activation("relu")(S11)
    M11 = MaxPooling1D(pool_size=5, strides=2)(A12)


    C21 = Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(M11)
    A21 = Activation("relu")(C21)
    C22 = Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(A21)
    S21 = Add()([C22, M11])
    A22 = Activation("relu")(S11)
    M21 = MaxPooling1D(pool_size=5, strides=2)(A22)


    C31 = Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(M21)
    A31 = Activation("relu")(C31)
    C32 = Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(A31)
    S31 = Add()([C32, M21])
    A32 = Activation("relu")(S31)
    M31 = MaxPooling1D(pool_size=5, strides=2)(A32)


    C41 = Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(M31)
    A41 = Activation("relu")(C41)
    C42 = Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(A41)
    S41 = Add()([C42, M31])
    A42 = Activation("relu")(S41)
    M41 = MaxPooling1D(pool_size=5, strides=2)(A42)


    C51 = Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(M41)
    A51 = Activation("relu")(C51)
    C52 = Conv1D(filters=32, kernel_size=5, strides=1, padding='same')(A51)
    S51 = Add()([C52, M41])
    A52 = Activation("relu")(S51)
    M51 = MaxPooling1D(pool_size=5, strides=2)(A52)

    F1 = Flatten()(M51)

    D1 = Dense(32)(F1)
    A6 = Activation("relu")(D1)
    D2 = Dense(32)(A6)
    D3 = Dense(5)(D2)
    A7 = Softmax()(D3)

    
    model_saved = Model(inputs=inp, outputs=A7)
    adam = Adam(lr = 0.001, beta_1 = 0.9, beta_2 = 0.999)
    model_saved.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
    model_saved.load_weights('ECG_classifier_200.h5')

    y_pred = model_saved.predict(data, batch_size=2).argmax(axis=1)

    return y_pred

def ml_prediction(data_file):
    '''

        call this function to get ECG signal prediction
    '''
    data = data_preprocessing(data_file)
    print("DATA:   " , data.shape)
    result = model_prediction(data)

    return result














