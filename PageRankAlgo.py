import math
import operator

dict_inlinks = dict() #dictionary consisting of nodes and its inlinks
dict_outlinks = dict() #dictionary consisting of nodes and its outlinks
S = [] # set of sinkNodes, pages that have no outlinks
L = {} #number of outlinks from a page
PR = {}
PR_new = {}
PR_TEMP = []
d = 0.85 #teleportation factor


# the below function creates a dictionary for inlinks
def get_listof_inlinks(file):
    inlinks = {}
    f = open(file,"r+")
    each_line = f.readlines()
    for i in each_line:
        text = str(i).strip()
        texts = text.split()
        dict_inlinks.setdefault(texts[0],[])
        num_inlinks = 0
        for each_inlink in texts[1:]:
            num_inlinks+=1
            dict_inlinks[texts[0]].append(each_inlink)
        inlinks[texts[0]] = num_inlinks

    temp = 0
    # to calculate the total number of pages with no in-links
    for key in inlinks.keys():
        if inlinks[key] == 0:
            temp+=1
    f.close()

get_listof_inlinks("G1.txt")


# the below function creates a dictionary of outlinks
def get_listof_outlinks():
    for doc_id in dict_inlinks.keys():
        dict_outlinks.setdefault(doc_id,[])

    for doc_id,values in dict_inlinks.iteritems():
        for inlinks in values:
            if str(inlinks) in dict_inlinks:
                dict_outlinks[inlinks].append(doc_id)

get_listof_outlinks()

P = dict_inlinks.keys() # its the set of all pages
N = len(P)

# to calculate the number of sink nodes
def num_of_outgoing_links():
    for doc_id in P:
        doc_ids = dict_inlinks[doc_id]
        for doc_id in doc_ids:
            if doc_id in L:
                L[doc_id] = L[doc_id] + 1
            else:
                L[doc_id] = 1

    x = set(dict_inlinks.keys())
    y = set(L.keys())
    S = (list(x - y))

    print "number of pages with no out-links ",len(S)

num_of_outgoing_links()

def initial_pr():
    for x in P:
        PR[x] = (1.0/N)

def calc_sink():
    PR_sink = 0
    x = set(dict_inlinks.keys())
    y = set(L.keys())
    S = (list(x - y))
    for x in S:
        PR_sink+= PR[x]
    for x in P:
        PR_new[x] = (1-d)/N
        PR_new[x] = PR_new[x] + d * PR_sink/N

        try:
            for y in dict_inlinks[x]:
                PR_new[x] = PR_new[x] + d * PR[y]/(L[y])

        except:
            pass

    for x in P:
        PR[x] = PR_new[x]

# calculate perplexity
def calc_perp_num():
    PR_H = 0
    for x in P:
        PR_H = PR_H + PR[x] * math.log(float(PR[x]),2)

    perp_num = math.pow(2,-PR_H)

    return perp_num


# starting of pageRank algorithm
def compute_page_rank():
    initial_pr()
    num_iteration = 0
    perplexity_num = 0

    while num_iteration < 4:
        perplexity_num_temp = perplexity_num

        calc_sink()

        perplexity_num = calc_perp_num()

        # to check for convergence- if the change is less than one then increment the counter
        if abs(perplexity_num_temp - perplexity_num) < 1 :
            num_iteration = num_iteration+1
        else:
            num_iteration = 0

    PR_TEMP = sorted((list(set(PR.values()))), reverse=True)

    fopen = open ("PR_G1.txt", 'w+')

    # pages along with their page ranks- top 50
    for doc_id in PR_TEMP[0:50]:
        for key,value in PR.iteritems():
            if doc_id == value:
                temp1 = str(key)
                temp2 = str(doc_id)
                fopen.write(temp1 + " " + temp2 + "\n")

    fopen.close()

def start_pgm():
    compute_page_rank()
start_pgm()