from process_inspector.activity_log import ActivityLog
import sys
import os
from process_inspector.model_data_utils import load_model_data

def test():
    
    datadir = "tests/output"
    activity_log, meta_data = load_model_data(datadir)
        
    print(activity_log.activities)
    for case, classified_trace in activity_log.c_event_log.items():
        print(case)
        print(classified_trace)
        break
    print(activity_log.activity_language)
    
    print(meta_data.get_case_data())
    
    print("SUCCESS")
    
if __name__ == "__main__":
    test()