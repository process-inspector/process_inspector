import pandas as pd
from .add_dfgs import add_dfgs
from .diff_dfgs import diff_dfgs
from .dfg import DFG
from .base_perspective import DFGBasePerspective

class DFGDifferencePerspective(DFGBasePerspective):
    def __init__(self, dfg1, dfg2,dfg_combined=None):
        
        if dfg_combined is None:
            dfg_combined = dfg1 + dfg2
        super().__init__(dfg_combined)
        
        self.diff = dfg1.diff(dfg2)
        
        self.default_activity_color = "#FFFFFF"
        self.default_edge_color = "#000000"
        
        self.node_red_hex = "#EF9A9A"
        self.node_green_hex = "#8BC34A"
        
        self.edge_red_hex = "#E53935"
        self.edge_green_hex = "#2E7D32"
        
        for activity in self.dfg.nodes:
            self.activity_label[activity] = activity
        
        
        
    def create_style(self):
        
        for node in self.dfg.nodes:
            self.activity_color[node] = self.default_activity_color
            if node in self.diff.unique_nodes1:
                self.activity_color[node] = self.node_green_hex
            elif node in self.diff.unique_nodes2:
                self.activity_color[node] = self.node_red_hex
                
        for edge in self.dfg.edges:
            self.edge_color[edge] = self.default_edge_color
            if edge in self.diff.unique_edges1:
                self.edge_color[edge] = self.edge_green_hex
            elif edge in self.diff.unique_edges2:
                self.edge_color[edge] = self.edge_red_hex
            
            self.edge_penwidth[edge] = 1.0
            self.edge_label[edge] = ""
            
        

