from process_inspector.dfg import DFG
from process_inspector.difference_coloring import DifferenceColoring
import sys
import os
from pathlib import Path

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
    
    perspective = DifferenceColoring(dfg1, dfg2)
    perspective.create_style()
    graph = perspective.prepare_digraph(rankdir='TD')
    print(graph)
    
    outdir = os.path.join('tmp')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    graph.render(os.path.join(outdir, 'dfg_diff'), format='svg', cleanup=True)
    
    
    
    