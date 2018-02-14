
# coding: utf-8

# In[1]:


from __future__ import division
from numpy.random import randn
import numpy as np
import os, glob
import sys
import matplotlib
import matplotlib.pyplot as plt
np.random.seed(12345)
plt.rc('figure', figsize=(10, 6))
from pandas import Series, DataFrame
import pandas as pd
np.set_printoptions(precision=4)
import random
get_ipython().run_line_magic('matplotlib', 'inline')
import pretty_midi as pm
import tensorflow as tf
from tqdm import tqdm


# In[2]:


#Literally load all midis as prettyMidis into a list
if(os.getcwd().split('/')[-1] != 'unpackedMidis'):
    os.chdir("unpackedMidis")

fileList = [x for x in glob.glob("*.mid")]
songList = []
badSongs = []
#doing all 16k crashes my whole computer. This may have something to do with Intel processors "leaking" in the most
#recent ubuntu dist. You should look that up
for file in tqdm(range(1000)):
    try:
        songList.append(pm.PrettyMIDI(fileList[file]))
    except:
        badSongs.append(fileList[file])


# In[11]:


songList[0].instruments[0].notes[0]


# In[ ]:


#So this builds two dictionaries. One for notes -> numbers, and the other for numbers -> notes
#You could also use pretty_midis pm.key_name_to_key_number() and pm.key_number_to_key_name()
#You can ignore this for now
def build_dataset(words):
    count = collections.Counter(words).most_common()
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return dictionary, reverse_dictionary

#This is the actual LSTM model
def RNN(x, weights, biases):

    # reshape to [1, n_input]
    x = tf.reshape(x, [-1, n_input])

    # Generate a n_input-element sequence of inputs
    # (eg. [had] [a] [general] -> [20] [6] [33])
    x = tf.split(x,n_input,1)

    # n-layer LSTM with n_hidden units.
    rnn_cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(n_hidden),rnn.BasicLSTMCell(n_hidden)])

    # generate prediction
    outputs, states = rnn.static_rnn(rnn_cell, x, dtype=tf.float32)

    # there are n_input outputs but
    # we only want the last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']

