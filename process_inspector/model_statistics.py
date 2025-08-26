import pandas as pd
import numpy as np

class ModelStatistics:
    def __init__(self, el_f, obj_key, activity_attrs, connection_attrs=[]):
        self.activity_stats = None
        self.connection_stats = None
        self.obj_key = obj_key
        self.activity_attrs = activity_attrs
        self.connection_attrs = connection_attrs
        self._prepare_data(el_f)
        
    
    def _prepare_data(self, el_f):
        df_list = []
        for case, df in el_f.items():
            start = df.iloc[0].copy()
            start[:] = np.nan
            df = pd.concat([pd.DataFrame([start]), df], ignore_index=True)
            df["next_activity"] = df['el:activity'].shift(-1)
            for an in self.connection_attrs:
                df["next_" + an] = df[an].shift(-1)
            attrs = list(set([self.obj_key, 'el:activity', 'next_activity'] + self.activity_attrs + self.connection_attrs + ["next_" + an for an in self.connection_attrs]))
            df_list.append(df[attrs])
            
        df_ = pd.concat(df_list, ignore_index=True)
        self.activity_stats = df_.groupby('el:activity')[[self.obj_key,] + self.activity_attrs]
        self.activity_stats = {activity: group for activity, group in self.activity_stats}
        if self.connection_attrs:
            self.connection_stats = df_.groupby(['el:activity', 'next_activity'], dropna=False)[[self.obj_key,] + self.connection_attrs+["next_" + an for an in self.connection_attrs]]
            self.connection_stats = { (activity, next_activity): group for (activity, next_activity), group in self.connection_stats}
        else:
            #for each goup i want a count
            self.connection_stats = df_.groupby(['el:activity', 'next_activity'], dropna=False).size().to_dict()