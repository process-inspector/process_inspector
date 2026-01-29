import pandas as pd
from .base_perspective import DFGBasePerspective

class DFGDifferencePerspective(DFGBasePerspective):
    def __init__(self, activities1, relations1,
                 activities2, relations2):
        
        self.activities = activities1 | activities2
        self.relations = relations1 | relations2
        
        super().__init__(self.activities, self.relations)
        
        self.unique_activities1, self.unique_activities2 = self._get_unique_elements(activities1, activities2)
        self.unique_relations1, self.unique_relations2 = self._get_unique_elements(relations1, relations2)
        
        
        self.default_activity_color = "#FFFFFF"
        self.default_edge_color = "#000000"
        
        self.node_red_hex = "#EF9A9A"
        self.node_green_hex = "#8BC34A"
        
        self.edge_red_hex = "#E53935"
        self.edge_green_hex = "#2E7D32"
                
    
    def _get_unique_elements(self, set1, set2):
        unique1 = [item for item in set1 if item not in set2]
        unique2 = [item for item in set2 if item not in set1]
        return unique1, unique2
        
    def create_style(self):
        
        for activity in self.activities:
            self.activity_label[activity] = activity
            self.activity_color[activity] = self.default_activity_color
            if activity in self.unique_activities1:
                self.activity_color[activity] = self.node_green_hex
            elif activity in self.unique_activities2:
                self.activity_color[activity] = self.node_red_hex
                
        for relation in self.relations:
            self.edge_color[relation] = self.default_edge_color
            if relation in self.unique_relations1:
                self.edge_color[relation] = self.edge_green_hex
            elif relation in self.unique_relations2:
                self.edge_color[relation] = self.edge_red_hex
            
            self.edge_penwidth[relation] = 1.0
            self.edge_label[relation] = ""
            
        

