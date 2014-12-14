'''
Created on Dec 12, 2014

@author: sscepano
'''
from os.path import isfile, join
from collections import defaultdict

# read in the relationship between department names and subprefs
def read_in_Departments():
    
    dept_sub = defaultdict(int)   
    i = 0
    path = "/home/sscepano/Project7s/D4D/CI/DATAexternal/geonames"
    file_name = "department_names_subpref_ids.csv"
    f_path = join(path,file_name)
    
    if isfile(f_path) and file_name != '.DS_Store':
            file7s = open(f_path, 'r')
            for line in file7s:
                i = i + 1
                dept, subpref = line.split('\t') 
                #print dept, subpref
                dept_sub[int(subpref)] = dept   
    print i                
    return dept_sub  

# this is the population of users we found in each subpref
def read_in_subpref_pop_stat():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/DATAexternal/geonames/home_num_users.tsv"
    f = open(file_name, "r")
    
    subpref_users = defaultdict(int)
    
    for line in f:
        subpref, users = line.split('\t')
        users = int(users)
        subpref = int(subpref)
              
        subpref_users[subpref] = users
    
    return subpref_users

# this is the population data found outside in geonames. Italian researchers told me to 
# just use PPL values for population
def read_in_Geonames():
    
    Geonames = defaultdict(int)
    # lines read in
    i = 0
    countPPLA = 0
    countPPLA2 = 0
   
    D4D_path_Geonames = "/home/sscepano/Project7s/D4D/CI/DATAexternal/geonames"
    file_name = "CI7s.txt"
    f_path = join(D4D_path_Geonames,file_name)
    print f_path
    if isfile(f_path) and file_name != '.DS_Store':
            file7s = open(f_path, 'r')
            for line in file7s:
                i = i + 1
                geonameid, name, asciiname, alternatenames, lat, lon, featureclas7s, featurecode, cc, cc2, admin1code, admin2code, admin3code, admin4code, population, elevation, dem, timezone, modificationdate = line.split('\t')

#                 print geonameid, name, asciiname, alternatenames, lat, lon, featureclas7s, featurecode, cc, cc2, admin1code, admin2code, admin3code, admin4code, population, elevation, dem, timezone, modificationdate
                # this is just to count PPLA values
                if  featurecode == 'PPLA':
                    countPPLA += 1
                    print asciiname 
                if  featurecode == 'PPLA2':
                    countPPLA2 += 1
                    print asciiname 
                    
                # this to assign the population (PPL, PPLA or PPLA2) values to the dict as output   
                if  featurecode == 'PPLA' or featurecode == 'PPLA2' or featurecode == 'PPL':
                    if int(population) <> 0:
                        Geonames[asciiname.upper()] = int(population)
                        print asciiname.upper(), int(population)
    
    print "PPLA", countPPLA, "PPLA2", countPPLA2
    print "Found places", len(Geonames)
    
    return Geonames


# this is the function that calls the others and sums the values for users and population
def find_dept_users_pop():
    
    Geonames = read_in_Geonames() 
    Departments = read_in_Departments()
    subpref_users = read_in_subpref_pop_stat()
    
    dept_users = defaultdict(int)
    dept_pop = defaultdict(int)
 
    for subpref in subpref_users.keys():
        if subpref <> 0 and subpref <> -1:
            dept = Departments[subpref]
            dept_users[dept] += subpref_users[subpref]
            print dept, subpref, subpref_users[subpref]
        
        
    for dept in Departments.values():  
        if dept in Geonames.keys():
            dept_pop[dept] = Geonames[dept]
    
    return dept_users, dept_pop
    
#     for el in Departments.values():
#         if el in Geonames.keys():
#             print el, Geonames[el]
#             s += 1        
#     print s
    

# here we just save the right values to files for further processing
def save_dept_users_pop():
    
    location = "/home/sscepano/Project7s/D4D/CI/DATAexternal/geonames"
    file_name = "dept_users_pop.tsv"
    save_path = join(location,file_name) 
    f = open(save_path, "w")
    
    dept_users, dept_pop = find_dept_users_pop()
    
    for dept in dept_users.keys():
        f.write(dept + '\t' + str(dept_users[dept]) + '\t' + str(dept_pop[dept]) + '\n')
    
    

# read_in_Geonames()    

# print find_dept_users_pop()

save_dept_users_pop()


