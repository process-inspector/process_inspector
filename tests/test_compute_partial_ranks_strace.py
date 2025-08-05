from process_inspector.dfg import DFG
from process_inspector.add_dfgs import add_dfgs
from process_inspector.compute_ranks import compute_activity_ranks
from pathlib import Path
import sys
import numpy as np

if __name__ == "__main__":
    # Example test (from root directory):
    
    # python -m tests.test_compute_partial_ranks_strace examples/dfgs/rw_ls/ examples/dfgs/rw_ls_l/
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
       df['perf'] = np.where(df['bytes'] == 0, np.nan, df['duration'] * 1e6 / df['bytes'])
    
    activity_ranks = compute_activity_ranks(dfg.inv_mapping ,group_by='id', on='perf')
    for activity, rank in activity_ranks.items():
        print(f'{activity}: {rank['nranks']}')