import pandas as pd
from .base_perspective import DFGBasePerspective
from ..compute_ranks import compute_meta_data_ranks

class DFGRanksPerspective(DFGBasePerspective):
    def __init__(self, dfg, reverse_maps, meta_data, *stats_args, **stats_kwargs):
        super().__init__(dfg)
        
        self.meta_data = meta_data
        self.reverse_maps = reverse_maps
        self.total_variants = 0
        
        
        obj_key = stats_kwargs.get('obj_key')
        obj_perf_key = stats_kwargs.get('obj_perf_key')
        if obj_key is None or obj_perf_key is None:
            raise ValueError("obj_key and on must be provided as keyword arguments.")
        
        self.total_variants = self.meta_data.get_case_data()[obj_key].nunique()
        self.obj_ranks = compute_meta_data_ranks(self.meta_data.get_case_data(), group_by=obj_key, on=obj_perf_key)
        
        self.activity_rank_score = self.compute_activities_rank_score(obj_key=obj_key)
        self.edge_rank_score = self.compute_edges_rank_score(obj_key=obj_key)
        
    def create_style(self):       
        max_rank_score = max(self.activity_rank_score.values())    
        for node in self.dfg.nodes:
            if not node == '__START__' and not node == '__END__':
                self.activity_label[node] = f'{node}\nRank score: {self.activity_rank_score[node]:.1f}'
                self.activity_color[node] = self._get_activity_color(self.activity_rank_score[node], 0.0, max_rank_score)
        

        max_rank_score = max(self.edge_rank_score.values())                
        for edge in self.dfg.edges:
            self.edge_color[edge] = self._get_edge_color(self.edge_rank_score[edge], 0.0, max_rank_score)
            self.edge_penwidth[edge] = 1.0
            self.edge_label[edge] = f'{self.edge_rank_score[edge]:.1f}'
        
        
    def compute_activities_rank_score(self, obj_key):
        activity_rank_score = {}
        for activity, df in self.reverse_maps.activities_map.items():
            
            nvariants = df[obj_key].nunique()
            if nvariants == self.total_variants:
                activity_rank_score[activity] = 0.0
                continue
            
            rank_score = 0.0
            for obj in df[obj_key].unique():
                rank_score += self.obj_ranks['m1'][obj]
            rank_score = rank_score / nvariants
            activity_rank_score[activity] = rank_score
            
        return activity_rank_score
    
    
    def compute_edges_rank_score(self, obj_key):
        edge_rank_score = {}
        for edge, df in self.reverse_maps.edges_map.items():
            
            _obj_key = obj_key
            if edge[0] == '__START__':
                _obj_key = f'next_{obj_key}'            

            nvariants = df[_obj_key].nunique()
            if nvariants == self.total_variants:
                edge_rank_score[edge] = 0.0
                continue
            
            rank_score = 0.0
            for obj in df[_obj_key].unique():
                rank_score += self.obj_ranks['m1'][obj]
            rank_score = rank_score / nvariants
            edge_rank_score[edge] = rank_score
            
        return edge_rank_score      
    
                    
    def _get_activity_color(self, trans_count, min_trans_count, max_trans_count):
        try:
            trans_base_color = int(255 - 100 * (trans_count - min_trans_count) / (max_trans_count - min_trans_count + 0.00001))
            trans_base_color_hex = str(hex(trans_base_color))[2:].upper().zfill(2)
            #return "#" + trans_base_color_hex + trans_base_color_hex + "FF"
            return "#FF" + trans_base_color_hex + trans_base_color_hex
        except ValueError:
            # this happens if trans_count is NaN or _sum is 0
            return "#FFFFFF"    
        
    def _get_edge_color(self, trans_count, min_trans_count, max_trans_count):
        try:
            trans_base_color = int(255 * (trans_count - min_trans_count) / (max_trans_count - min_trans_count + 1e-9))
            trans_base_color_hex = str(hex(trans_base_color))[2:].upper().zfill(2)
            return "#" + trans_base_color_hex + "0000"
        except ValueError:
            # this happens if trans_count is NaN or _sum is 0
            return "#000000"