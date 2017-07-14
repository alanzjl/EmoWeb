#!/usr/bin/python
#########################################################################
# File Name: sharegen.py
# Description: 
# Author: Jialiang Zhao
# Mail: alanzjl@163.com
# Created_Time: 2017-05-20 18:41:23
# Last modified: 2017-05-20 18:41:1495276883
#########################################################################

import numpy as np
import sys
import os

def gendata(userdata, username, password):
    print 'generating txt...'

    os.system('mkdir -p download/'+username)

    txt = file('download/'+username+'/data.txt', 'w+')
    writedata = '================================================================================ \n'
    writedata += 'Data for ' + username + ' from EmoWeb\n'
    writedata += 'Here are %d labelled data in our database\n'%len(userdata)
    writedata += 'Thanks for your contribution to this web! \n'
    writedata += 'This file is auto-generated. \n'
    writedata += 'Please contact Jialiang Zhao if you have any question \n'
    writedata += '================================================================================ \n'
    writedata += '\n|\tcount\t\t|\tspeaker\t|\tlabel\t|sentence\n\n'
    cnt = 1
    for i in userdata:
        writedata += '%d / %d'%(cnt, userdata.shape[0])+'\t\t'+i[0] + '\t' + i[2] +'\t'+i[1] + '\n'
        cnt += 1
    txt.write(writedata)
    txt.close()

    np.save('download/'+username+'/data.npy', userdata)
    
    os.system('cp get_EmoWeb_data.py download/'+username)
    os.system('cp README.txt download/'+username)

    # os.system('cd download')
    os.popen('zip -r -P '+password+' download/' + username + '.zip download/'+username)
    # os.system('cd ..')

def sharegen(user = ''):
    userlist = np.load('users/userlist.npy')
    data = np.load('data/all.npy')
    for i in userlist:
        username = i[0]
        password = i[1]
        usernum = int(i[3])
        if 2*usernum < data.shape[0]:
            userdata = data[0:2*usernum]
        else:
            userdata = data

        gendata(userdata, username, password)
        #print username," data generated, size: %d"%userdata.shape[0] 

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "--> Generating download links for users..."
        sharegen();
    else:
        #print "--> Generating for ",sys.argv[1], " ..."
        sharegen(user = sys.argv[1])

