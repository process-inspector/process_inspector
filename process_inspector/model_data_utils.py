
import pickle
import os
import pandas as pd
from .meta_data import MetaData
        
        
def save_model_data(data_dir, process_model, classified_event_traces, meta_data=None):
    os.makedirs(data_dir, exist_ok=True)
    process_model.save(data_dir)
    
    ae_file = os.path.join(data_dir, 'classified_event_traces.pkl')
    with open(ae_file, 'wb') as f:
        pickle.dump(classified_event_traces, f)
    
    if meta_data is not None:
        # Save meta data if provided
        md_file = os.path.join(data_dir, 'meta_data.pkl')
        with open(md_file, 'wb') as f:
            pickle.dump(meta_data, f)    
        
        
def load_model_data(data_dir, process_model):
    process_model.restore(data_dir)
    ae_file = os.path.join(data_dir, 'classified_event_traces.pkl')
    md_file = os.path.join(data_dir, 'meta_data.pkl')
    
    if not os.path.exists(ae_file) or not os.path.exists(md_file):
        raise FileNotFoundError("Activity events or meta data file does not exist.")
    
    try:
        with open(ae_file, 'rb') as f:
            activity_events = pickle.load(f)
    except Exception as e:
        raise ValueError(f"Error loading activity events: {e}")
    
    
    meta_data = None
    if os.path.exists(md_file): 
        with open(md_file, 'rb') as f:
            meta_data = pickle.load(f)
        
    return process_model, activity_events, meta_data

def concat_activity_events(*activity_events):
    combined = {}
    for ae in activity_events:
        for activity, df in ae.items():
            if activity not in combined:
                combined[activity] = df
            else:
                combined[activity] = pd.concat([combined[activity], df], ignore_index=True)
    return combined

def concat_meta_data(*meta_data):
    case_data = []
    obj_data = []
    for md in meta_data:
        case_data.extend(md.case_data)
        obj_data.extend(md.obj_data)
    combined_meta_data = MetaData()
    combined_meta_data.case_data = case_data
    combined_meta_data.obj_data = obj_data
    return combined_meta_data 