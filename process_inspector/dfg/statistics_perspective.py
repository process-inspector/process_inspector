import pandas as pd
from .perspective import DFGPerspective

class DFGStatisticsPerspective(DFGPerspective):
    def __init__(self, dfg, activity_events):
        super().__init__(dfg)
        
        #check if nodes of dfg and activity_events keys match
        if not set(self.dfg.nodes).issubset(set(activity_events.keys())):
            raise ValueError("DFG nodes must be a subset of activity events keys.")
        
        
        self.color_by = 'count'
        self.stats = self._compute_stats(activity_events)
        self.stats['label_str'] = self.stats.apply(self._format_label_str, axis=1)
        self.node_label = self.stats.set_index('activity')['label_str'].to_dict()
        
    
    def _compute_stats(self, activity_events):
        result = []
        for activity, events_df in activity_events.items():
            count = events_df.shape[0]
            result.append({
                'activity':activity,
                'count': count,
            })
        return pd.DataFrame(result)
    
    def _format_label_str(self, row):
        label_str = f"{row['activity']} ({row['count']})"
        return label_str
        
    def create_style(self):

        for edge, label in self.dfg.edges.items():
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
        
        sum_ = self.stats[self.color_by].sum()
        self.node_color = self.stats.set_index('activity').apply(
            lambda row: self._get_node_color(row[self.color_by]/sum_, 0.0, 1.0), axis=1
        ).to_dict()

    
    def _get_node_color(self, trans_count, min_trans_count, max_trans_count):
        """
        Get color representation based on the transaction count.

        Args:
            trans_count (float): The transaction count.
            min_trans_count (float): The minimum transaction count.
            max_trans_count (float): The maximum transaction count.

        Returns:
            str: A hexadecimal color code representing the transaction count.
        """
        trans_base_color = int(255 - 100 * (trans_count - min_trans_count) / (max_trans_count - min_trans_count + 0.00001))
        trans_base_color_hex = str(hex(trans_base_color))[2:].upper()
        return "#" + trans_base_color_hex + trans_base_color_hex + "FF"
