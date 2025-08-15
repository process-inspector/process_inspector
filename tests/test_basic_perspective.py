from process_inspector.dfg import DFG
from process_inspector.basic_perspective import BasicPerspective
import sys
import os

if __name__ == "__main__":
    # Example test (from root directory):
    
    data_dir = sys.argv[1]
    
    dfg = DFG()
    dfg.restore(data_dir)
    
    perspective = BasicPerspective(dfg)
    perspective.create_style()
    graph = perspective.prepare_digraph(rankdir='TD')
    print(graph)
    graph.render(os.path.join(data_dir, 'dfg'), format='svg', cleanup=True)
    
    
    
    