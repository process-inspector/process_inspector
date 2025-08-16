from process_inspector.dfg.dfg import DFG
from process_inspector.model_data_utils import load_model_data
import sys

if __name__ == "__main__":
    # Example test (from root directory):
    
    data_dir = sys.argv[1]
    
    dfg = DFG()
    dfg, activity_events, meta_data = load_model_data(data_dir, dfg)

    print(dfg.nodes)
    print(dfg.edges)
    print(dfg.im)
    print(dfg.fm)
    print(activity_events)
    print(meta_data.case_attr)
    print(meta_data.obj_attr)
    print(dfg.ready)

    