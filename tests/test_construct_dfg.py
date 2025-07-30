from scorep_inspector.event_log.prepare_event_log import prepare_event_log
from scorep_inspector.mappings.send_recv import f_send_recv_b
from process_inspector.dfg import DFG
from process_inspector.activity_log import ActivityLog

import sys

if __name__ == "__main__":
    # Example test (from root directory):
    
    otf2_file = sys.argv[1]
    df, unresolved = prepare_event_log(otf2_file)
    print(df)
    
    activity_log = ActivityLog(df, 4, f_send_recv_b)    
    dfg = DFG(activity_log)
    print(dfg.dfg)
    
    inv_map = dfg.inv_mapping
    print(inv_map.get_group(next(iter(inv_map.groups))))
    
    dfg.save('tmp/')