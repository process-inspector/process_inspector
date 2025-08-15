class EventLog:
    def __init__(self, events_df, obj_key, case_key, order_key):
        self.df = events_df

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
            
        
  
class MetaData:
    def __init__(self):
        self.case_attr = {}
        self.obj_attr = {}
        self.info = {}
        
    def add_case_attr(self, case, attr, value):
        if case not in self.case_attr:
            self.case_attr[case] = {}
        self.case_attr[case][attr] = value
        
        
    def add_obj_attr(self, obj, attr,value):
        if obj not in self.obj_attr:
            self.obj_attr[obj] = {}
        self.obj_attr[obj][attr] = value
        
    def get_case_attr(self, case, attr):
        value = None
        try:
           value = self.case_attr[case][attr]
        except KeyError as e:
            raise KeyError(f"Error: {e} for case {case} and attribute {attr}") 
        return value
    
    def get_obj_attr(self, obj, attr):
        value = None
        try:
            value = self.obj_attr[obj][attr]
        except KeyError as e:
            raise KeyError(f"Error: {e} for object {obj} and attribute {attr}") 
        return value