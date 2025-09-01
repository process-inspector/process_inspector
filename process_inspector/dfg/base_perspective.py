# from abc import abstractmethod
from graphviz import Digraph


class DFGBasePerspective:
    def __init__(self, dfg):
        """
        Initialize the Perspective with a Directed Flow Graph (DFG).

        Args:
            dfg: The Directed Flow Graph to be used in this perspective.
        """
        self.dfg = dfg
        self.activity_label = {}
        self.activity_color = {}
        self.edge_color = {}
        self.edge_penwidth = {}
        self.edge_label = {}
        
    
    def create_style(self):
        for node in self.dfg.nodes:
            if not node == '__START__' and not node == '__END__':
                self.activity_label[node] = node
                self.activity_color[node] = "#FFFFFF"
        
            
        for edge in self.dfg.edges:
            self.edge_color[edge] = "#000000"
            self.edge_penwidth[edge] = 1.0
            self.edge_label[edge] = ""
                        
    
    def prepare_digraph(self, rankdir='LR', graph=None):
        """
        Prepare a Directed Graph (Digraph) representing the process flow.

        Returns:
            Digraph: A graph object representing the process flow.
        """
        if not self.dfg:
            logger.error("DFG is not available.")
            return None
        
        if graph is None:
            graph = Digraph(strict=True, engine='dot', format='png')
        graph.attr(rankdir=rankdir)
        graph.node_attr['shape'] = 'box'
        
        graph.node('__START__', label="<&#9679;>", shape='circle', fontsize="30")
        for node in self.dfg.nodes:
            if not node == '__START__' and not node == '__END__':                
                graph.node(node, label=self.activity_label[node], style='filled', fillcolor=self.activity_color[node], fontsize='12')        
        graph.node('__END__', label="<&#9632;>", shape='doublecircle', fontsize="30")
        
        for edge in self.dfg.edges:
            graph.edge(edge[0], edge[1], label=self.edge_label[edge], penwidth=str(self.edge_penwidth[edge]), color=self.edge_color[edge])


        return graph
