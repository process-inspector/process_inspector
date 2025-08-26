from linnea_inspector.event_data  import prepare
from linnea_inspector.classifiers.f_call import f_call

from process_inspector.event_log import EventLog
from process_inspector.activity_log import ActivityLog

from process_inspector.dfg.dfg import DFG
from process_inspector.dfg.diff_dfgs import diff_dfgs

import sys
import os

def test():
    # Example test (from root directory):
    
    trace_file1 = "tests/traces/algorithm0.traces"
    trace_file2 = "tests/traces/algorithm45.traces"
    
    event_data, meta_data = prepare(trace_file1)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    activity_log = ActivityLog(event_log, f_call)    
    dfg1 = DFG(activity_log)
    
    event_data, meta_data = prepare(trace_file2)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    activity_log = ActivityLog(event_log, f_call)    
    dfg2 = DFG(activity_log)
    
    diff = diff_dfgs(dfg1, dfg2)
    print(diff)
    print("SUCCESS")
    

if __name__ == "__main__":
    test()
