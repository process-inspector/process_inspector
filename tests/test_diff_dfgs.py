import sys
from process_inspector.dfg import DFG
from process_inspector.diff_dfgs import diff_dfgs
from pathlib import Path

if __name__ == "__main__":
    
    data_dir1 = sys.argv[1]
    data_dir2 = sys.argv[2]
    
    dfg1 = DFG()
    dfg1.restore(data_dir1)
    dfg1.id = Path(data_dir1).name  # Use directory name as ID
    
    dfg2 = DFG()
    dfg2.restore(data_dir2)
    dfg2.id = Path(data_dir2).name  # Use directory name as ID
    
    diff = diff_dfgs(dfg1, dfg2)
    print(diff)