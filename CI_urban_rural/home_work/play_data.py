'''
Created on Jun 10, 2014

@author: sscepano
'''
from collections import defaultdict, OrderedDict

#######################################################################################      
# this one is for calling other functions needed with the data
#######################################################################################  
def play_data(data1, data2):
    
#    data2 = arrange_all_data(data1)

#    data2 = test_data(data1, data2)

    return data2


#######################################################################################      
# this one is to learn what you need and how the data looks
#######################################################################################  
def test_data(data1, data2):
    
    print "TESTING starts"
    
    print len(data1)
#     print len(data1[0])
    i = 0
    for k in data1[0]['home'].keys():
        i += 1
        print k, data1[0]['home'][k]
        print k, data2['home'][k]
        print data2['home'][k].keys()[0]
        if i == 15:
            break
    
    print len(data2)
#     print len(data2['home'])
#      
#     i = 0   
#     for k in data2['home'].keys():
#         i += 1
#         print k, data2['home'][k]
#         try:
#             print data2['home'][k].itervalues()
#         except KeyError:
#             print "Empty"
#         if i == 33:
#             break
    
    print "TESTING ends"
    
    return data2

#######################################################################################      
# this one is for summing the parallel output & other formal arrangement
#######################################################################################      
def arrange_all_data(data1):
    
    data2 = sum_multitasking_output(data1)
  
    data2 = sort_and_find_home_work(data2)

    return data2

#######################################################################################      
# we need sorting as the home & work will be the most frequently visited locations
#######################################################################################  
def sort_and_find_home_work(data):
    
    data3 = defaultdict()
    data3['home'] = defaultdict()
    data3['work'] = defaultdict()
    
    for user in data['home'].keys():
        data3['home'][user] = OrderedDict(sorted(data['home'][user].iteritems(), key=lambda t:t[1], reverse = True))

    for user in data['work'].keys():
        data3['work'][user] = OrderedDict(sorted(data['work'][user].iteritems(), key=lambda t:t[1], reverse = True))   
    
    return data3

#######################################################################################      
# do not want to call this one unless the data is an array of 10, i.e., parallel output
#######################################################################################  
def sum_multitasking_output(data):
    
    if len(data) >= 10:
    
        data2 = defaultdict(int)
        data2['home'] = defaultdict(int)
        data2['work'] = defaultdict(int)
        
        for i in range(10):
            for k in data[i]['home'].keys():
                data2['home'][k] = data2['home'].get(k, defaultdict(int))
                for k2 in data[i]['home'][k].keys():
                    data2['home'][k][k2] += data[i]['home'][k][k2]
            for k in data[i]['work'].keys():
                data2['work'][k] = data2['work'].get(k, defaultdict(int))
                for k2 in data[i]['work'][k].keys():
                    data2['work'][k][k2] += data[i]['work'][k][k2]
                    
    else:
        print "DID NOTHING in multitasking, as the data seems to be already summed"
    
    return data2