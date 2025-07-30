from process_inspector.dfg import DFG
import sys

if __name__ == "__main__":
    # Example test (from root directory):
    
    data_dir = sys.argv[1]
    
    dfg = DFG()
    dfg.restore(data_dir)
    print(dfg.dfg)
    print(dfg.im)
    print(dfg.fm)
    print(dfg.inv_mapping)
    print(dfg.ready)
    if dfg.inv_mapping:
        for name, group in dfg.inv_mapping.items():
            print(name)
            print(group)
            break
    