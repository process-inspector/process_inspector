from partial_ranker import QuantileComparer, PartialRanker, Method
import numpy as np
import pandas as pd


def compute_partial_ranks(measurements,q_max=75, q_min=25, remove_outliers=True):
    cm = QuantileComparer(measurements)
    cm.compute_quantiles(q_max=q_max, q_min=q_min, outliers=remove_outliers)
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
    
def compute_meta_data_ranks(meta_data_df, group_by, on, q_max=75, q_min=25, remove_outliers=True):
    ranks = {}
    measurements = meta_data_df.groupby(group_by)[on].apply(lambda x: [float(v) for v in x if pd.notna(v)]).to_dict()
    ranks['measurements'] = measurements
    rank_data = compute_partial_ranks(measurements, q_max=q_max, q_min=q_min, remove_outliers=remove_outliers)
    for k, v in rank_data.items():
        ranks[k] = v
    return ranks
    

def compute_activity_ranks(activity_events, group_by, on, q_max=75, q_min=25, remove_outliers=True):
    ranks = {}
    for activity, df in activity_events.items():
        measurements =  df.groupby(group_by)[on].apply(lambda x: [float(v) for v in x if pd.notna(v)]).to_dict()
        # print(measurements)
        ranks[activity] = {}
        ranks[activity]['measurements'] = measurements
        
        rank_data = compute_partial_ranks(measurements, q_max=q_max, q_min=q_min, remove_outliers=remove_outliers)
        for k, v in rank_data.items():
            ranks[activity][k] = v
    
    return ranks        