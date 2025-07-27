# Process Inspector
# Contributors:
# - Aravind Sankaran

import time
import pm4py
from .logging_config import logger


class DFG:
    def __init__(self,activity_log):
        start = time.time()
        self.dfg,self.im,self.fm = pm4py.discover_dfg(activity_log)
        end = time.time()
        logger.info(f"[DFG] elapsed: {end - start:.4f} s")    
            
    def view_dfg(self):
        if self.dfg:
            return pm4py.view_dfg(self.dfg, self.im, self.fm)
        else:
            logger.error("DFG not initialized")
            return None

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

    
    