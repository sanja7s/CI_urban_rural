'''
Created on Jun 9, 2014

@author: sscepano
'''
from datetime import date
from os.path import isfile, join
from collections import defaultdict
from multiprocessing import Pool
from itertools import repeat

# function for multithread support
def f((data, i)):
    data = read_in_home_work(i, data)
    return data

# function to read A ... Z files in parallel
def read_in_all_multiprocessing():

    data = defaultdict(int)
    
    data['home'] = defaultdict(int)
    data['work'] = defaultdict(int)
    
    print "Read data USING POOL started"
    p = Pool(processes=10)         
    data2 = p.map(f, zip(repeat(data), list(map(chr, range(ord('A'), ord('J')+1)))))
    
    return data2

def read_in_home_work(c, homework):
    
    print "Read data started for " + c
    
    # lines read in
    i = 0
    
    D4D_path_SET3 = "/home/sscepano/DATA SET7S/D4D/SET3TSV"
    file_name = "SUBPREF_POS_SAMPLE_" + c + ".TSV"
    f_path = join(D4D_path_SET3,file_name)
    if isfile(f_path) and file_name != '.DS_Store':
            file7s = open(f_path, 'r')
            for line in file7s:
                i = i + 1
                usr, call_time, subpref = line.split('\t')
                subpref = int(subpref[:-1])
                if subpref <> -1:
                    homework['home'][usr] = homework['home'].get(usr, defaultdict(int))
                    homework['work'][usr] = homework['work'].get(usr, defaultdict(int))
                    call_hour = int(call_time[11:13])
                    call_date = date(int(call_time[:4]), int(call_time[5:7]), int(call_time[8:10]))
         
                    # just from time to time testing printing to know we are reading in still
                    if i in [10000, 100000, 1000000, 10000000, 100000000]:
                        print i, len(homework['home']), len(homework['work'])
                    
                    # the KeyError checks below might not be necessary since we have .get above, but it works fine 
                    if call_date.weekday() < 5:
                        if call_hour > 19 or call_hour <= 5:
                            try:
                                homework['home'][usr][subpref] += 1
                            except KeyError:
                                homework['home'][usr][subpref] = 1
                        else:
                            try:
                                homework['work'][usr][subpref] += 1
                            except KeyError:
                                homework['work'][usr][subpref] = 1
                    else:
                        try:
                            homework['home'][usr][subpref] += 1
                        except KeyError:
                            homework['home'][usr][subpref] = 1
    
    print i     
    print "Read data finished for " + c       
    return homework