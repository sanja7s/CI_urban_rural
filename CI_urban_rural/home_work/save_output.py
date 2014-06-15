'''
Created on Jun 9, 2014

@author: sscepano
'''
from os.path import join
from collections import defaultdict
import networkx as nx

def save_home_work(data):
    
    print len(data)
    
    location = "/home/sscepano/Project7s/D4D/CI/urban_rural/home_work/OUTPUT_files"
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
        
        
    file_name5 = "users_work_home.tsv"
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