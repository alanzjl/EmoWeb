#!/usr/bin/python
#########################################################################
# File Name: get_EmoWeb_data.py
# Description: 
# Author: Jialiang Zhao
# Mail: alanzjl@163.com
# Created_Time: 2017-05-20 19:39:09
# Last modified: 2017-05-20 19:39:1495280349
#########################################################################

import numpy as np

if __name__ == '__main__':
    data = np.load('data.npy')   # Data file from EmoWeb
    print "-->\tData Size: ", data.shape[0]
    print "-->\tCnt\t|\tSpeaker\t|\tLabel\t|\tSentence"
    for i in xrange(data.shape[0]):
        print "-->\t%d/%d\t|\t"%(i+1, data.shape[0]) + data[i][0] + "\t|\t" + data[i][2] + "\t|\t" + data[i][1]

