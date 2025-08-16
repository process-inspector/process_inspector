import pandas as pd
from .add_dfgs import add_dfgs
from .diff_dfgs import diff_dfgs
from .dfg import DFG
from .perspective import DFGPerspective

class DFGDifferencePerspective(DFGPerspective):
    def __init__(self, dfg1, dfg2,dfg_combined=None):
        
        if dfg_combined is None:
            dfg_combined = add_dfgs(dfg1, dfg2)
        super().__init__(dfg_combined)
        
        self.diff = diff_dfgs(dfg1, dfg2)
        
        self.default_node_color = "#FFFFFF"
        self.default_edge_color = "#000000"
        
        self.node_red_hex = "#EF9A9A"
        self.node_green_hex = "#8BC34A"
        
        self.edge_red_hex = "#E53935"
        self.edge_green_hex = "#2E7D32"
        
        for activity in self.dfg.nodes:
            self.node_label[activity] = activity
        
        
        
    def create_style(self):
        
        for node in self.dfg.nodes:
            self.node_color[node] = self.default_node_color
            if node in self.diff.unique_nodes1:
                self.node_color[node] = self.node_green_hex
            elif node in self.diff.unique_nodes2:
                self.node_color[node] = self.node_red_hex
                
        for edge, label in self.dfg.edges.items():
            self.edge_color[edge] = self.default_edge_color
            if edge in self.diff.unique_edges1:
                self.edge_color[edge] = self.edge_green_hex
            elif edge in self.diff.unique_edges2:
                self.edge_color[edge] = self.edge_red_hex
            
            self.edge_penwidth[edge] = 1.0
            self.edge_label[edge] = str(label)
            
        for im, label in self.dfg.im.items():
            self.edge_color[im] = self.default_edge_color
            if im in self.diff.unique_im1:
                self.edge_color[im] = self.edge_green_hex
            elif im in self.diff.unique_im2:
                self.edge_color[im] = self.edge_red_hex
            
            self.edge_penwidth[im] = 1.0
            self.edge_label[im] = str(label)
            
        for fm, label in self.dfg.fm.items():
            self.edge_color[fm] = self.default_edge_color
            if fm in self.diff.unique_fm1:
                self.edge_color[fm] = self.edge_green_hex
            elif fm in self.diff.unique_fm2:
                self.edge_color[fm] = self.edge_red_hex
            
            self.edge_penwidth[fm] = 1.0
            self.edge_label[fm] = str(label)
        

