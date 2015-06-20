import sys
import os
import pymongo
from pymongo import MongoClient
from itertools import islice

SENTENCE_END = "?!."
not_sentence_enders = ["Dr.", "Mr.", "Mrs."]

def is_sentence_end(last_word):
    if last_word in not_sentence_enders:
        return False

    if last_word[-1] in SENTENCE_END:
        return True

    return False

if __name__ == '__main__':
    args = sys.argv
    usage = 'Usage: %s (parse <filename> <depth> <dbname> | gen <name> <count>)' % (args[0], )

    if (len(args) < 3):
        raise ValueError(usage)

    filename   = args[1]
    depth      = int(args[2])
    dbname	   = args[3]

    text		= open(filename, "r").read()
    group		= text.split('\n')
    
    # setup MongoDB
    MONGOHQ_URL = os.environ.get('MONGOHQ_URL')
    connection 	= MongoClient(MONGOHQ_URL)
    db 		   	= connection['marty']
    		# check if there is 'testdb' existing
    									# create if none exists

    # clean up since we're still testing
    # db.phrases.remove({})

    # set document
    phrases	= db[dbname]

    # cleaning text
    sentence = " ".join(group)  # super-size string
    sentence = " ".join(sentence.split())   # remove multiple spaces
    sentence = sentence.translate(None, '[]"_;,')

    # split text
    words    = sentence.split(" ")
    num_words = len(words)
    iterations = iter(range(0, num_words-depth+1))
    _sentence_start = True

    for i in iterations:
        if i%1000 == 0:
            print i
    	_phrase = " ".join(words[i:i+depth])
        _next = "^"  # assume end of sentence

        if i < num_words-depth:
            _next = words[i+depth]

            _sentence_end = is_sentence_end(words[i+depth-1])
            if _sentence_end:
                _next = "^"
                next(islice(iterations, depth-1, depth-1), None)
                
        db_hits = phrases.find( { 'phrase' : _phrase } )

        if db_hits.count() > 0:
        # is already in database

            for doc in db_hits:
            	next_dict = doc['next']

                if _next not in next_dict:
                    phrases.update_one({'phrase': _phrase}, {'$push': {'next' : _next}})
        
        else:
        # only when phrase is not already in the dictionary	
        	phrases.insert({'phrase': _phrase, 'start': 1 if _sentence_start else 0, 'next': [_next]})

        _sentence_start = False
        if _sentence_end:
            _sentence_end = False
            _sentence_start = True


    count = phrases.count()
    print "Count: ", count

    size = db.command("collstats", dbname)['size']
    print "Size: ", size
