import sys
import time
import json
from lxml import html,etree
import urllib2
import nltk
import math
import HTMLParser
from bs4 import BeautifulSoup
from collections import defaultdict, OrderedDict
from urlparse import urlparse, parse_qs
import re
from rankedRetrieval import calc_inverse_df, calc_term_freq

##dictionary to store inverted index
index = defaultdict(dict)

##docIDs = {}

data= {}
docs = 0



##gets file info for url from bookkeeping
def getInfo():
    """Gets file info for url from bookkeeping.json parses the html
        and create inverted index dictionary"""
    global docs
    with open('/Users/madisonthompson/Downloads/WEBPAGES_RAW/bookkeeping.json') as json_data:
        d = json.load(json_data)
        for urlfile in d:
            folder_num, file_num = urlfile.split('/')
            file_path = '/Users/madisonthompson/Downloads/WEBPAGES_RAW/'+ folder_num +'/' + file_num
            url = "http://" + d[urlfile]
             
            if is_valid(url) == True:
                docs += 1
 ##               docIDs[urlfile] = url
                with open(file_path) as content:
                    x = content.read()
                    ##create beuatiful soup class object and parse
                    soup = BeautifulSoup(x,"html.parser")
                    ##return unicode text for html doc
                    words= soup.get_text()
                    ##tokenize the words
                    tokens = nltk.word_tokenize(words)
                
                for token in tokens:
                    if len(token) < 25:
                        if token not in index and urlfile not in index[token]:
                            index[token][urlfile] =  1
                        if token in index and urlfile not in index[token]:
                            index[token][urlfile] = 1
                        else:
                            index[token][urlfile] += 1
    print docs
    return index
                    

def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be crawled
 
    '''
    parsed = urlparse(url)
    long_str= re.match("^.*/[^/]{300,}$" ,parsed.path.lower())
    if long_str != None:
        return False

    if '.java' in parsed.path.lower():
        return False
    if '.txt' in parsed.path.lower():
        return False

    not_web = re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
    if not_web!= None:
        return False
    
    else:
        return True

        



def writeFile(data):
    data = OrderedDict(sorted(data.items(),key = lambda x:x[0]) )
    with open('InvertedIndex.json', 'w') as outfile:
        json.dump(data, outfile)
    

                  
def calc_for_best():
    with open('/Volumes/G-DRIVE mobile USB/InvertedIndex.json') as json_data:
           d = json.load(json_data)
           for term in d:
               inverse_df = calc_inverse_df(d[term], term)
               term_freq= 

                
        


if __name__ == "__main__":
 ##   index = getInfo()
 ##   writeFile(index)
    test()
    
