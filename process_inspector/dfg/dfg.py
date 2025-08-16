# Process Inspector
# Contributors:
# - Aravind Sankaran

import time
# import pm4py
from collections import Counter
import pickle
import os
from .logging_config import logger


class DFG:
    def __init__(self,activity_log=None):
        self.nodes = None
        self.edges = None
        self.im = None
        self.fm = None
        
        
        self.ready = False
        
        if activity_log:
            self.construct(activity_log)
            
    
    def construct(self, activity_log):
        start = time.time()
        self.nodes = set(activity_log.activity_events.keys())
        # self.edges,self.im,self.fm = pm4py.discover_dfg(activity_log.activity_log)
        self.edges,self.im,self.fm = self.discover_dfg(activity_log.activity_log)
        end = time.time()
        logger.info(f"[DFG] elapsed: {end - start:.4f} s") 
        self.ready = True  
    
    
    def discover_dfg(self, activity_log):
        im = Counter()
        fm = Counter()
        edges = Counter()
        for activit_trace, count in activity_log.items():
            im[activit_trace[0]] += count
            fm[activit_trace[-1]] += count
            
            for i in range(len(activit_trace) - 1):
                edge = (activit_trace[i], activit_trace[i + 1])
                edges[edge] += count
                
        return edges, im, fm
        
    def save(self, data_dir):
        os.makedirs(data_dir, exist_ok=True)
        dfg_file = os.path.join(data_dir, 'dfg.pkl')
        try:
            if self.ready:
                with open(dfg_file, 'wb') as f:
                    pickle.dump({'nodes': self.nodes, 'edges':self.edges, 'im':self.im, 'fm':self.fm}, f)
                logger.info(f"DFG saved to {dfg_file}")
                return True
            else:
                logger.error("DFG not initialized, cannot save")
        except Exception as e:
            logger.error(f"Error saving DFG: {e}")

        return False        
    
    def restore(self, data_dir):
        dfg_file = os.path.join(data_dir, 'dfg.pkl')
        
        if not os.path.exists(dfg_file):
            logger.error(f"DFG file {dfg_file} does not exist.")
            raise FileNotFoundError(f"DFG file {dfg_file} does not exist.")
        
        try:
            with open(dfg_file, 'rb') as f:
                data = pickle.load(f)
                self.nodes = data['nodes']
                self.edges = data['edges']
                self.im = data['im']
                self.fm = data['fm']
            logger.info(f"DFG restored from {dfg_file}")
            self.ready = True
            
        except Exception as e:
            logger.error(f"Error restoring DFG: {e}")
            raise e
        
        

# if __name__ == "__main__":
#     import logging
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    
#     import pandas as pd
#     from .mappings.swlibs import f_swlibs
#     from .mappings.pathstrings import f_pathstrings
#     paths = [
#         ("/proj/nobackup/", "/proj"),
#         ("/home/", "/home"),
#         ("/dev/shm/", "/dev/shm"),
#         ("/sys/", "/sys"),
#         ("/proc/", "/proc"),
#     ]
    
#     from .activity_log import ActivityLog
        
#     el = pd.read_pickle("tests/logs/sample_el.pkl")
#     # activity_log = ActivityLog(el, 18, f_swlibs)
#     activity_log = ActivityLog(el, 4, f_pathstrings,paths=paths)

#     dfg = DFG(activity_log.activity_log)
#     print(dfg.dfg)

    
    