'''
Created on Jun 9, 2014

@author: sscepano
'''
from datetime import date, datetime
from os.path import isfile, join
from collections import defaultdict
from multiprocessing import Pool
from itertools import repeat
import networkx as nx

# function for multithread support
def f((G, c)):
    G = read_in_commuting_patterns_all_subprefs(c, G)
    return G

# function to read A ... Z files in parallel
def read_in_all_multiprocessing():

    G = nx.DiGraph()
    
    print "Read data USING POOL started"
    p = Pool(processes=10)         
    data2 = p.map(f, zip(repeat(G), list(map(chr, range(ord('A'), ord('J')+1)))))
    
    return data2

def read_in_commuting_patterns_all_subprefs(c, G):
    
    # here we save # of all patterns found
    count_total_daily_patterns = 0
    # here we save all subprefs recorded for a user today
    usr_loc_today = defaultdict(int)
    # helping array
    current_day = defaultdict(int)
    # we assign empty arrays to all our users at start
    for usr in range(500001):
        usr_loc_today[usr] = []
        current_day[usr] = date.today() 
    
    # in this matrix we will save all users who made the commuting path in this week
    # later will function run_weekly_check() count all users who took the path 3 times at least
    # and only then increase the commuting edges weight
    weekly_patterns = defaultdict()
    for subpref in range(256):
        weekly_patterns[subpref] = defaultdict()
        for subpref2 in range(256):
            weekly_patterns[subpref][subpref2] = defaultdict(int)
    
    # dict with home for each user -- just to check how many commutes happen from home
    usr_home_subprefs = read_in_user_home_subprefs()
    # here we count how many of patterns found are from home back to home
    count_home_matches = 0
    
    # this is helping so that the first weekly check is done for each of files c on half date
    # after that date is passed when reading the file -- we set this to False and do no more checks 
    # till the end of the file when the new check happens
    weekly_check = True
    
    D4D_path_SET3 = "/home/sscepano/DATA SET7S/D4D/SET3TSV"
    file_name = "SUBPREF_POS_SAMPLE_" + c + ".TSV"
    #file_name = "100Klines.txt"
    #file_name= "usr50000.csv"
    f_path = join(D4D_path_SET3,file_name)
    if isfile(f_path) and file_name != '.DS_Store':
            file7s = open(f_path, 'r')
            for line in file7s:
                usr, call_time, subpref = line.split('\t')
                usr = int(usr)
                subpref = int(subpref)
                
                if subpref == -1:
                    #print "skip -1"
                    continue
                
                call_time = datetime.strptime(call_time, '%Y-%m-%d %H:%M:%S')
#                print current_day[usr]
#                print call_time.date()
                        
                # if read in a different day from the one so far, lets process the previous one
                if current_day[usr] <> call_time.date():
                    #print current_day[usr]
                    # this finds possible commuting today for the user usr
                    e = len(usr_loc_today[usr])
                    #print "e " + str(e)
                    #print usr_loc_today[usr]
                    # this checks when we found a new pattern to exit the loop (we count only the widest loop pattern) 
                    found_pattern = False
                    for end in range(e-1, 1, -1):
                        last_loc = usr_loc_today[usr][end]
                        #print "Last loc " + str(last_loc)
                        for i in range(end-1):
                            #print "\t" + "loc check i " + str(i) + " " + str(usr_loc_today[usr][i])
                            if last_loc == usr_loc_today[usr][i]:
                                found_pattern = True
                                count_total_daily_patterns += 1
                                if last_loc == usr_home_subprefs[usr]:
                                    count_home_matches += 1
                                k = 0
                                # this is where we save in the weekly_pattern the whole pattern found
                                while k < end-1:
                                    first_subpref = usr_loc_today[usr][k]
                                    second_subpref = usr_loc_today[usr][k+1]
                                    weekly_patterns[first_subpref][second_subpref][usr] += 1
                                    k += 1
                                break
                        if found_pattern:
                            break
                    usr_loc_today[usr] = [subpref]
                    current_day[usr] = call_time.date()
                else:
                    last_index =len(usr_loc_today[usr])-1
                    if usr_loc_today[usr][last_index] <> subpref:
                        usr_loc_today[usr].append(subpref)
                
                # here we do the check for the week
                if weekly_check:
                    if c == 'A' and call_time.date() >= datetime.strptime('2011-12-08', '%Y-%m-%d').date() \
                    or c == 'B' and call_time.date() >= datetime.strptime('2011-12-22', '%Y-%m-%d').date() \
                    or c == 'C' and call_time.date() >= datetime.strptime('2012-01-05', '%Y-%m-%d').date() \
                    or c == 'D' and call_time.date() >= datetime.strptime('2012-01-19', '%Y-%m-%d').date() \
                    or c == 'E' and call_time.date() >= datetime.strptime('2012-02-02', '%Y-%m-%d').date() \
                    or c == 'F' and call_time.date() >= datetime.strptime('2012-02-16', '%Y-%m-%d').date() \
                    or c == 'G' and call_time.date() >= datetime.strptime('2012-03-01', '%Y-%m-%d').date() \
                    or c == 'H' and call_time.date() >= datetime.strptime('2012-03-15', '%Y-%m-%d').date() \
                    or c == 'I' and call_time.date() >= datetime.strptime('2012-03-29', '%Y-%m-%d').date() \
                    or c == 'J' and call_time.date() >= datetime.strptime('2012-04-12', '%Y-%m-%d').date():
                        weekly_check = False
                        #print weekly_patterns[60]
                        G = run_weekly_check(G, weekly_patterns)
                        weekly_patterns = defaultdict()
                        for subpref in range(256):
                            weekly_patterns[subpref] = defaultdict()
                            for subpref2 in range(256):
                                weekly_patterns[subpref][subpref2] = defaultdict(int)

                        
    print ("Total patterns found ", count_total_daily_patterns)
    print ("Home matches found ", count_home_matches)     
    
    # I think here we will do the second weekly check for the 2weeks period
    G = run_weekly_check(G, weekly_patterns)
                   
    return G      

def read_in_commuting_patterns_subpref_users(c, G, subpref_id):
    
    print "Read data started for " + c
    
    usrs_list = read_in_subpref_users(subpref_id)
    NUM_USR = len(usrs_list)
    
    # here we save # of all patterns found
    count_total_daily_patterns = 0
    # here we save all subprefs recorded for a user today
    usr_loc_today = defaultdict(int)
    # helping array
    current_day = defaultdict(int)
    # we assign empty arrays to all our users at start
    for usr in range(500001):
        if usrs_list[usr] == 1:
            usr_loc_today[usr] = []
            current_day[usr] = date.today() 
    
    # in this matrix we will save all users who made the commuting path in this week
    # later will function run_weekly_check() count all users who took the path 3 times at least
    # and only then increase the commuting edges weight
    weekly_patterns = defaultdict()
    for subpref in range(256):
        weekly_patterns[subpref] = defaultdict()
        for subpref2 in range(256):
            weekly_patterns[subpref][subpref2] = defaultdict(int)
    
    # dict with home for each user -- just to check how many commutes happen from home
    usr_home_subprefs = read_in_user_home_subprefs()
    # here we count how many of patterns found are from home back to home
    count_home_matches = 0
    
    # this is helping so that the first weekly check is done for each of files c on half date
    # after that date is passed when reading the file -- we set this to False and do no more checks 
    # till the end of the file when the new check happens
    weekly_check = True
    
    D4D_path_SET3 = "/home/sscepano/DATA SET7S/D4D/SET3TSV"
    file_name = "SUBPREF_POS_SAMPLE_" + c + ".TSV"
    #file_name = "100Klines.txt"
    #file_name= "usr50000.csv"
    f_path = join(D4D_path_SET3,file_name)
    if isfile(f_path) and file_name != '.DS_Store':
            file7s = open(f_path, 'r')
            for line in file7s:
                usr, call_time, subpref = line.split('\t')
                usr = int(usr)
                subpref = int(subpref)
                
                if subpref == -1:
                    #print "skip -1"
                    continue
                
                if usrs_list[usr] <> 0:
                    continue
                
                call_time = datetime.strptime(call_time, '%Y-%m-%d %H:%M:%S')
#                print current_day[usr]
#                print call_time.date()
                        
                # if read in a different day from the one so far, lets process the previous one
                if current_day[usr] <> call_time.date():
                    #print current_day[usr]
                    # this finds possible commuting today for the user usr
                    e = len(usr_loc_today[usr])
                    #print "e " + str(e)
                    #print usr_loc_today[usr]
                    # this checks when we found a new pattern to exit the loop (we count only the widest loop pattern) 
                    found_pattern = False
                    for end in range(e-1, 1, -1):
                        last_loc = usr_loc_today[usr][end]
                        #print "Last loc " + str(last_loc)
                        for i in range(end-1):
                            #print "\t" + "loc check i " + str(i) + " " + str(usr_loc_today[usr][i])
                            if last_loc == usr_loc_today[usr][i]:
                                found_pattern = True
                                count_total_daily_patterns += 1
                                if last_loc == usr_home_subprefs[usr]:
                                    count_home_matches += 1
                                k = 0
                                # this is where we save in the weekly_pattern the whole pattern found
                                while k < end-1:
                                    first_subpref = usr_loc_today[usr][k]
                                    second_subpref = usr_loc_today[usr][k+1]
                                    weekly_patterns[first_subpref][second_subpref][usr] += 1
                                    k += 1
                                break
                        if found_pattern:
                            break
                    usr_loc_today[usr] = [subpref]
                    current_day[usr] = call_time.date()
                else:
                    last_index =len(usr_loc_today[usr])-1
                    if usr_loc_today[usr][last_index] <> subpref:
                        usr_loc_today[usr].append(subpref)
                
                # here we do the check for the week
                if weekly_check:
                    if c == 'A' and call_time.date() >= datetime.strptime('2011-12-08', '%Y-%m-%d').date() \
                    or c == 'B' and call_time.date() >= datetime.strptime('2011-12-22', '%Y-%m-%d').date() \
                    or c == 'C' and call_time.date() >= datetime.strptime('2012-01-05', '%Y-%m-%d').date() \
                    or c == 'D' and call_time.date() >= datetime.strptime('2012-01-19', '%Y-%m-%d').date() \
                    or c == 'E' and call_time.date() >= datetime.strptime('2012-02-02', '%Y-%m-%d').date() \
                    or c == 'F' and call_time.date() >= datetime.strptime('2012-02-16', '%Y-%m-%d').date() \
                    or c == 'G' and call_time.date() >= datetime.strptime('2012-03-01', '%Y-%m-%d').date() \
                    or c == 'H' and call_time.date() >= datetime.strptime('2012-03-15', '%Y-%m-%d').date() \
                    or c == 'I' and call_time.date() >= datetime.strptime('2012-03-29', '%Y-%m-%d').date() \
                    or c == 'J' and call_time.date() >= datetime.strptime('2012-04-12', '%Y-%m-%d').date():
                        weekly_check = False
                        #print weekly_patterns[60]
                        G = run_weekly_check(G, weekly_patterns)
                        weekly_patterns = defaultdict()
                        for subpref in range(256):
                            weekly_patterns[subpref] = defaultdict()
                            for subpref2 in range(256):
                                weekly_patterns[subpref][subpref2] = defaultdict(int)

                        
    print ("Total patterns found ", count_total_daily_patterns)
    print ("Home matches found ", count_home_matches)     
    
    # I think here we will do the second weekly check for the 2weeks period
    G = run_weekly_check(G, weekly_patterns)
                   
    return G    


def run_weekly_check(G, weekly_patterns):
    #print "Weekly check"
    for subpref1 in weekly_patterns.iterkeys():
        for subpref2 in weekly_patterns[subpref1].iterkeys():
            for usr in weekly_patterns[subpref1][subpref2].iterkeys():
                if weekly_patterns[subpref1][subpref2][usr] > 3:
                    if G.has_edge(subpref1, subpref2):
                        G[subpref1][subpref2]['weight'] += 1
                    else:
                        G.add_edge(subpref1, subpref2, weight = 1)

    return G  


def read_in_subpref_users(subpref):

    D4DPath = "/home/sscepano/Project7s/D4D/CI/COMMUTINGNEW/data"
    file7s = "Subprefs_and_their_users.tsv"
    f = open(join(D4DPath,file7s), 'r')
    
    usrs_list = defaultdict(int)
    
    for line in f:
        line_elems = line.split('\t')
        subpref_id = line_elems[0]
        subpref_id = int(subpref_id[:-1])
        if subpref_id == subpref:
            for i in range(1, len(line_elems)):
                usr = int(line_elems[i])
                usrs_list[usr] = 1
            break
        
    return usrs_list


def read_in_user_home_subprefs():

    D4DPath = "/home/sscepano/Project7s/D4D/CI/COMMUTINGNEW/data"
    file7s = "Users_and_their_homes.tsv"
    f = open(join(D4DPath,file7s), 'r')
    
    usrs_subprefs = defaultdict(int)
    
    for line in f:
        usr, subpref = line.split('\t')
        usr = int(usr)
        subpref = int(subpref)
        usrs_subprefs[usr] = subpref
      
    return usrs_subprefs