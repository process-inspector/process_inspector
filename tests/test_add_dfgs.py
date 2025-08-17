from linnea_inspector.event_data  import prepare
from linnea_inspector.classifiers.f_call import f_call

from process_inspector.event_log import EventLog
from process_inspector.activity_log import ActivityLog

from process_inspector.dfg.dfg import DFG
from process_inspector.dfg.add_dfgs import add_dfgs
from process_inspector.dfg.perspective import DFGPerspective

import sys
import os

def test():
    # Example test (from root directory):
    
    trace_file1 = "examples/traces/gls/traces/algorithm0.traces"
    trace_file2 = "examples/traces/gls/traces/algorithm5.traces"
    
    event_data, meta_data = prepare(trace_file1)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    activity_log = ActivityLog(event_log, 4, f_call)    
    dfg1 = DFG(activity_log)
    
    event_data, meta_data = prepare(trace_file2)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    activity_log = ActivityLog(event_log, 4, f_call)    
    dfg2 = DFG(activity_log)
    
    dfg = add_dfgs(dfg1, dfg2)
    
    perspective = DFGPerspective(dfg)
    perspective.create_style()
    graph = perspective.prepare_digraph(rankdir='TD')
    print(graph)
    graph.render(os.path.join('tmp', 'dfg_add'), format='svg', cleanup=True)
    print("SUCCESS")

if __name__ == "__main__":
    test()

    