#! /usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: prepocess.py
# Description: 
# Author: Jialiang Zhao
# Mail: alanzjl@163.com
# Created_Time: 2017-05-01 20:17:29
# Last modified: 2017-05-01 20:17:1493641049
#########################################################################

import re
import sys
import numpy as np

def decoder(filename):         
    # ‘：’ \uff1a
    textFile = file(filename, 'rb')
    talkers = []
    res = []
    reTalker = re.compile(u'.+(?=\uff1a)')
    reWord = re.compile(u'(?<=\uff1a).+')
    lines = textFile.readlines()
    for line in lines:
        talker = reTalker.findall(line.decode('utf8'))
        if(len(talker) > 0):
            talker[0] = talker[0].strip()
            candidates = reWord.findall(line.decode('utf8'))
            if (talker[0] not in talkers):
                talkers.append(talker[0])
            talkerABC = talkers.index(talker[0])
            if  (len(candidates) >= 1):
                res.append([talkerABC, candidates[0].encode('utf-8'), -1])
            #print candidates[0]
    return res
    #for a in res:
        #print a
        #print a[0], a[1].encode('utf8')
        #print '-->\t', talkerABC, '\t', candidates[0].encode('utf8')

def convt(res, fn):
    npRes = np.asarray(res)
    np.save(fn+'.npy',npRes)
    print "--> prepocessed file saved as: " + fn + ".npy"
    waitlist = file('waitlist.txt', 'a')
    waitlist.write(fn+".npy\n")
    waitlist.close()
    print "--> waitlist.txt written"

def readFromList():
    fnList = file("sourcelist.txt", 'rb')
    fns = fnList.readlines()
    for fn in fns:
        fn = fn.strip('\n')
        print '----'
        print "----> processing file: " + fn
        print '----'
        res = decoder(fn)
        #for i in res:
        #    for a,b in i.items():
        #        print "-->", a, "\t", b
        convt(res, fn)




if __name__ == "__main__":
    print "text analysis preprocess - V1.0"
    if (len(sys.argv) == 1):
        print "No source txt specified. Using sourcelist.txt"
        readFromList();
        exit(0);
    elif  (len(sys.argv) > 2):
        print "Usage: ./prepocess.py [filename]"
        exit(1)
    filename = sys.argv[1]
    res = decoder(filename)
    convt(res, filename)


