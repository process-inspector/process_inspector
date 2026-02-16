from process_inspector.schemas import ObjectSchema, ActivitySchema, RelationSchema
from process_inspector.compute_ranks import compute_partial_ranks
from abc import ABC, abstractmethod
import numpy as np

    
class ObjectContextBase(ABC):
    def __init__(self):
        self.data = ObjectSchema()
        
    @abstractmethod
    def compute_object_stats(self, case_data):
        """
        compute and populate self.data with object statistics
        """
        raise NotImplementedError()
        
            
    def _compute_partial_ranks(self, bp_data: dict[str, list]):
        partial_ranks = compute_partial_ranks(bp_data, remove_outliers=False)
        # obj_rank = partial_ranks[method]
        # perf_class = partial_ranks['nranks']
        return partial_ranks 

    
class PMContextBase(ABC):
    def __init__(self):
        
        self.activity_data = ActivitySchema()
        self.relation_data = RelationSchema()


    @abstractmethod                
    def compute_activity_stats(self, reverse_maps):
        """
        compute and populate self.activity_data with activity statistics
        """
        raise NotImplementedError()
            
    
    @abstractmethod
    def compute_relation_stats(self, reverse_maps):
        """
        compute and populate self.relation_data with relation statistics
        """
        raise NotImplementedError()
                
    def _compute_rank_score(self, objs:list, obj_rank:dict) -> float:
        assert len(obj_rank) > 0, "Object ranks not available for rank score computation."
        assert len(objs) > 0, "No objects provided for rank score computation."

        total_objs = len(obj_rank)        
        nobjs = len(objs)
        
        # if an op occurs in all objects, it cannot be discriminated hence return -1.0
        if nobjs == total_objs:    
            return -1.0
        
        #If all objs are in the same rank, then the rank score is -1.0 since it does not help in discrimination
        rank_values = set(obj_rank[obj] for obj in obj_rank)
        if len(rank_values) == 1:
            return -1.0
        
        # all other cases, compute average rank score across objects, normalized by number of objects
        rank_score = 0.0
        for obj in objs:
            try:
                rank_score += obj_rank[obj]
            except KeyError:
                raise KeyError(f"Object '{obj}' not found in object ranks.")
        rank_score /= nobjs
            
        return rank_score            
        
    def _compute_partial_ranks(self, obj_bp:dict, invert=False):
        if invert:
            inverted_m = {k: -1*np.array(v) for k, v in obj_bp.items()}
            partial_ranks = compute_partial_ranks(inverted_m, remove_outliers=False)
        else:
            partial_ranks = compute_partial_ranks(obj_bp, remove_outliers=False)
        # obj_rank = partial_ranks[method]
        # perf_class = partial_ranks['nranks']
        
        return partial_ranks 