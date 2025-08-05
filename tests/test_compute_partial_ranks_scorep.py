from process_inspector.dfg import DFG
from process_inspector.add_dfgs import add_dfgs
from process_inspector.compute_ranks import compute_activity_ranks
from pathlib import Path
import sys
import numpy as np
from partial_ranker import MeasurementsVisualizer
# from process_inspector.measurements_visualizer import MeasurementsVisualizer

if __name__ == "__main__":
    # Example test (from root directory):
    #  python -m tests.test_compute_partial_ranks_scorep examples/dfgs/hpcg_1N/ examples/dfgs/hpcg_2N/
    data_dir1 = sys.argv[1]
    data_dir2 = sys.argv[2]
    
    dfg1 = DFG()
    dfg1.restore(data_dir1)
    dfg1.id = Path(data_dir1).name  # Use directory name as ID
    
    dfg2 = DFG()
    dfg2.restore(data_dir2)
    dfg2.id = Path(data_dir2).name  # Use directory name as ID
    
    dfg = add_dfgs(dfg1, dfg2)
    
    for activity, df in dfg.inv_mapping.items():
        df['perf'] = np.where(df['duration'] == 0, np.nan, (df['msg_size']/ df['duration'])*1000)
    
    
    activity_ranks = compute_activity_ranks(dfg.inv_mapping, group_by='id', on='perf')
    for activity, rank in activity_ranks.items():
        print(f'{activity}: {rank['nranks']}')
        # print(rank['m1'])
    
    print("\nDetails of activity 'MPI_Send/MPI_Irecv (2048B)':")    
    for variant, vals in activity_ranks['MPI_Send/MPI_Irecv (2048B)']['measurements'].items():
        print(f"Variant: {variant}, Mean: {np.mean(vals)} len: {len(vals)}")
    mv = MeasurementsVisualizer(activity_ranks['MPI_Send/MPI_Irecv (2048B)']['measurements'])
    fig = mv.show_measurements_boxplots()
    fig.tight_layout()
    fig.savefig('tmp/boxplots.svg',format="svg", bbox_inches='tight')