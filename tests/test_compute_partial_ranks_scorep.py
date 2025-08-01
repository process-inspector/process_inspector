from process_inspector.dfg import DFG
from process_inspector.add_dfgs import add_dfgs
from process_inspector.compute_partial_ranks import compute_partial_ranks
from pathlib import Path
import sys
import numpy as np
from partial_ranker import MeasurementsVisualizer
# from process_inspector.measurements_visualizer import MeasurementsVisualizer

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
    
    for activity, df in dfg.inv_mapping.items():
        df['perf'] = np.where(df['duration'] == 0, None, (df['msg_size']/ df['duration'])*1000)
    
    
    ranks = compute_partial_ranks(dfg,group_by='id', on='perf')
    for activity, rank in ranks.items():
        print(f'{activity}: {rank['rank_str']}')
        # print(rank['m1'])
    
    print("\nDetails of activity 'MPI_Send/MPI_Irecv (2048B)':")    
    for variant, vals in ranks['MPI_Send/MPI_Irecv (2048B)']['measurements'].items():
        print(f"Variant: {variant}, Mean: {np.mean(vals)} len: {len(vals)}")
    mv = MeasurementsVisualizer(ranks['MPI_Send/MPI_Irecv (2048B)']['measurements'])
    fig = mv.show_measurements_boxplots()
    fig.tight_layout()
    fig.savefig('tmp/boxplots.svg',format="svg", bbox_inches='tight')