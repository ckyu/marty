import sys
import os
import pymongo
from pymongo import MongoClient
import random

if __name__ == '__main__':
    args = sys.argv
    usage = 'Usage: %s gen <dbname>' % (args[0], )

    if (len(args) < 2):
        raise ValueError(usage)

    dbname	   = args[1]

    # setup MongoDB
    MONGOHQ_URL = os.environ.get('MONGOHQ_URL')
    connection 	= MongoClient(MONGOHQ_URL)
    db 		   	= connection['marty']		
    phrases		= db[dbname]

    states = [p['phrase'] for p in phrases.find({'start':1})]
    # print states
    cnt = len(states)
    curr_state = states[random.randint(0,cnt)]
    gen = curr_state
    while curr_state != "^":
    	print curr_state,
    	list_next = [p['next'] for p in phrases.find({'phrase': curr_state})]
    	# print list_next
    	cnt = len(list_next)
    	# if cnt > 1:
	    	next_word = list_next[random.randint(0, cnt)]
    	# else:
    		# next_word = list_next[0][0]
    	if next_word == "^":
    		break

    	gen += " " + next_word
    	print next_word
    	
    	curr_state = [" ".join(curr_state.split()[1:]), next_word]
    	# print curr_state
    	curr_state = " ".join(curr_state)

    print ""
    print gen