import math
import tokenize
import StringIO
import json
from collections import defaultdict
import lxml.html


token_indexes = defaultdict(dict)
best_docs = []

with open('/Volumes/G-DRIVE mobile USB/InvertedIndex.json') as json_data:
    all_indexes = json.load(json_data)


def calc_inverse_df(index, term):
    """Given the inverted index of all documents,
    calculates the inverse document frequency
    of the given term"""
    if term not in index:
        return 0
    else:
        ##length of all_indexes (hardcoded to optimize)
        N = 760136

            #doc_frequency is amount of times term appears in documents
        doc_frequency = len(index[term])

            #use log to dampen effect of idf    
        return math.log10((N/doc_frequency))

def calc_term_freq(index, term, docID) :
    """Given the interverted index of all documents,
    calculates the term frequency using log-frequency
    weighting of the given term in a given document"""

    if (term not in index) or (docID not in index[term]):
        return 0
    else:
        return (1 + math.log10(index[term][docID]))

def calc_tfIdf_weight(index, term, docID) :
    """Returns the product of the term frequency
    weight and its inverse document frequency weight"""

    return calc_inverse_df(index, term) * calc_term_freq(index, term, docID)

def calc_query_score(index, query, docID) :
    """Given a search query (a list of tokens) and a document
    ID, calculates the score of that query in the provided
    document"""

    score = 0
    for token in query:
        score += calc_tfIdf_weight(index, token, docID)
    return score

def find_best_documents(index, query) :
    """Returns a sorted list in descending order based on
    each documents' query score. Higher scores are at the front
    of the list"""
   
    return sorted(
        {docID for term in index for docID in index[term]},
        key = lambda x: -(calc_query_score(index, query, x)))

def get_tokenize_query():

    """Takes input from the user as a query
    and tokenizes the query which is returned
    to find the relevant pages"""

    tokens = []
    search_query = raw_input("Enter query or quit: ")
    try:
        tokenized = tokenize.generate_tokens(StringIO.StringIO(search_query).readline)
        for toknum,tokval,_,_,_ in tokenized: ## code used from https://docs.python.org/2/library/tokenize.html
            if tokval != "":
                tokens.append(tokval.lower())
    except tokenize.TokenError:
            pass

    return tokens

def get_indexes( tokens, d):
    global token_indexes
    for token in tokens:
        if d.get(token) != None:
            token_indexes[token] = d.get(token)
        else:
            pass



    
    

def best_docs(index, tokens):
    """Takes input from the user as a search query
    and prints to the screen a ranked list of
    pages relevant to the query"""


    best_docs = find_best_documents(index, tokens)
    return(best_docs[:10])

def writeFile(data):
    with open('TokenIndex.json', 'w') as outfile:
        json.dump(data, outfile)

def getURLs(docs):
    query_urls = []
    with open('/Users/madisonthompson/Downloads/WEBPAGES_RAW/bookkeeping.json') as json_data:
        d = json.load(json_data)
    
    for position in docs:
            url = "http://" + d[position]
            query_urls.append(url)
    json_data.close()
    return  query_urls

        
        


if __name__ == '__main__':

    while(True):
        tokens = get_tokenize_query()
        
        if 'quit' in tokens:
            break
        get_indexes(tokens,all_indexes)
        
        writeFile(token_indexes)
        with open('/Users/madisonthompson/Downloads/TokenIndex.json') as token_data:
           indexes = json.load(token_data)
        best = best_docs( indexes, tokens)
        urls =   getURLs(best)
        print("\n To open link cmd then double click the link\n")
        if len(urls) != 0 and len(urls)>=10:
                for x in range(10):
                    print(str(x+1) + ". " + urls[x]+"\n")
        elif len(urls)< 10 and len(urls)>0:
            for x in range(len(urls)):
                print(str(x+1) + ". " + urls[x] +"\n")
        else:
            print("Sorry no pages found for this query try again")
                
            

    json_data.close()
        



















#sample_query = ["computer", "science"]
#sample_query2 = ["sharks", "in", "the", "water"]

#print(calc_inverse_df(sample_dict, "science"))
#print(calc_inverse_df(sample_dict, "the"))

#calc_term_freq(sample_dict, "science")
#print(calc_term_freq(sample_dict, "the", "1:1"))

#print(calc_tfIdf_weight(sample_dict, "science", '1:0'))

#print(calc_query_score(sample_dict, sample_query, "0:0"))
#print(calc_query_score(sample_dict, sample_query, "0:1"))
#print(calc_query_score(sample_dict, sample_query, "1:0"))
#print(calc_query_score(sample_dict, sample_query2, "0:1"))
#print(calc_query_score(sample_dict, sample_query2, "1:1"))


#print(find_best_documents(sample_dict, sample_query))
