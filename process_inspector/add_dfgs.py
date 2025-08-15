from .dfg import DFG
from collections import Counter
import pandas as pd

def add_dfgs(*dfgs):
    combined_dfg = Counter()
    combined_im = Counter()
    combined_fm = Counter()
    inv_mapping = {}
    for dfg in dfgs:
        combined_dfg.update(dfg.dfg)
        combined_im.update(dfg.im)
        combined_fm.update(dfg.fm)
        for activity, df in dfg.inv_mapping.items():
            # df['el:id'] = dfg.id  # Ensure each activity has the DFG ID
            if activity not in inv_mapping:
                inv_mapping[activity] = df
            else:
                inv_mapping[activity] = pd.concat([inv_mapping[activity], df], ignore_index=True)
    

    dfg_ = DFG()
    dfg_.dfg = combined_dfg
    dfg_.im = combined_im
    dfg_.fm = combined_fm
    dfg_.inv_mapping = inv_mapping
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