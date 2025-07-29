from abc import abstractmethod
from graphviz import Digraph


class Perspective:
    def __init__(self, dfg):
        """
        Initialize the Perspective with a Directed Flow Graph (DFG).

        Args:
            dfg: The Directed Flow Graph to be used in this perspective.
        """
        self.dfg = dfg
        self.activities = None
        self.stats = None
        self.node_label = {}
        self.node_color = {}
        self.edge_color = {}
        self.edge_penwidth = {}
        self.edge_label = {}
        
    @abstractmethod
    def create_style(self):
        pass
    
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
        
        for activity in self.activities:                      
            graph.node(activity, label=self.node_label[activity], style='filled', fillcolor=self.node_color[activity], fontsize='12')
        
        graph.node(end, shape='doublecircle', fontsize="30")

        for activity, val in self.dfg.im.items():
            graph.edge(start, activity, label=str(val))

        for edge, _ in self.dfg.dfg.items():
            graph.edge(edge[0], edge[1], label=self.edge_label[edge], penwidth=str(self.edge_penwidth[edge]), color=self.edge_color[edge])

        for activity, val in self.dfg.fm.items():
            graph.edge(activity, end, label=str(val))

        return graph
