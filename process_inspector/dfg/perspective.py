# from abc import abstractmethod
from graphviz import Digraph


class DFGPerspective:
    def __init__(self, dfg):
        """
        Initialize the Perspective with a Directed Flow Graph (DFG).

        Args:
            dfg: The Directed Flow Graph to be used in this perspective.
        """
        self.dfg = dfg
        self.node_label = {}
        self.node_color = {}
        self.edge_color = {}
        self.edge_penwidth = {}
        self.edge_label = {}
        
    
    def create_style(self):
        for activity in self.dfg.nodes:
            self.node_label[activity] = activity
        
        for node in self.node_label:
            self.node_color[node] = "#FFFFFF"
            
        for edge, _ in self.dfg.edges.items():
            self.edge_color[edge] = "#000000"
            self.edge_penwidth[edge] = 1.0
            self.edge_label[edge] = ""
            
        for im, _ in self.dfg.im.items():
            self.edge_color[im] = "#000000"
            self.edge_penwidth[im] = 1.0
            self.edge_label[im] = ""
            
        for fm, _ in self.dfg.fm.items():
            self.edge_color[fm] = "#000000"
            self.edge_penwidth[fm] = 1.0
            self.edge_label[fm] = ""
    
    def prepare_digraph(self, rankdir='LR'):
        """
        Prepare a Directed Graph (Digraph) representing the process flow.

        Returns:
            Digraph: A graph object representing the process flow.
        """
        if not self.dfg:
            logger.error("DFG is not available.")
            return None
        
        graph = Digraph(strict=True, engine='dot', format='png')
        graph.attr(rankdir=rankdir)
        start = "<&#9679;>"
        end = "<&#9632;>"

        graph.node_attr['shape'] = 'box'
        graph.node(start, shape='circle', fontsize="30")
        
        for activity in self.dfg.nodes:                      
            graph.node(activity, label=self.node_label[activity], style='filled', fillcolor=self.node_color[activity], fontsize='12')
        
        graph.node(end, shape='doublecircle', fontsize="30")

        for activity, val in self.dfg.im.items():
            graph.edge(start, activity, label=self.edge_label[activity], penwidth=str(self.edge_penwidth[activity]), color=self.edge_color[activity])

        for edge, _ in self.dfg.edges.items():
            graph.edge(edge[0], edge[1], label=self.edge_label[edge], penwidth=str(self.edge_penwidth[edge]), color=self.edge_color[edge])

        for activity, val in self.dfg.fm.items():
            graph.edge(activity, end, label=self.edge_label[activity], penwidth=str(self.edge_penwidth[activity]), color=self.edge_color[activity])

        return graph
