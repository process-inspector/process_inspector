from linnea_inspector.event_data import prepare
from linnea_inspector.classifiers.f_call import f_call
from process_inspector.dfg import DFG
from process_inspector.activity_log import ActivityLog

import sys
import os

if __name__ == "__main__":
    # Example test (from root directory):
    
    trace_file = sys.argv[1]
    el, meta_data = prepare(trace_file)
    print(el.events)
    print(f"Num events: {el.n_events}, Num cases: {el.n_cases}")
    
    activity_log = ActivityLog(el, 4, f_call)   
    

    
    inv_map = activity_log.inv_mapping
    for activity, df in inv_map.items():
        print(f"Activity: {activity}, DataFrame:\n {df}")
        break
        
    print(f"Num activities: {activity_log.n_activities}, Num variants: {activity_log.n_variants}") 
        
    