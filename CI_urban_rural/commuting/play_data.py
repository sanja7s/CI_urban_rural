'''
Created on Jun 10, 2014

@author: sscepano
'''
from collections import defaultdict, OrderedDict
import numpy
import networkx as nx

#######################################################################################      
# this one is for calling other functions needed with the data
#######################################################################################  
def play_data(data1, data2):
    
    data2 = arrange_all_data(data1)

#     data2 = test_data(data1, data2)

#     data2 = filter_data(data1, data2, 0.8, 100)

    return data2


#######################################################################################      
# this one is to learn what you need and how the data looks
#######################################################################################  
def test_data(data1, data2):
    
    print "TESTING starts"
    
#     print len(data1)
# #     print len(data1[0])
#     i = 0
#     for k in data1[0]['home'].keys():
#         i += 1
#         print k, data1[0]['home'][k]
#         print k, data2['home'][k]
#         print data2['home'][k].keys()[0]
#         if i == 15:
#             break
    
    print len(data2)
    print len(data2['home'])
      
    i = 0   
    for k in data2['home'].keys():
        i += 1
        print k, data2['home'][k]
        try:
            print data2['home'][k].itervalues()
        except KeyError:
            print "Empty"
        sumant = 0
        countant = 0
        for ant in data2['home'][k].items():
            sumant += ant[1]
            countant += 1
        print k, countant, sumant, data2['home'][k].itervalues().next(), data2['home'][k].iterkeys().next()
        if i == 33:
            break
        
    
    print "TESTING ends"
    
    return data2

#######################################################################################      
# this one is for summing the parallel output & other formal arrangement
#######################################################################################      
def arrange_all_data(data1):
    
    data2 = sum_multitasking_output(data1)
  
#     data2 = sort_and_find_home_work(data2)

    return data2


#######################################################################################      
# do not want to call this one unless the data is an array of 10, i.e., parallel output
#######################################################################################  
def sum_multitasking_output(data):
    
    if len(data) >= 10:
    
        data2 = nx.DiGraph()
        
        for i in range(10):
            for u, v, w in data[i].edges(data=True):
                if data2.has_edge(u, v):
                    data2[u][v]['weight'] += w['weight']
                    print data2[u][v]['weight'] , w['weight']
                else:
                    data2.add_edge(u, v, weight = 1)
                    
    else:
        print "DID NOTHING in multitasking, as the data seems to be already summed"
    
    return data2