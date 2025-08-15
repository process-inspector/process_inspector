class EventLog:
    def __init__(self, df, obj_key, case_key, order_key):
        self.df = df

        self.case_key = case_key
        self.order_key = order_key
        self.obj_key = obj_key
               
        # self._sanity_check()
        
        self.n_events = len(self.df)
        self.n_cases = len(self.df[self.case_key].unique())
        
        if self.obj_key in self.df.columns:
            self.n_objs = len(self.df[self.obj_key].unique())
        else:
            self.n_objs = 1
            
        
    def _sanity_check(self):
        pass
            
        
    