'''
Created on Jun 15, 2014

@author: sscepano
'''
###########################################################################################################
### computes how many people per home subpref & how many of them commute and saves to output files
###########################################################################################################
from collections import defaultdict

def save_per_home_stats():
    
    file_name = "/home/sscepano/Project7s/D4D/CI/urban_rural/divide_by_home/OUTPUT_files/Cleaned/users_home.tsv"
    f = open(file_name, "w")
    
    user_home_work = read_in_home_work_output()
    home_num_users = defaultdict(int)
    home_num_commuters = defaultdict(int)
    
    for user in user_home_work.iterkeys():
        home = user_home_work[user][0]
        if home == 0:
            print user, user_home_work[user][1]
        f.write(str(user) + '\t' + str(home) + '\n')
        home_num_users[home] += 1
        if home <> user_home_work[user][1] and user_home_work[user][1] <> -1:
            home_num_commuters[home] += 1
        
    file_name2 = "/home/sscepano/Project7s/D4D/CI/urban_rural/divide_by_home/OUTPUT_files/Cleaned/home_num_users.tsv"
    f2 = open(file_name2, "w")
    
    file_name3 = "/home/sscepano/Project7s/D4D/CI/urban_rural/divide_by_home/OUTPUT_files/Cleaned/home_num_commuters.tsv"
    f3 = open(file_name3, "w")
    
    for home in home_num_users.iterkeys():
        f2.write(str(home) + '\t' + str(home_num_users[home])+ '\n')
        f3.write(str(home) + '\t' + str(home_num_users[home])+ '\t' + str(home_num_commuters[home]) + '\n')
        

def save_per_work_stats():
    
    file_name = "/home/sscepano/Project7s/D4D/CI/urban_rural/divide_by_home/OUTPUT_files/Cleaned/users_work.tsv"
    f = open(file_name, "w")
    
    user_home_work = read_in_home_work_output()
    work_num_users = defaultdict(int)
    work_num_commuters = defaultdict(int)
    
    for user in user_home_work.iterkeys():
        work = user_home_work[user][1]
        f.write(str(user) + '\t' + str(work) + '\n')
        work_num_users[work] += 1
        if work <> user_home_work[user][0] and user_home_work[user][1] <> -1:
            work_num_commuters[work] += 1
        
    file_name2 = "/home/sscepano/Project7s/D4D/CI/urban_rural/divide_by_home/OUTPUT_files/Cleaned/work_num_users.tsv"
    f2 = open(file_name2, "w")
    
    file_name3 = "/home/sscepano/Project7s/D4D/CI/urban_rural/divide_by_home/OUTPUT_files/Cleaned/work_num_commuters.tsv"
    f3 = open(file_name3, "w")
    
    for work in work_num_users.iterkeys():
        f2.write(str(work) + '\t' + str(work_num_users[work])+ '\n')
        f3.write(str(work) + '\t' + str(work_num_users[work])+ '\t' + str(work_num_commuters[work]) + '\n')


def read_in_home_work_output():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/urban_rural/home_work/OUTPUT_files/vCleaned/users_home_work.tsv"
    f = open(file_name, "r")
    
    user_home_work = defaultdict(int)
    
    for line in f:
        user, home, work, nothing = line.split('\t')
        user = int(user[:-1])
        home = int(home)
        work = int(work)
        
        user_home_work[user] = defaultdict(int)
        user_home_work[user][0] = home
        user_home_work[user][1] = work
    
    return user_home_work


# save_per_home_stats()

save_per_work_stats()