from linnea_inspector.event_data  import prepare
from linnea_inspector.classifiers.f_call import f_call

from process_inspector.event_log import EventLog
from process_inspector.activity_log import ActivityLog

from process_inspector.dfg.dfg import DFG
from process_inspector.dfg.diff_dfgs import diff_dfgs

import sys
import os

if __name__ == "__main__":
    # Example test (from root directory):
    
    trace_file1 = sys.argv[1]
    trace_file2 = sys.argv[2]
    
    event_data, meta_data = prepare(trace_file1)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    activity_log = ActivityLog(event_log, 4, f_call)    
    dfg1 = DFG(activity_log)
    
    event_data, meta_data = prepare(trace_file2)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    activity_log = ActivityLog(event_log, 4, f_call)    
    dfg2 = DFG(activity_log)
    
    diff = diff_dfgs(dfg1, dfg2)
    print(diff)