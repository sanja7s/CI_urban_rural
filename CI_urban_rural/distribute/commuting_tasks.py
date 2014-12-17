'''
Created on Jun 9, 2014

@author: sscepano
'''
import commuting.read_in as rd
import commuting.save_output as so
import commuting.map_output as mo
import commuting.play_data as pd
 
#######################################################################################      
# the functions for home work to be called by the distributor -- task manager
#######################################################################################   
def read_data():
    
    try:
        reload(rd)
    except Exception as e:
        print e
    
    print "Read data multiprocesing"
    data = rd.read_in_all_multiprocessing()

    print len(data)
    
    return data

def play_data(data1, data2):

    try:
        reload(pd)
    except Exception as e:
        print e
            
    return pd.play_data(data1, data2)

def save_data(data):

    try:
        reload(so)
    except Exception as e:
        print e
            
#     mo.map_commute_from_home2work(data)
    so.save_commuting_graph(data)
#     mo.map_commutes(data)


    
