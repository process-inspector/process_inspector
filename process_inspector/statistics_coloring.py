import pandas as pd
from .perspective import Perspective

class StatisticsColoring(Perspective):
    def __init__(self, dfg):
        super().__init__(dfg)
        self.activities = list(dfg.inv_mapping.keys())
        self.color_by = 'count'
        self.stats = None
        
    
    def compute_stats(self, inv_mapping):
        result = []
        for activity, df in inv_mapping.items():
            count = df.shape[0]
            result.append({
                'activity':activity,
                'count': count,
            })
        self.stats = pd.DataFrame(result)
    
    def _format_label_str(self, row):
        label_str = f"{row['activity']}"
        return label_str
        
    def create_style(self):
        self.compute_stats(self.dfg.inv_mapping)
        self.stats['label_str'] = self.stats.apply(self._format_label_str, axis=1)
        self.node_label = self.stats.set_index('activity')['label_str'].to_dict()
        for edge, label in self.dfg.dfg.items():
            self.edge_color[edge] = "#000000"
            self.edge_penwidth[edge] = 1.0
            self.edge_label[edge] = str(label)
        
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
