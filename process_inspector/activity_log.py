import time
import numpy as np
import multiprocessing as mp
import pandas as pd
import pm4py
from functools import partial
from .logging_config import logger

class ActivityLog:
    def __init__(self, event_log, n_cpu, classifier_fn, **kwargs):
        self.n_cpu = n_cpu
        self.classifier_fn = classifier_fn
        self.inv_mapping = None
        self.activity_log = None
        
        self.n_variants = 0
        self.n_activities = 0
        self._prepare(event_log, **kwargs)

    
 
    def _prepare(self, el, **kwargs):
        
        start = time.time()
        
        chunks = np.array_split(el.df, self.n_cpu)  
        with mp.Pool(processes=self.n_cpu) as pool:
            func = partial(self._apply_classifier, **kwargs)
            results = pool.map(func, chunks)    
        df = pd.concat(results, ignore_index=True)
        self.inv_mapping = df.groupby('el:activity')
        self.inv_mapping = {activity: df for activity, df in self.inv_mapping}  # Convert to dict for easier access
        

        df_ = pm4py.format_dataframe(df[[el.case_key, 'el:activity', el.order_key]].copy(),case_id=el.case_key ,activity_key='el:activity',timestamp_key=el.order_key)        
        self.activity_log = pm4py.convert_to_event_log(df_)
        del df_
        self.n_variants = len(pm4py.statistics.variants.log.get.get_variants(self.activity_log))
        self.n_activities = len(self.inv_mapping)
        end = time.time()
        logger.info(f"[ACTIVITY_LOG] classifier_fn: {self.classifier_fn.__qualname__} | elapsed: {end - start:.4f} seconds | nevents: {el.n_events} | ncases: {el.n_cases} | nactivities: {self.n_activities}")
        
        

    def _apply_classifier(self,chunk, **kwargs):
        chunk['el:activity'] = chunk.apply(lambda x: self.classifier_fn(x,**kwargs), axis=1)
        return chunk[chunk['el:activity'].notna()]
    
    
    
    
    

    #self.activity_log = df[['case','activity']].groupby('case').agg(list)
    # try:
    #     df['time'] = pd.to_datetime(df['time'].astype(float), unit='s')
    # except ValueError:
    #     logger.warning("[ACTIVITY_LOG] 'time' does not include date.")
    #     pass
    
    # def _prepare_serial(self,el, **kwargs):
    #     el['activity'] = el.apply(lambda x: self.mapping_fn(x,**kwargs), axis=1)
    #     df = el[el['activity'].notna()]
    #     self.num_events = df.shape[0]
    #     self.inv_mapping = df.groupby('activity')
    #     self.inv_mapping = {activity: df for activity, df in self.inv_mapping}
    #     #self.activity_log = df[['case','activity']].groupby('case').agg(list)
    #     df_ = pm4py.format_dataframe(df[['case', 'activity', 'time']].copy(),case_id='case',activity_key='activity',timestamp_key='time')
    #     self.activity_log = pm4py.convert_to_event_log(df_)
    #     del df_



