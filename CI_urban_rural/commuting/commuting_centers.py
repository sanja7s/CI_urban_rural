'''
Created on Jun 17, 2014

@author: sscepano
'''
########################################################
### here we read in the previous output for home work
### and find which work places are most popular for
### the commuters (i.e., which are commuting centers)
########################################################
from collections import defaultdict

########################################################
# just pick up the previous output
########################################################
def read_in_home_work_output():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/urban_rural/home_work/OUTPUT_files/users_work_home.tsv"
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

########################################################
# if the user travels to work (<> home) count this 
# work as commuting center
########################################################
def find_commuting_centers():
    
    home_work = read_in_home_work_output()
    
    work_num_commuters = defaultdict(int)
    home_num_commuters = defaultdict(int)
    
    for user in home_work.keys():
        home = home_work[user][0]
        work = home_work[user][1]
        if home <> work and home <> -1 and work <> -1:
            work_num_commuters[work] += 1
            home_num_commuters[home] += 1
        
    return work_num_commuters, home_num_commuters


########################################################
# just save this output
########################################################
def save_num_commuters():
    
    file_name = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/work_num_commuters.tsv"
    f = open(file_name, "w")
    file_name2 = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/home_num_commuters.tsv"
    f2 = open(file_name2, "w")
    
    work_num_commuters, home_num_commuters = find_commuting_centers()
    
    for subpref in work_num_commuters.keys():
        f.write(str(subpref) + '\t' + str(work_num_commuters[subpref]) + '\n')
        f2.write(str(subpref) + '\t' + str(home_num_commuters[subpref]) + '\n')
        
        
########################################################
# extract weighted directed commuting graph 
# subprefs are nodes, weight is the num of commuters
########################################################
def calculate_commuting_graph():
    
    home_work = read_in_home_work_output()
    
    commuting_graph = defaultdict(int)
    
    for user in home_work.keys():
        home = home_work[user][0]
        work = home_work[user][1]
        if home <> work and home <> -1 and work <> -1:
            commuting_graph[home] = commuting_graph.get(home, defaultdict(int))
            commuting_graph[home][work] += 1
        
    return commuting_graph

def save_commuting_graph():
    
    g = calculate_commuting_graph()
    
    file_name = "/home/sscepano/Project7s/D4D/CI/commuting_centers/OUTPUT_files/commuting_graph.tsv"
    f = open(file_name, "w")
    
    for k in g.keys():
        for k2 in g[k].keys():
            f.write(str(k) + '\t' + str(k2) + '\t' + str(g[k][k2]) + '\n' )

### only for saving        
# save_num_commuters()

### also for calculating the edge graph
# calculate_commuting_graph()
# save_commuting_graph()    