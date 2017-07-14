#! /usr/bin/python

import numpy as np

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

print "--> EmoWeb Statistics: "
print "\n"
print "|\tOverall\t|\tNonemotional\t|\tHappy\t|\tWondering\t|\tAngry\t|"
print "|\t%d\t|\t%d\t\t|\t%d\t|\t%d\t\t|\t%d\t|"%(a0+a1+a2+a3,a0, a1, a2, a3)
print "\n--> Thanks"
