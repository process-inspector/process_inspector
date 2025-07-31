import sys
from process_inspector.dfg import DFG
from process_inspector.add_dfgs import add_dfgs
from process_inspector.statistics_coloring import StatisticsColoring
import os
from pathlib import Path

if __name__ == "__main__":
    
    dfgs = []
    for i in range(1, len(sys.argv)):
        data_dir = sys.argv[i]
        
        dfg = DFG()
        dfg.restore(data_dir)
        dfg.id = Path(data_dir).name  # Use directory name as ID
        
        dfgs.append(dfg)
        
    print(dfgs)
    dfg_combined = add_dfgs(*dfgs)
    print(dfg_combined.dfg)
    print(dfg_combined.im)
    print(dfg_combined.fm)
    for activity, df in dfg_combined.inv_mapping.items():
        print(f"Activity: {activity}")
        print(df)
        break
    
    outdir = os.path.join('tmp')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    dfg_combined.save(outdir)
            
    perspective = StatisticsColoring(dfg_combined)
    perspective.create_style()
    graph = perspective.prepare_digraph(rankdir='TD')
    print(graph)
    graph.render(os.path.join(outdir, 'dfg'), format='svg', cleanup=True)