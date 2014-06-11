'''
Created on June 09, 2014

@author: sscepano
'''
# This one serves for the starting point 
import logging
import traceback
import multiprocessing

#####################################################
# imports distributor
#####################################################
from distribute import task_manager as D
#####################################################

_log = logging.getLogger(__name__)

def test():
    print 'cpu_count() = %d\n' % multiprocessing.cpu_count()

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.INFO, format='%(name)s: %(levelname)-8s %(message)s')
    
    test()
    
    # data1 will be the read in from all 10 parallel processes
    # data2 will be processed & arranged from those
    data1 = None
    data2 = None

    while True:
        raw_input("Press enter to start a process cycle:\n")
        try:
            reload(D)
        except NameError:
            _log.error("Could not reload the module.")
        try:
            # THIS THE FUNCTION YOU ARE TESTING
            ####################################################
            # this is for distributing the task 
            ####################################################
            print "Distribute task started."
            data1, data2 = D.distribute_task(data1, data2)
            print "Distribute task finished."
            ####################################################
            
        except Exception as e:
            _log.error("Caught exception from the process\n%s\n%s" % (e, traceback.format_exc()))

        _log.info("Cycle ready.")