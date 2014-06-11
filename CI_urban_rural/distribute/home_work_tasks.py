'''
Created on Jun 9, 2014

@author: sscepano
'''
import home_work.read_in as rd
import home_work.save_output as so
import home_work.play_data as pd

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
            
#     so.save_home_work(data)
    so.map_commute_from_home2work(data)


    
