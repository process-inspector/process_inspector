from linnea_inspector.event_data import prepare
from process_inspector.event_log import EventLog

import sys
import os

if __name__ == "__main__":
    # Example test (from root directory):
    
    trace_file = sys.argv[1]
    event_data, meta_data = prepare(trace_file)
    event_log = EventLog(event_data, case_key='iter', order_key='time', obj_key='alg')
    
    for case, trace in event_log.event_log:
        print(f"Case: {case}")
        print(trace)
        break
    