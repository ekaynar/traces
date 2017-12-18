
import sys
import numpy as np
import operator
import pandas as pd
from collections import deque
from lru import LRU
import ConfigParser
from boltons.cacheutils import LRU as botlru
from boltons.cacheutils import LRI
import logging
##############################################################
## GLobal Variables
#-----------------------------
key=[]
osize=[]
dict={}

config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))
log_file = config.get('My Section', 'log_file')
logging.basicConfig(filename=log_file,level=logging.DEBUG)


## Parsing the input file
## Get object ID,size and calculate footprint of
## input data for calculating the cache size, 
#----------------------------------------------
def parse(fname):
        fd = open(fname, 'r')
        data=0
        for line in fd:
                value = line.split(" ")
                key1 = value[2]
                osize.append(int(key1.split("length=")[1]))
                key.append(key1)
                if key1 not in dict:
                        dict[key1]=1
                        data+=int(key1.split("length=")[1])
        fd.close()
	dict.clear()
	logging.info("Footprint " + str(data))
	return data
## FIFO eviction policy
#-----------------------------
def fifo(ratio,output_file,data):
	hit=miss=0
	size = avail = float(data * ratio)/10
	hashmap={}
	avail=int(avail)
	fifo=deque()
	for i in range(len(key)):
		if key[i] in hashmap:
			hit+=1
		else:
			miss +=1
			if (osize[i] <= avail):
				fifo.append(key[i])
				hashmap[key[i]]=osize[i]
				avail -= osize[i]
			else:
				while(osize[i] > avail):
					id=fifo.popleft()
					avail+=hashmap[id]
					del hashmap[id]
				hashmap[key[i]]=osize[i]
				fifo.append(key[i])
				avail -= osize[i]

        fd = open("output_file","a")
        fd.write(str(hit)+","+str(miss)+"\n")
        fd.close()
        logging.info("Hit Ratio:"+str(hit))
        logging.info("Miss Ratio:"+str(miss))
        print "Cache Size:", int(size)
        print "Cache Size Ratio:", ratio/10
        print "Hit Ratio:", hit
        print "Miss Ratio:", miss

## LRU eviction policy
#-----------------------------
def lru(ratio,output_file,data):
	hit=miss=0
        size = avail = float(data * ratio)/10
        hashmap={}
        avail=int(avail)
	cache = LRU(3)
	for i in range(len(key)):
		if key[i] in hashmap:
			hit+=1
			cache[key[i]]="a"
		else:
			miss +=1
			if (int(osize[i]) <= avail):
				cache[key[i]]="1"
				hashmap[key[i]]=int(osize[i])
				avail -= int(osize[i])
			else:
				while(int(osize[i]) > avail):
					id = cache.peek_last_item()[0]	
				 	avail+=int(hashmap[id])
                                        del cache[id]
					del hashmap[id]
				hashmap[key[i]]=osize[i]
                                cache[key[i]]="1"
                                avail -= int(osize[i])
        fd = open("output_file","a")
        fd.write(str(hit)+","+str(miss)+"\n")
        fd.close()
        logging.info("Hit Ratio:"+str(hit))	
        logging.info("Miss Ratio:"+str(miss))	
        #print "Cache Size:", int(size)
        #print "Cache Size Ratio:", ratio/10
        #print "Hit Ratio:", hit
        #print "Miss Ratio:", miss
	print hit, "," , miss
if __name__ == "__main__":

## Load the configuration file
#------------------------------

	input_file = config.get('My Section', 'input_file')	
	size_ratio = int(config.get('My Section', 'size_ratio')	)
	cache_type = config.get('My Section', 'cache_type')
	output_file = config.get('My Section', 'output_file')

## Parsing the Input File
	logging.info('Parsing ' + str(input_file))
	data=parse(input_file)

## Running Single Level Cache
	if cache_type == "fifo":
		logging.info('Eviction Policy: FIFO' )
		for i in xrange(1,size_ratio+1):
			print i
			fifo(i, output_file,data)
	elif cache_type =="lru":
		logging.info('Eviction Policy: LRU' )
		for i in xrange(1,size_ratio+1):
			lru(i, output_file,data)
		

#		
#	lru(1);	
    	#test(sys.argv[1:])
