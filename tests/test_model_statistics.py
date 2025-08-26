from linnea_inspector.event_data  import prepare
from linnea_inspector.classifiers.f_call import f_call
from process_inspector.dfg.dfg import DFG
from process_inspector.event_log import EventLog
from process_inspector.activity_log import ActivityLog
from process_inspector.model_statistics import ModelStatistics

import sys
import os

def test():
    # Example test (from root directory):
    
    trace_file = "tests/traces/algorithm0.traces"
    event_data, meta_data = prepare(trace_file)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    
    activity_log = ActivityLog(event_log, f_call)   
    ms = ModelStatistics(activity_log.el_f, obj_key='alg', activity_attrs=['flops', 'duration'], connection_attrs=['flops', 'time'])
    # ms = ModelStatistics(activity_log.el_f, obj_key='alg', activity_attrs=['flops', 'duration'])
    
    for activity, df in ms.activity_stats.items():
        print(f"Activity: {activity}")
        print(df)
    
    for activity, df in ms.connection_stats.items():
        print(f"Activity: {activity}")
        print(df)
    print("SUCCESS")
    
if __name__ == "__main__":
    test()