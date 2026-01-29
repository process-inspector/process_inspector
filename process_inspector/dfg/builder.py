import numpy as np
import pandas as pd
from process_inspector.activity_log import ActivityLog

import warnings
warnings.filterwarnings(
    "ignore",
    message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated",
    category=FutureWarning,
)

class DFGBuilder:
    def __init__(self, activity_log: ActivityLog, edge_attrs: list = []):
        
        self.nodes = set()
        self.edges = set()
        
        self.node_data = None # I_v
        self.edge_data = None # I_d
        
        self.edge_attrs = ['el:activity'] + edge_attrs # use egde_attrs only for those columns that are needed for edge stats (like, diff in duration)
        
        assert activity_log.c_event_log is not None, "Activity log cannot be empty for DFG Builder"
        
        self._build_dfg(activity_log.c_event_log)
        
    def _build_dfg(self, c_event_log: pd.DataFrame):
        
        df_node_data = []
        df_edge_data = []   
        columns = c_event_log[list(c_event_log.keys())[0]].columns
        
        for case, df in c_event_log.items():
            df_node_data.append(df.copy())
            
            start = df.iloc[0].copy()
            # start[:] = np.nan # this step results in future warning
            start['el:activity'] = '__START__'
            
            end = df.iloc[-1].copy()
            # end[:] = np.nan # this step results in future warning
            end['el:activity'] = '__END__'
    
            df_ = pd.concat([pd.DataFrame([start]), df, pd.DataFrame([end])], ignore_index=True)

            for col in self.edge_attrs:
                df_["next_" + col] = df_[col].shift(-1)
            df_edge_data.append(df_)
            
        df_node_data = pd.concat(df_node_data, ignore_index=True)
        df_node_data = df_node_data.groupby('el:activity')
        self.node_data = {activity: group for activity, group in df_node_data}
        
        df_edge_data = pd.concat(df_edge_data, ignore_index=True)
        df_edge_data = df_edge_data.groupby(['el:activity', 'next_el:activity'])
        self.edge_data = { f"{activity} -->_dfr {next_activity}": group for (activity, next_activity), group in df_edge_data}
        
        self.nodes = set(self.node_data.keys()) | {'__START__', '__END__'}
        self.edges = set(self.edge_data.keys())
        
        
        
        