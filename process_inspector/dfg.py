# Process Inspector
# Contributors:
# - Aravind Sankaran

import time
import pm4py
import pickle
import os
from .logging_config import logger


class DFG:
    def __init__(self,activity_log=None):
        self.dfg = None
        self.im = None
        self.fm = None
        self.inv_mapping = None
        self.ready = False
        
        if activity_log:
            self.construct(activity_log)
            self.inv_mapping = activity_log.inv_mapping    
            
    
    def construct(self, activity_log):
        start = time.time()
        self.dfg,self.im,self.fm = pm4py.discover_dfg(activity_log.activity_log)
        end = time.time()
        logger.info(f"[DFG] elapsed: {end - start:.4f} s") 
        self.ready = True  
    
    def view_dfg(self):
        if self.dfg:
            return pm4py.view_dfg(self.dfg, self.im, self.fm)
        else:
            logger.error("DFG not initialized")
            return None
        
    def save(self, data_dir):
        os.makedirs(data_dir, exist_ok=True)
        dfg_file = os.path.join(data_dir, 'dfg.pkl')
        inv_mapping_file = os.path.join(data_dir, 'inv_mapping.pkl')
        
        try:
            if self.ready:
                with open(dfg_file, 'wb') as f:
                    pickle.dump({'dfg':self.dfg, 'im':self.im, 'fm':self.fm}, f)
                with open(inv_mapping_file, 'wb') as f:
                    pickle.dump(self.inv_mapping, f)
                logger.info(f"DFG saved to {dfg_file} and {inv_mapping_file}")
                return True
            else:
                logger.error("DFG not initialized, cannot save")
        except Exception as e:
            logger.error(f"Error saving DFG: {e}")

        return False        
    
    def restore(self, data_dir):
        dfg_file = os.path.join(data_dir, 'dfg.pkl')
        inv_mapping_file = os.path.join(data_dir, 'inv_mapping.pkl')
        
        if not os.path.exists(dfg_file):
            logger.error(f"DFG file {dfg_file} does not exist.")
            return False
        if not os.path.exists(inv_mapping_file):
            logger.error(f"Inverse mapping file {inv_mapping_file} does not exist.")
            return False
        
        try:
            with open(dfg_file, 'rb') as f:
                data = pickle.load(f)
                self.dfg = data['dfg']
                self.im = data['im']
                self.fm = data['fm']
            with open(inv_mapping_file, 'rb') as f:
                self.inv_mapping = pickle.load(f)
            logger.info(f"DFG restored from {dfg_file} and {inv_mapping_file}")
            self.ready = True
            return True
        except Exception as e:
            logger.error(f"Error restoring DFG: {e}")
            return False
        
        

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    
    import pandas as pd
    from .mappings.swlibs import f_swlibs
    from .mappings.pathstrings import f_pathstrings
    paths = [
        ("/proj/nobackup/", "/proj"),
        ("/home/", "/home"),
        ("/dev/shm/", "/dev/shm"),
        ("/sys/", "/sys"),
        ("/proc/", "/proc"),
    ]
    
    from .activity_log import ActivityLog
        
    el = pd.read_pickle("tests/logs/sample_el.pkl")
    # activity_log = ActivityLog(el, 18, f_swlibs)
    activity_log = ActivityLog(el, 4, f_pathstrings,paths=paths)

    dfg = DFG(activity_log.activity_log)
    print(dfg.dfg)

    
    