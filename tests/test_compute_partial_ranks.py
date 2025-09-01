from linnea_inspector.event_data  import prepare
from linnea_inspector.classifiers.f_call import f_call

from process_inspector.event_log import EventLog
from process_inspector.activity_log import ActivityLog
from process_inspector.dfg.reverse_maps import DFGReverseMaps

from process_inspector.model_data_utils import concat_meta_data
from process_inspector.compute_ranks import compute_activity_ranks, compute_meta_data_ranks

import sys
import os

def test():
    # Example test (from root directory):
    
    trace_file1 = "tests/traces/algorithm0.traces"
    trace_file2 = "tests/traces/algorithm45.traces"
    
    event_data, meta_data1 = prepare(trace_file1)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    activity_log1 = ActivityLog(event_log, f_call)    
    
    event_data, meta_data2 = prepare(trace_file2)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    activity_log2 = ActivityLog(event_log, f_call)    
    
    activity_log = activity_log1 + activity_log2
    meta_data = concat_meta_data(meta_data1, meta_data2)
    reverse_maps = DFGReverseMaps(activity_log)
    
    for activity, events in reverse_maps.activities_map.items():
        events['perf'] = events['flops'] / events['duration']
    
    for activity, events in reverse_maps.activities_map.items():
        print(f"Activity: {activity}")
        print(events)
        break
                
    activity_ranks = compute_activity_ranks(reverse_maps.activities_map ,group_by='alg', on='perf')
    
    for activity, ranks in activity_ranks.items():
        print(f"Activity: {activity}")
        print(f"nranks: {ranks['nranks']}")
        print(f"M1: {ranks['m1']}")
        print(f"M2: {ranks['m2']}")
        print(f"M3: {ranks['m3']}")
    
    print(meta_data.get_obj_data())
    print(meta_data.get_case_data())
    
    alg_ranks = compute_meta_data_ranks(meta_data.get_case_data(), group_by='alg', on='perf')
    
    print(alg_ranks['measurements'])
    print(f"nranks: {alg_ranks['nranks']}")
    print(f"M1: {alg_ranks['m1']}")
    print(f"M2: {alg_ranks['m2']}")
    print(f"M3: {alg_ranks['m3']}")
    
    print("SUCCESS")
    

if __name__ == "__main__":
    test()
    
    