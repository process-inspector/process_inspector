from linnea_inspector.event_data import prepare
from linnea_inspector.classifiers.f_call import f_call
from process_inspector.event_log import EventLog
from process_inspector.activity_log import ActivityLog

import sys
import os

def test():
    trace_file = "tests/traces/algorithm0.traces"
    event_data, meta_data = prepare(trace_file)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    print(f"Num events: {event_log.n_events}, Num cases: {event_log.n_cases}")
    
    activity_log = ActivityLog(event_log, f_call) 
    

    
    for case, classified_trace in activity_log.el_f.items():
        print(case)
        print(classified_trace)
        break
    
    print(activity_log.activity_language)
    print(activity_log.vocabulary)
    
    # activity_events = activity_log.activity_events
    # for activity, df in activity_events.items():
    #     print(f"Activity: {activity}, DataFrame:\n {df}")
    #     break
    
    # # print(activity_events.get_group('potrf'))  
    
        
    print(f"Num activities / Vocabulary: {len(activity_log.vocabulary)}, Num variants: {activity_log.n_variants}")
    print("SUCCESS") 

if __name__ == "__main__":
    test()
        
    