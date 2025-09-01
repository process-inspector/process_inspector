# Process Inspector
# Contributors:
# - Aravind Sankaran

import time
# import pm4py
from collections import Counter
import pickle
import os
from .logging_config import logger
from types import SimpleNamespace


class DFG:
    def __init__(self,activity_log):
        self.nodes = None
        self.edges = None
                        
        self.nodes, self.edges = self._construct_dfg(activity_log)
            
    
    def _construct_dfg(self, activity_log):
        nodes = activity_log.activities | {'__START__', '__END__'}
        edges = set()
        
        for activit_trace, count in activity_log.activity_language.items():
            edges.add(('__START__', activit_trace[0]))
            
            for i in range(len(activit_trace) - 1):
                edge = (activit_trace[i], activit_trace[i + 1])
                edges.add(edge)

            edges.add((activit_trace[-1], '__END__'))
        
        return nodes, edges
    
    def __add__(self, other):
        if not isinstance(other, DFG):
            raise ValueError("Can only add another DFG instance.")
        
        new_dfg = DFG.__new__(DFG)
        new_dfg.nodes = self.nodes | other.nodes
        new_dfg.edges = self.edges | other.edges
        
        return new_dfg
    
    def diff(self, other):
        if not isinstance(other, DFG):
            raise TypeError("Unsupported operand type(s) for -: 'DFG' and '{}'".format(type(other).__name__))
        
        # Use a helper function for clarity, or put logic directly here
        def get_unique_elements(set1, set2):
            unique1 = [item for item in set1 if item not in set2]
            unique2 = [item for item in set2 if item not in set1]
            return unique1, unique2

        # Calculate differences for all attributes
        unique_nodes1, unique_nodes2 = get_unique_elements(self.nodes, other.nodes)
        unique_edges1, unique_edges2 = get_unique_elements(self.edges, other.edges)
        
        # Create a dictionary to hold the results
        diff_dict = {
            "unique_nodes1": unique_nodes1,
            "unique_nodes2": unique_nodes2,
            "unique_edges1": unique_edges1,
            "unique_edges2": unique_edges2,
        }
        
        # Return the result as a SimpleNamespace
        return SimpleNamespace(**diff_dict)
        
        
    
        

    
    