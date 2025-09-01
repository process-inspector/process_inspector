from linnea_inspector.event_data  import prepare
from linnea_inspector.classifiers.f_call import f_call
from process_inspector.dfg.dfg import DFG
from process_inspector.event_log import EventLog
from process_inspector.activity_log import ActivityLog
from process_inspector.dfg.reverse_maps import DFGReverseMaps

import sys
import os

def test():
    # Example test (from root directory):
    
    trace_file = "tests/traces/algorithm0.traces"
    event_data, meta_data = prepare(trace_file)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    
    activity_log = ActivityLog(event_log, f_call)
    reverse_map = DFGReverseMaps(activity_log)
    
    for node, df in reverse_map.activities_map.items():
        print(f"Node: {node}, DataFrame:\n {df}")
        break
 
    print(reverse_map.edges_map[('trsv', '__END__')])
    print(reverse_map.edges_map[('trsv', 'trsm')])
    print(reverse_map.edges_map[('__START__', 'potrf')])
    
    print(reverse_map.edges_map.keys())
    print("SUCCESS")
    

    
    
if __name__ == "__main__":
    test()