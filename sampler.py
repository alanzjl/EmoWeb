#!/usr/bin/python
#########################################################################
# File Name: sampler.py
# Description: 
# Author: Jialiang Zhao
# Mail: alanzjl@163.com
# Created_Time: 2017-05-09 19:25:19
# Last modified: 2017-05-09 19:25:1494329119
#########################################################################

import sys
import os
import datetime
import numpy as np
import time


def login(userlist):
    username = raw_input("Please input your username: ")
    while len(username) < 5:
        username = raw_input("Please input a valid username (length >= 5): ")
        
    if username not in userlist[:, 0]:
        print "User does not exit. Creating user: ", username
        password = raw_input("Please input your password (unchangable): ")
        name = raw_input("And your real name: ")
        userlist = np.concatenate((userlist, np.array([[username, password, name, 0]])))
        np.save("users/userlist.npy", userlist)
        print username, " created"
        userid = np.where(userlist[:,0] == username)[0][0]
    else:
        password = raw_input("Please input your password: ")
        userid = np.where(userlist[:,0] == username)[0][0]
        if userlist[userid,1] != password:
            print "\nSorry, wrong password."
            print "Contact Jialiang if you forget or want to change your password."
            exit(0);

    print username, " welcome to EmoWeb!"
    print "\n-->\tYou have labelled %d samples till now. Contact Jialiang if you want to download them."%int(userlist[userid, 3])

    print '\n\n'
    time.sleep(3)
    return userid
        

def getInput():
    valid = ['-1', '0', '1', '2', '3']
    input = (raw_input("\t->press 0 (no emotion),1 (positive),2 (wondering), 3 (negative), or -1 (nonsense): "))
    while input not in valid:
        input = (raw_input("\t->press 0 (no emotion),1 (positive),2 (wondering), 3 (negative), or -1 (nonsense): "))
    res = int(input)
    return res

def sampler(inFile):
    print "\n--> Please select an emotion for the following sentences <--"
    print "--> Neiboring sentences are related <--"
    print "--> press 0 (no emotion),1 (positive),2 (wondering), 3 (negative), or 9 (nonsense) after each sentence"
    print "|\tspeaker\t|\t sentence\n\n"
    #a = np.asarray([]);
    a = []
    i = 0;
    for line in inFile:
        i = i+1
        print "%d/%d\t|\t"%(i, len(inFile)) + line[0] + "\t|\t" + line[1]
        res = getInput()
        print "-----------------------------------------------------------------------------------"
        line[2] = res;
        #np.concatenate((a,line), axis=0)
        if res != 9:
            a.append(line.tolist())
        #print a

    return a


def readFromList(userid):
    waitList = file('waitlist.txt', 'r+')
    waitfiles = waitList.readlines()
    waitList.close()
    newwf = waitfiles;
    for wf in waitfiles:
        wf = wf.strip('\n')
        npWF = np.load(wf)
        print "--> Numpy file " + wf + " loaded. Starting sampler\n\n\n"
        npWFlist = sampler(npWF)
        np.save("data/" + wf, np.asarray(npWFlist))
        print "--> " + wf + " finished. Saved as " + "data/"+wf+"\n\n\n"
        
        userlist[userid, 3] = '%d'%(int(userlist[userid,3]) + len(npWF))
        np.save("users/userlist.npy", userlist)
        print "# Your data has been updated. Thanks for your kind help! You can safely quit this web now, or another database will be loaded."
        time.sleep(2);
        
        npAll = np.load('data/all.npy')
        if(npAll.size == 0):
            npAll = np.asarray(npWFlist)
        else:
            npAll = np.concatenate((npAll, np.asarray(npWFlist)), axis=0)
        #npAll = npAll.reshape((-1,3))
        np.save('data/all.npy', npAll)
        #print npAll.shape
        print "--> New data merged to database. Merged shape: %d %d"% (npAll.shape[0],npAll.shape[1])
        print "\n\n"
        #print npAll
        now = datetime.datetime.now()
        tim = now.strftime('%Y.%m.%d.%H.%M.%S')
        os.system("cp data/all.npy data/backup/"+tim+'.npy')
        print "--> backup made: " + tim
        newwf.remove(wf+'\n')
        #print newwf
        newwl = file('waitlist.txt', 'w+')
        for i in newwf:
            newwl.write(i)
        newwl.close()
        print "Thanks, this file is finished. Another one will be loaded.\n"
        print '--------------------------------------------------------------------------------'
    print "Sorry, there are no more files waiting to be labelled. Please contact Jialiang Zhao to add more.\n\n"

def statistics():
    data = np.load('data/all.npy')
    a0 = 0
    a1 = 0
    a2 = 0
    a3 = 0

    for i in data:
	if i[2] == '0':	a0 = a0+1
	if i[2] == '1':	a1 = a1+1
	if i[2] == '2':	a2 = a2+1
	if i[2] == '3':	a3 = a3+1

    print '--------------------------------------------------------------------------------'
    print "--> EmoWeb Statistics: (Current labelled samples in EmoWeb)"
    time.sleep(3)
    print "\n"
    print "|\tOverall\t|\tNonemotional\t|\tHappy\t|\tWondering\t|\tAngry\t|"
    print "|\t%d\t|\t%d\t\t|\t%d\t|\t%d\t\t|\t%d\t|"%(a0+a1+a2+a3,a0, a1, a2, a3)
    print '--------------------------------------------------------------------------------'
    print "\n"

if __name__ == "__main__":
    print "\n\n"
    print '--------------------------------------------------------------------------------'
    print '--------------------------------------------------------------------------------'
    print '\n\n\t\t EmoWeb: Emotion Detection in Dialogues\n\n'
    print "\t\t This web is deleloped by Jialiang Zhao "
    print "\t\t Contact me at QQ/WeChat: 843216224 if you need anything"
    print '\n--------------------------------------------------------------------------------'
    print '\t-->\t Basic rules: Samples are collected by Jiawei Zhang and me (Team 20)'
    print '\t-->\t Basic rules: If you label n samples in EmoWeb, we will send you 2*n labelled samples for your own task'
    print '\t-->\t If you have better samples, please contact me'
    print "\n\n\t IMPORTANT!!!!!!!! Don't quit this web when labelling within one file, or your labelled data won't be merged into database\n\n"
    print "\n Version 1.3, developed by Jialiang\n"
    print "\n Version 1.3 update: happy -> possitive, angry -> negative"
	
    time.sleep(3)
    statistics()

    
    userid = -1
    userlist = np.load("users/userlist.npy")
    
    userid = login(userlist);
    if(userid != -1):
        readFromList(userid);

