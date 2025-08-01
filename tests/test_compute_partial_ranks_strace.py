from process_inspector.dfg import DFG
from process_inspector.add_dfgs import add_dfgs
from process_inspector.compute_partial_ranks import compute_partial_ranks
from pathlib import Path
import sys
import numpy as np

if __name__ == "__main__":
    # Example test (from root directory):
    
    data_dir1 = sys.argv[1]
    data_dir2 = sys.argv[2]
    
    dfg1 = DFG()
    dfg1.restore(data_dir1)
    dfg1.id = Path(data_dir1).name  # Use directory name as ID
    
    dfg2 = DFG()
    dfg2.restore(data_dir2)
    dfg2.id = Path(data_dir2).name  # Use directory name as ID
    
    dfg = add_dfgs(dfg1, dfg2)
    
    # perf indicator
    for activity, df in dfg.inv_mapping.items():
       df['perf'] = np.where(df['bytes'] == 0, None, df['duration'] * 1e6 / df['bytes'])
    
    ranks = compute_partial_ranks(dfg,group_by='id', on='perf')
    for activity, rank in ranks.items():
        print(f'{activity}: {rank['rank_str']}')