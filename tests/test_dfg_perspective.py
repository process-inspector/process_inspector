from linnea_inspector.event_data  import prepare
from linnea_inspector.classifiers.f_call import f_call
from process_inspector.dfg.dfg import DFG
from process_inspector.event_log import EventLog
from process_inspector.activity_log import ActivityLog
from process_inspector.dfg.perspective import DFGPerspective
import sys
import os

if __name__ == "__main__":
    # Example test (from root directory):
    
    trace_file = sys.argv[1]
    event_data, meta_data = prepare(trace_file)
    event_log = EventLog(event_data, case_key=['alg','iter'], order_key='time', obj_key='alg')
    
    activity_log = ActivityLog(event_log, 4, f_call)    
    dfg = DFG(activity_log)
    
    
    perspective = DFGPerspective(dfg)
    perspective.create_style()
    graph = perspective.prepare_digraph(rankdir='TD')
    print(graph)
    graph.render(os.path.join('tmp', 'dfg'), format='svg', cleanup=True)
    
    
    
    