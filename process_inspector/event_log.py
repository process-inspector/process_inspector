class EventLog:
    def __init__(self, event_data, obj_key, case_key, order_key, do_sort=False):
        
        self.case_key = case_key
        self.order_key = order_key
        self.obj_key = obj_key
               
        # self._sanity_check()
        
        self.n_events = len(event_data)
        # self.n_cases = len(event_data[self.case_key].unique())
        self.n_cases = event_data[self.case_key].drop_duplicates().shape[0]
        self.n_objs = len(event_data[self.obj_key].unique())
        
        self.event_log = self.group_and_sort(event_data, do_sort=do_sort)            
    
    def group_and_sort(self, event_data, do_sort=False):
        if do_sort:
            event_data = event_data.sort_values(by=[self.order_key,])
        grouped = event_data.groupby(self.case_key)
        return grouped
        
    def _sanity_check(self):
        pass
            
        
  
