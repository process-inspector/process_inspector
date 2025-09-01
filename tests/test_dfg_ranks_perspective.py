from linnea_inspector.event_data  import prepare
from linnea_inspector.classifiers.f_call import f_call

from process_inspector.event_log import EventLog
from process_inspector.activity_log import ActivityLog

from process_inspector.dfg.dfg import DFG
from process_inspector.dfg.ranks_perspective import DFGRanksPerspective
from process_inspector.dfg.reverse_maps import DFGReverseMaps
from process_inspector.model_data_utils import concat_meta_data

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
    
    dfg = DFG(activity_log)
    reverse_maps = DFGReverseMaps(activity_log)
    
    perspective = DFGRanksPerspective(dfg, reverse_maps, meta_data, obj_key='alg', obj_perf_key='duration')
    perspective.create_style()
    graph = perspective.prepare_digraph(rankdir='TD')
    print(graph)
    graph.render(os.path.join('tests/output', 'dfg_ranks'), format='svg', cleanup=True)
    print("SUCCESS")
    

if __name__ == "__main__":
    test()