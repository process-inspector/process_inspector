from linnea_inspector.event_data  import prepare
from linnea_inspector.classifiers.f_call import f_call

from process_inspector.event_log import EventLog
from process_inspector.activity_log import ActivityLog

from process_inspector.dfg.dfg import DFG
from process_inspector.dfg.statistics_perspective import DFGStatisticsPerspective
from process_inspector.dfg.reverse_maps import DFGReverseMaps

import sys
import os

def test():
    # Example test (from root directory):
    
    trace_file1 = "tests/traces/algorithm0.traces"
    trace_file2 = "tests/traces/algorithm45.traces"
    
    event_data, meta_data = prepare(trace_file1)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    activity_log1 = ActivityLog(event_log, f_call)    
    
    event_data, meta_data = prepare(trace_file2)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    activity_log2 = ActivityLog(event_log, f_call)    
    
    activity_log = activity_log1 + activity_log2
    dfg = DFG(activity_log)
    reverse_maps = DFGReverseMaps(activity_log)
    
    
    
    perspective = DFGStatisticsPerspective(dfg, reverse_maps)
    perspective.create_style()
    graph = perspective.prepare_digraph(rankdir='TD')
    print(graph)
    graph.render(os.path.join('tests/output', 'dfg_stats'), format='svg', cleanup=True)
    print("SUCCESS")

if __name__ == "__main__":
    test()

    