import pandas as pd
from .perspective import Perspective

class BasicPerspective(Perspective):
    def __init__(self, dfg):
        super().__init__(dfg)
        
            
    def create_style(self):
        
        for activity in self.dfg.inv_mapping.keys():
            self.node_label[activity] = activity
        
        for node in self.node_label:
            self.node_color[node] = "#FFFFFF"
            
        for edge, label in self.dfg.dfg.items():
            self.edge_color[edge] = "#000000"
            self.edge_penwidth[edge] = 1.0
            self.edge_label[edge] = str(label)
            
        for im, label in self.dfg.im.items():
            self.edge_color[im] = "#000000"
            self.edge_penwidth[im] = 1.0
            self.edge_label[im] = str(label)
            
        for fm, label in self.dfg.fm.items():
            self.edge_color[fm] = "#000000"
            self.edge_penwidth[fm] = 1.0
            self.edge_label[fm] = str(label)
        

