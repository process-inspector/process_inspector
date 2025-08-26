from .dfg import DFG
import pandas as pd

def add_dfgs(*dfgs):
    combined_nodes = set()
    combined_edges = set()
    combined_im = set()
    combined_fm = set()
    #complexity: O(len(dfgs)*max_num_edges)
    for dfg in dfgs:
        combined_nodes.update(dfg.nodes)
        combined_edges.update(dfg.edges)
        combined_im.update(dfg.im)
        combined_fm.update(dfg.fm)
    
    dfg_ = DFG()
    dfg_.nodes = combined_nodes
    dfg_.edges = combined_edges
    dfg_.im = combined_im
    dfg_.fm = combined_fm
    dfg_.ready = True    
    
    return dfg_
        
 
            
            
if __name__ == "__main__": 
    # dfg1 = Counter({('A', 'B'): 3, ('B', 'C'): 2})
    # dfg2 = Counter({('A', 'B'): 1, ('C', 'D'): 4})
    # dfg3 = Counter({('B', 'C'): 5})
    
    # combined_dfg = add_dfgs(dfg1, dfg2, dfg3)
    # print(combined_dfg)

    dfg1_dir = "examples/data/hpcg/scorep-2N/"
    dfg1 = DFG()
    dfg1.restore(dfg1_dir)
    dfg1.id = '2N'
    
    dfg2_dir = "examples/data/hpcg/scorep-1N/"
    dfg2 = DFG()
    dfg2.restore(dfg2_dir)
    dfg2.id = '1N'
    
    dfg_combined = add_dfgs(dfg1, dfg2)
    print(dfg_combined.dfg)
    print(dfg_combined.im)
    print(dfg_combined.fm)
    for activity, df in dfg_combined.inv_mapping:
        print(f"Activity: {activity}")
        print(df)