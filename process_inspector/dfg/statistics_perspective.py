import pandas as pd
from .base_perspective import DFGBasePerspective

class DFGStatisticsPerspective(DFGBasePerspective):
    def __init__(self, dfg, reverse_maps, *stats_args, **stats_kwargs):
        super().__init__(dfg)
        
        #check if nodes of dfg and activity_events keys match
        if not set(set(reverse_maps.activities_map.keys())).issubset(self.dfg.nodes):
            raise ValueError("DFG nodes must be a subset of reverse map node keys.")
        
        
        self.color_by = 'count'
        
        self.activities_stats = self._compute_node_stats(reverse_maps, *stats_args, **stats_kwargs)
        self.activities_stats['label_str'] = self.activities_stats.apply(self._format_activity_label_str, axis=1)
        self.activity_label = self.activities_stats.set_index('activity')['label_str'].to_dict()
        
        self.edge_stats = self._compute_edge_stats(reverse_maps)
        self.edge_stats['label_str'] = self.edge_stats.apply(self._format_edge_label_str, axis=1)
        self.edge_label = self.edge_stats.set_index('edge')['label_str'].to_dict()
        
        
    
    def _compute_node_stats(self, reverse_maps, *args, **kwargs):
        result = []
        for activity, df in reverse_maps.activities_map.items():
            count = df.shape[0]
            result.append({
                'activity':activity,
                'count': count,
            })
        return pd.DataFrame(result)
    
    def _format_activity_label_str(self, row):
        label_str = f"{row['activity']} ({row['count']})"
        return label_str
    
    def _compute_edge_stats(self, reverse_maps):
        result = []
        for (activity, next_activity), df in reverse_maps.edges_map.items():
            count = df.shape[0]
            result.append({
                'edge': (activity, next_activity),
                'count': count,
            })
        return pd.DataFrame(result)
    
    def _format_edge_label_str(self, row):
        label_str = f"{row['count']}"
        return label_str
        
    def create_style(self):

        for edge in self.dfg.edges:
            self.edge_color[edge] = "#000000"
            self.edge_penwidth[edge] = 1.0
            
        
        sum_ = self.activities_stats[self.color_by].sum()
        self.activity_color = self.activities_stats.set_index('activity').apply(
            lambda row: self._get_activity_color(row[self.color_by]/sum_, 0.0, 1.0), axis=1
        ).to_dict()

    
    def _get_activity_color(self, trans_count, min_trans_count, max_trans_count):
        """
        Get color representation based on the transaction count.

        Args:
            trans_count (float): The transaction count.
            min_trans_count (float): The minimum transaction count.
            max_trans_count (float): The maximum transaction count.

        Returns:
            str: A hexadecimal color code representing the transaction count.
        """
        try:
            trans_base_color = int(255 - 100 * (trans_count - min_trans_count) / (max_trans_count - min_trans_count + 0.00001))
            trans_base_color_hex = str(hex(trans_base_color))[2:].upper()
            return "#" + trans_base_color_hex + trans_base_color_hex + "FF"
        except ValueError:
            # this happens if trans_count is NaN or _sum is 0
            return "#FFFFFF"
