from partial_ranker import QuantileComparer, PartialRanker, Method
import numpy as np
import pandas as pd


def compute_partial_ranks(measurements,q_max=75, q_min=25):
    cm = QuantileComparer(measurements)
    cm.compute_quantiles(q_max=q_max, q_min=q_min)
    cm.compare()
    pr = PartialRanker(cm)
    
    pr.compute_ranks(Method.DFG)
    nranks_m1 = len(pr.get_ranks())
    ranks_m1 = pr.ranker._obj_rank
    
    pr.compute_ranks(Method.DFGReduced)
    nranks_m2 = len(pr.get_ranks())
    ranks_m2 = pr.ranker._obj_rank
    
    pr.compute_ranks(Method.Min)
    nranks_m3 = len(pr.get_ranks())
    ranks_m3 = pr.ranker._obj_rank
    
    nranks = f'{nranks_m1}-{nranks_m2}-{nranks_m3}'
    
    return {
        'm1': ranks_m1,
        'm2': ranks_m2,
        'm3': ranks_m3,
        'nranks': nranks
    }
    

def compute_activity_ranks(inv_mapping, group_by, on, q_max=75, q_min=25):
    ranks = {}
    for activity, df in inv_mapping.items():
        measurements =  df.groupby(group_by)[on].apply(lambda x: [float(v) for v in x if pd.notna(v)]).to_dict()
        # print(measurements)
        ranks[activity] = {}
        ranks[activity]['measurements'] = measurements
        
        rank_data = compute_partial_ranks(measurements, q_max=q_max, q_min=q_min)
        for k, v in rank_data.items():
            ranks[activity][k] = v
    
    return ranks        