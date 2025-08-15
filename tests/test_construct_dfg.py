from linnea_inspector.event_data  import prepare
from linnea_inspector.classifiers.f_call import f_call
from process_inspector.dfg import DFG
from process_inspector.activity_log import ActivityLog

import sys
import os

if __name__ == "__main__":
    # Example test (from root directory):
    
    trace_file = sys.argv[1]
    el, meta_data = prepare(trace_file)
    
    activity_log = ActivityLog(el, 4, f_call)    
    dfg = DFG(activity_log)
    print(dfg.dfg)
    
    
    outdir = os.path.join('tmp')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
        
    dfg.save(outdir)