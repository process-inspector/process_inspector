from linnea_inspector.event_data  import prepare
from linnea_inspector.classifiers.f_call import f_call
from process_inspector.dfg.dfg import DFG
from process_inspector.event_log import EventLog
from process_inspector.activity_log import ActivityLog
from process_inspector.model_data_utils import save_model_data

import sys
import os

def test():
    # Example test (from root directory):
    
    trace_file = "examples/traces/gls/traces/algorithm0.traces"
    event_data, meta_data = prepare(trace_file)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    
    activity_log = ActivityLog(event_log, 4, f_call)    
    dfg = DFG(activity_log)
    print(dfg.im)
    print(dfg.fm)
    print(dfg.edges)
    
    
    outdir = os.path.join('tmp')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
        
    save_model_data(outdir, dfg, activity_log.activity_events, meta_data)
    print("SUCCESS")
    

if __name__ == "__main__":
    test()