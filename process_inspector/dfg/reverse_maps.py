import numpy as np
import pandas as pd

class DFGReverseMaps:
    def __init__(self, activity_log, next_attrs = []):
        self.activities_map = None # I_v
        self.edges_map = None # I_d
        
        self.case_key = activity_log.case_key
        self.order_key = activity_log.order_key
        self.obj_key = activity_log.obj_key
        
        # check if next_atts is a list
        if not isinstance(next_attrs, list):
            raise ValueError("next_attrs should be a list of attribute names.")
        self.next_attrs = self.case_key + [self.obj_key] + ['el:activity',] + next_attrs
        
        self._prepare_data(activity_log.c_event_log)
        
        
        
    def _prepare_data(self, c_event_log):
        
        df_activities_map = []
        df_edge_map = []   
        columns = c_event_log[list(c_event_log.keys())[0]].columns
        
        for case, df in c_event_log.items():
            df_activities_map.append(df.copy())
            
            start = df.iloc[0].copy()
            start[:] = np.nan
            start['el:activity'] = '__START__'
            
            end = df.iloc[-1].copy()
            end[:] = np.nan
            end['el:activity'] = '__END__'
            
            df_ = pd.concat([pd.DataFrame([start]), df, pd.DataFrame([end])], ignore_index=True)

            for col in self.next_attrs:
                df_["next_" + col] = df_[col].shift(-1)
            df_edge_map.append(df_)
            
        df_activities_map = pd.concat(df_activities_map, ignore_index=True)
        df_activities_map = df_activities_map.groupby('el:activity')
        self.activities_map = {activity: group for activity, group in df_activities_map}
        
        df_edge_map = pd.concat(df_edge_map, ignore_index=True)
        df_edge_map = df_edge_map.groupby(['el:activity', 'next_el:activity'])
        self.edges_map = { (activity, next_activity): group for (activity, next_activity), group in df_edge_map}
        
            