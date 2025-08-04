from partial_ranker import QuantileComparer, PartialRanker, Method
import numpy as np

def compute_partial_ranks(inv_mapping, group_by, on):
    ranks = {}
    for activity, df in inv_mapping.items():
        measurements =  df.groupby(group_by)[on].apply(lambda x: [float(v) for v in x if v is not np.nan]).to_dict()
        
        ranks[activity] = {}
        ranks[activity]['measurements'] = measurements
        
        
        cm = QuantileComparer(measurements)
        cm.compute_quantiles(q_max=75, q_min=25)
        cm.compare()
        pr = PartialRanker(cm)
        
        pr.compute_ranks(Method.DFG)
        ranks_m1 = pr.get_ranks()
        nranks_m1 = len(ranks_m1)
        ranks[activity]['m1'] = ranks_m1
        
        
        pr.compute_ranks(Method.DFGReduced)
        ranks_m2 = pr.get_ranks()
        nranks_m2 = len(ranks_m2)        
        ranks[activity]['m2'] = ranks_m2
        
        pr.compute_ranks(Method.Min)
        ranks_m3 = pr.get_ranks()
        nranks_m3 = len(ranks_m3)
        ranks[activity]['m3'] = ranks_m3
        
        rank_str = f'{nranks_m1}-{nranks_m2}-{nranks_m3}'
        ranks[activity]['rank_str'] = rank_str
    
        
    return ranks        
        
        
        
        # for k,v in data[activity].items():
            
        #     print(f"Activity: {activity}, Group: {k}, Values: {v}")