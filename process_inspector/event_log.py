class EventLog:
    def __init__(self, event_data, obj_key, case_key, order_key, do_sort=True, inplace=False):
        
        self.case_key = case_key
        self.order_key = order_key
        self.obj_key = obj_key
        self.event_traces = {}
               
        # self._sanity_check()
        
        self.n_events = len(event_data)
        # self.n_cases = len(event_data[self.case_key].unique())
        self.n_cases = event_data[self.case_key].drop_duplicates().shape[0]
        self.n_objs = len(event_data[self.obj_key].unique())
        
        self._prepare_event_traces_serial(event_data, do_sort=do_sort)
        
        if inplace:
            event_data = None
                 
    
    def _prepare_event_traces_serial(self, event_data, do_sort=True):
        self.event_traces = {}
        grouped = event_data.groupby(self.case_key)
        # can be parallelized
        for case, trace in grouped:
            if do_sort:
                trace = trace.sort_values(by=[self.order_key,])
            self.event_traces[case] = trace        
        
        
        
    def _sanity_check(self):
        pass
            
        
  
