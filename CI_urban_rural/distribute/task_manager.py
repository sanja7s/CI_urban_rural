'''
Created on Jun 9, 2014

@author: sscepano
'''
from distribute import home_work_tasks as hw


def distribute_task(data1, data2):
    
    try:
        reload(hw)
    except NameError:
        print "NameError"
     
#######################################################################################      
# this part is for reading in the data; comment out after the first step
#######################################################################################   
#     if data1 is None:
#         print "Read data started"
#         data1 = hw.read_data()
#         print "Read data finished"
        
#######################################################################################      
# this part is for playing with the data, so testing & arranging them as needed
#######################################################################################           
#     print "before playing ", len(data1)
#     data2 = hw.play_data(data1, data2)
#     print "after playing ", len(data2)
        
#######################################################################################      
# this part is for saving  the data, after you learned them from playing
#######################################################################################  
    hw.save_data(data2)
        
    return data1, data2