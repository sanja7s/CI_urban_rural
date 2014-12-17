'''
Created on Jun 10, 2014

@author: sscepano
'''
from collections import defaultdict, OrderedDict
import numpy
#######################################################################################      
# this one is for calling other functions needed with the data
#######################################################################################  
def play_data(data1, data2):
    
#     data2 = arrange_all_data(data1)

#     data2 = test_data(data1, data2)

    data2 = filter_data(data1, data2, 0.8, 100)

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
# this one is to filter the data for output, in following way: 
# K is the filter for the most frequent location (pct of calls made there from total)
# N is for the number of calls the user has to have made in the first location
# this function will result on one data dict with home work only location for each user as key
#######################################################################################  
def filter_data(data1, data2, K=0.5, N=30):
    
    # we take the right data that are read in the memory
    data = data2
    # filtered output qill go to data7s
    data7s = defaultdict()
    
    print "FILTERING starts"
    
    less_than_N_calls_first = 0
    ant_neg = 0
    
    cnt_diff_hw = 0

    # k is iterating over users for whom we found a home
    for k in data['home'].keys():
        # total number of calls made in home/work hours
        # and the number of locations found respectively
        sumhome = 0
        sumwork = 0
        counthome = 0
        countwork = 0
        # interate through found home/work locations and count right values
        for ant in data['home'][k].items():
            sumhome += ant[1]
            counthome += 1
        for ant in data['work'][k].items():
            sumwork += ant[1]
            countwork += 1
        # try is for the cases when one is not found or so, not to break the func
        try:
            homecalls = data['home'][k].itervalues().next()
            homeid = data['home'][k].iterkeys().next()
            homefq = numpy.float64(homecalls)/sumhome 
            workcalls = data['work'][k].itervalues().next()
            workid = data['work'][k].iterkeys().next()
            workfq = numpy.float64(workcalls)/sumwork 
        except StopIteration:
            homecalls = 0
            homeid = 0
            homefq = 0 
            workcalls = 0
            workid = 0
            workfq = 0    
        # here comes the actual FILTERING
        # if we did not find that user has made N calls in his home/work location (first one), filter him out  
        if sumhome < N:
            less_than_N_calls_first += 1
            print k
        elif workcalls < N:
            less_than_N_calls_first += 1
            print k
        elif int(homeid) == -1 or int(workid) == -1:
            ant_neg += 1
        elif int(homeid) == 0 or int(workid) == 0:
            print k
        # the last filter is for boundary case and not frequent enough first location (< K)
        elif homefq <> 'inf' and homefq >= K and workfq <> 'inf' and workfq >= K:
            data7s[k] = (homeid, workid)
            if homeid <> workid:
                cnt_diff_hw += 1
                print k, homeid, workid
        
    print cnt_diff_hw
    print "FILTERING ends"
    
    return data7s



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