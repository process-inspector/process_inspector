class EventLog:
    def __init__(self, events_df, obj_key, case_key, order_key):
        self.events = events_df

        self.case_key = case_key
        self.order_key = order_key
        self.obj_key = obj_key
               
        # self._sanity_check()
        
        self.n_events = len(self.events)
        self.n_cases = len(self.events[self.case_key].unique())
        self.n_objs = len(self.events[self.obj_key].unique())
                    
        
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
            pass
        return value
    
    def get_obj_attr(self, obj, attr):
        value = None
        try:
            value = self.obj_attr[obj][attr]
        except KeyError as e:
            pass
        return value