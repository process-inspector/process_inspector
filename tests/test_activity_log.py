from linnea_inspector.event_data import prepare
from linnea_inspector.classifiers.f_call import f_call
from process_inspector.event_log import EventLog
from process_inspector.activity_log import ActivityLog
from process_inspector.model_data_utils import save_model_data

import sys
import os


def test2():
    trace_file1 = "tests/traces/algorithm0.traces"
    trace_file2 = "tests/traces/algorithm45.traces"
    
    event_data, meta_data = prepare(trace_file1)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    activity_log1 = ActivityLog(event_log, f_call)    
    
    event_data, meta_data = prepare(trace_file2)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    activity_log2 = ActivityLog(event_log, f_call)
    
    activity_log = activity_log1 + activity_log2    
    
    for case, classified_trace in activity_log.c_event_log.items():
        print(case)
        print(classified_trace)
        break
    
    print(activity_log.activity_language)
    print(activity_log.activities)
    print(activity_log.c_event_log.keys())
    print("SUCCESS")
    

def test1():
    trace_file = "tests/traces/algorithm0.traces"
    event_data, meta_data = prepare(trace_file)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    print(f"Num events: {event_log.n_events}, Num cases: {event_log.n_cases}")
    
    activity_log = ActivityLog(event_log, f_call) 
    

    
    for case, classified_trace in activity_log.c_event_log.items():
        print(case)
        print(classified_trace)
        break
    
    print(activity_log.activity_language)
    print(activity_log.activities)
    
    # activity_events = activity_log.activity_events
    # for activity, df in activity_events.items():
    #     print(f"Activity: {activity}, DataFrame:\n {df}")
    #     break
    
    # # print(activity_events.get_group('potrf'))  
    
    outdir = os.path.join('tests/output')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
        
    save_model_data(outdir, activity_log, meta_data)
    
        
    print(f"Num activities / Activities set: {len(activity_log.activities)}, Num variants: {activity_log.n_variants}")
    print("SUCCESS") 

if __name__ == "__main__":
    test1()
    test2()
        
    