
import time
import numpy as np
import multiprocessing as mp
import pandas as pd
import pm4py
from functools import partial
from .logging_config import logger

class ActivityLog:
    def __init__(self, event_log, n_cpu, mapping_fn, **kwargs):
        self.n_cpu = n_cpu
        self.mapping_fn = mapping_fn
        self.inv_mapping = None
        self.activity_log = None
        self.num_events = 0
        self.num_cases = 0
        self.num_activities = 0
        self._prepare(event_log, **kwargs)
        
        #self.num_cases = self.activity_log.shape[0]
        self.num_cases = len(self.activity_log)
        self.num_activities = len(self.inv_mapping)

    
 
    def _prepare(self, el, **kwargs):
        
        start = time.time()
        
        chunks = np.array_split(el, self.n_cpu)  
        with mp.Pool(processes=self.n_cpu) as pool:
            func = partial(self._apply_mapping, **kwargs)
            results = pool.map(func, chunks)    
        df = pd.concat(results, ignore_index=True)
        self.num_events = df.shape[0]
        self.inv_mapping = df.groupby('activity')
        
        #self.activity_log = df[['case','activity']].groupby('case').agg(list)
        try:
            df['time'] = pd.to_datetime(df['time'].astype(float), unit='s')
        except ValueError:
            logger.warning("[ACTIVITY_LOG] 'time' does not include date.")
            pass
        df_ = pm4py.format_dataframe(df[['case', 'activity', 'time']].copy(),case_id='case',activity_key='activity',timestamp_key='time')        
        self.activity_log = pm4py.convert_to_event_log(df_)
        del df_
        self.num_cases = len(self.activity_log)
        self.num_activities = len(self.inv_mapping)
        end = time.time()
        logger.info(f"[ACTIVITY_LOG] mapping_fn: {self.mapping_fn.__qualname__} | elapsed: {end - start:.4f} seconds | nevents: {self.num_events} | ncases: {self.num_cases} | nactivities: {self.num_activities}")
        
        

    def _apply_mapping(self,chunk, **kwargs):
        chunk['activity'] = chunk.apply(lambda x: self.mapping_fn(x,**kwargs), axis=1)
        return chunk[chunk['activity'].notna()]
    
    def _prepare_serial(self,el, **kwargs):
        el['activity'] = el.apply(lambda x: self.mapping_fn(x,**kwargs), axis=1)
        df = el[el['activity'].notna()]
        self.num_events = df.shape[0]
        self.inv_mapping = df.groupby('activity')
        #self.activity_log = df[['case','activity']].groupby('case').agg(list)
        df_ = pm4py.format_dataframe(df[['case', 'activity', 'time']].copy(),case_id='case',activity_key='activity',timestamp_key='time')
        self.activity_log = pm4py.convert_to_event_log(df_)
        del df_


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_parser = logging.getLogger('st')
    logger_parser.setLevel(logging.DEBUG)
    
    import pandas as pd
    from .mappings.swlibs import f_swlibs
    
    from .mappings.pathstrings import f_pathstrings
    paths = [
        # ("/proj/nobackup/", "/proj"),
        ("/home/", "/home"),
        ("/dev/shm/", "/dev/shm"),
        ("/sys/", "/sys"),
        ("/proc/", "/proc"),
    ]
        
    el = pd.read_pickle("tests/logs/sample_el.pkl")
    # activity_log = ActivityLog(el, 18, f_swlibs)
    activity_log = ActivityLog(el, 4, f_pathstrings,paths=paths)
    #print(activity_log.el)
    inv_map = activity_log.inv_mapping
    # print(inv_map.get_group('read+libzstd.so.1.4.4'))
    print(inv_map.get_group(next(iter(inv_map.groups))))
    
        
    al = activity_log.activity_log
    for case in al:
        print(case)
        break
    
    print(f"Number of cases: {activity_log.num_cases}")
    print(f"Number of activities: {activity_log.num_activities}")
    for i, (activity,df) in enumerate(inv_map):
        print(f" {i+1}) {activity} count: {len(df)}")
    #print(al.iloc[0,0])
    
    #print(el)
