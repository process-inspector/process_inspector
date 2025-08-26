from process_inspector.dfg.dfg import DFG
from process_inspector.model_data_utils import load_model_data
import sys

def test():
    # Example test (from root directory):
    
    data_dir = "tests/output"
    
    dfg = DFG()
    dfg, classified_event_traces, meta_data = load_model_data(data_dir, dfg)

    print(dfg.nodes)
    print(dfg.edges)
    print(dfg.im)
    print(dfg.fm)
    print(classified_event_traces)
    print(meta_data.get_case_data())
    print(meta_data.get_obj_data())
    print(dfg.ready)
    print("SUCCESS")

if __name__ == "__main__":
    test()


    