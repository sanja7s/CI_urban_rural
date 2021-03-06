'''
Created on Jun 9, 2014

@author: sscepano
'''
import numpy

from os.path import join
from collections import defaultdict

#######################################################################################      
# this is where we save the extracted data needed for the next steps to .TSV files
####################################################################################### 
def save_home_work(data):
    
    print len(data)
    
    location = "/home/sscepano/Project7s/D4D/CI/urban_rural/home_work/OUTPUT_files_new"
    file_name = "users_home_frequency.tsv"
    file_name2 = "users_home.tsv"
    save_path = join(location,file_name)
    save_path2 = join(location,file_name2)
    f = open(save_path, "w")
    f2 = open(save_path2, "w")
    
    for user in data['home'].keys():
        f.write(str(user) + ':\t')
        f2.write(str(user) + ':\t')
        for subpref in data['home'][user].keys():
            f.write(str(subpref) + ':' + str(data['home'][user][subpref]) + '\t')
            f2.write(str(subpref) + '\t') 
        f.write('\n')
        f2.write('\n')
        
    file_name3 = "users_work_frequency.tsv"
    file_name4 = "users_work.tsv"
    save_path = join(location,file_name3)
    save_path2 = join(location,file_name4)
    f = open(save_path, "w")
    f2 = open(save_path2, "w")
    
    for user in data['work'].keys():
        f.write(str(user) + ':\t')
        f2.write(str(user) + ':\t')
        for subpref in data['work'][user].keys():
            f.write(str(subpref) + ':' + str(data['work'][user][subpref]) + '\t')
            f2.write(str(subpref) + '\t') 
        f.write('\n')
        f2.write('\n')
        
        
    file_name5 = "users_home_work.tsv"
    save_path = join(location,file_name5)
    f = open(save_path, "w")
    
    user_home_work = select_only_home_work(data)
     
    for user in user_home_work.keys():
        f.write(str(user) + ':\t')
         
        try:
            f.write(str(user_home_work[user][0]) + '\t')
            f.write(str(user_home_work[user][1]) + '\t') 
        except KeyError:
            print "KeyError"
        f.write('\n') 
    
    return

def save_filtered_input(data):
    
    location = "/home/sscepano/Project7s/D4D/CI/urban_rural/home_work/OUTPUT_files_new"
    file_name = "users_home_work_filtered_v3.tsv"
    save_path = join(location,file_name)
    f = open(save_path, "w")
    
    cnt_diff_subprefs = defaultdict(int)
    cnt_commuters = 0 
    for user in data.keys():
        f.write(str(user) + '\t')
        try:
            f.write(str(data[user][0]) + '\t')
            f.write(str(data[user][1])) 
            cnt_diff_subprefs[data[user][1]] = 1
            cnt_diff_subprefs[data[user][0]] = 1
            if data[user][0] <> data[user][1]:
                cnt_commuters += 1
        except KeyError:
            print "KeyError"
        f.write('\n') 
    print cnt_commuters
    print sum(cnt_diff_subprefs.values())

##################################################################################################################################
## This code has to do with our reviewers comments. I will check what is the situation 
## with found homes, and how statistically significant we can claim they are, before making any changes.
##################################################################################################################################
def save_STATS_on_home_work(data):
      
    location = "/home/sscepano/Project7s/D4D/CI/urban_rural/home_work/OUTPUT_files_new"
    file_name = "users_home_frequency_STATS.tsv" 
    save_path = join(location,file_name)
    fh = open(save_path, "w")
    
    file_namef = "users_home_frequency_STATS_FILTERED_gr30tot.tsv" 
    save_pathf = join(location,file_namef)
    fhf = open(save_pathf, "w")
    
    file_name2 = "users_work_frequency_STATS.tsv" 
    save_path2 = join(location,file_name2)
    fw = open(save_path2, "w")
    
    file_name2f = "users_work_frequency_STATS_FILTERED_gr30tot.tsv" 
    save_path2f = join(location,file_name2f)
    fwf = open(save_path2f, "w")
    
    less_than_100_calls = 0
    less_than_100_calls_first = 0
    ant_neg = 0
    firstfq_gr08 = 0
    for k in data['home'].keys():
        sumant = 0
        countant = 0
        for ant in data['home'][k].items():
            sumant += ant[1]
            countant += 1
        try:
            firstant = data['home'][k].itervalues().next()
            firstantid = data['home'][k].iterkeys().next()
            firstfq = numpy.float64(firstant)/sumant 
        except StopIteration:
            firstant = 0
            firstantid = 0
            firstfq = 0        
#         f.write( str(k) + '\t' + str(firstantid) + '\t' + str(countant) + '\t' +  str(sumant) + '\t' + str(firstant) + '\t' + str(numpy.float64(firstant)/sumant) + '\n')
        if sumant < 30:
            less_than_100_calls += 1
            less_than_100_calls_first += 1
            print k
#         elif firstant < 100:
#             less_than_100_calls_first += 1
#             print k
        elif int(firstantid) == -1:
            ant_neg += 1
        elif firstfq <> 'inf' and firstfq >= 0.5:
            fhf.write( str(k) + '\t' + str(firstantid) + '\t' + str(countant) + '\t' +  str(sumant) + '\t' + str(firstant) + '\t' + str(firstfq) + '\n')
        
        fh.write( str(k) + '\t' + str(firstantid) + '\t' + str(countant) + '\t' +  str(sumant) + '\t' + str(firstant) + '\t' + str(firstfq) + '\n')
             
    print less_than_100_calls, less_than_100_calls_first, ant_neg
    
    
    
    for k in data['work'].keys():
        sumant = 0
        countant = 0
        for ant in data['work'][k].items():
            sumant += ant[1]
            countant += 1
        try:
            firstant = data['work'][k].itervalues().next()
            firstantid = data['work'][k].iterkeys().next()
            firstfq = numpy.float64(firstant)/sumant
        except StopIteration:
            firstant = 0
            firstantid = 0
            firstfq = 0 
#         f.write( str(k) + '\t' + str(firstantid) + '\t' + str(countant) + '\t' +  str(sumant) + '\t' + str(firstant) + '\t' + str(numpy.float64(firstant)/sumant) + '\n')
        if sumant < 30:
            less_than_100_calls += 1
            less_than_100_calls_first += 1
            print k
#         elif firstant < 100:
#             less_than_100_calls_first += 1
#             print k
        elif int(firstantid) == -1:
            ant_neg += 1
        elif firstfq <> 'inf' and firstfq >= 0.5:
            fwf.write( str(k) + '\t' + str(firstantid) + '\t' + str(countant) + '\t' +  str(sumant) + '\t' + str(firstant) + '\t' + str(firstfq) + '\n')
     
        fw.write( str(k) + '\t' + str(firstantid) + '\t' + str(countant) + '\t' +  str(sumant) + '\t' + str(firstant) + '\t' + str(firstfq) + '\n')
            
    print less_than_100_calls, less_than_100_calls_first, ant_neg
    
    return

#######################################################################################      
# in the  input we take and rank by the frequency of a user calls all the subprefs he
# visited. Here we extract just the first one from the non-working hours for HOME, 
#and first one from the working hours for WORK
####################################################################################### 
def select_only_home_work(data):
    
    user_home_work = defaultdict(int)
    
    for user in data['home'].keys():
        user_home_work[user] = defaultdict(int)
        try:
            user_home_work[user][0] = data['home'][user].keys()[0]
        except IndexError:
            print
        
    for user in data['work'].keys():
        try:
            user_home_work[user] = user_home_work.get(user, defaultdict(int))
            user_home_work[user][1] = data['work'][user].keys()[0]
        except IndexError:
            print
        
    return user_home_work


#######################################################################################      
# read in home work data per user and count commuters and save the graph as weighted edge list
#######################################################################################
def cnt_commuting_from_home_work(data=None):
    
    commuting_graph = defaultdict(int)
    
    if data == None:
    
        location = "/home/sscepano/Project7s/D4D/CI/urban_rural/home_work/OUTPUT_files_new"
        file_name = "users_home_work_filtered_v2.tsv"
        save_path = join(location,file_name)
        f = open(save_path, "r")
        
        for line in f:
    
            usr, home, work, empty = line.split('\t')
            usr = int(usr)
            home = int(home)
            work = int(work)
            print usr, home, work
            
            commuting_graph[home] = commuting_graph.get(home, defaultdict(int))
            commuting_graph[home][work] += 1
            
    else:
        
        for usr in data.keys():
            home = data[usr][0]
            work = data[usr][1]
#             print home, work
            commuting_graph[home] = commuting_graph.get(home, defaultdict(int))
            commuting_graph[home][work] += 1
#             print commuting_graph[home]
        
    
    location2 = "/home/sscepano/Project7s/D4D/CI/urban_rural/home_work/OUTPUT_files_new"
    file_name2 = "commuting_graph_from_home_work_filtered_no_self_loops_v2.tsv"
    save_path = join(location2,file_name2)
    f2 = open(save_path, "w")    
        
    for home in commuting_graph.keys():
        for work in commuting_graph[home].keys():
            if home <> work:
                f2.write(str(home) + '\t' + str(work) + '\t' + str(commuting_graph[home][work]) + '\n')
        
    return


# cnt_commuting_from_home_work()
   
