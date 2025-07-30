from process_inspector.dfg import DFG
from process_inspector.statistics_coloring import StatisticsColoring
import sys
import os

if __name__ == "__main__":
    # Example test (from root directory):
    
    data_dir = sys.argv[1]
    
    dfg = DFG()
    dfg.restore(data_dir)
    
    perspective = StatisticsColoring(dfg)
    perspective.create_style()
    graph = perspective.prepare_digraph(rankdir='TD')
    print(graph)
    graph.render(os.path.join(data_dir, 'dfg'), format='svg', cleanup=True)
    
    
    
    