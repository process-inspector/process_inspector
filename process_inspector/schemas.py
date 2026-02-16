from typing import Dict, List, Tuple, Set
from pydantic import BaseModel, Field

class ActivitySchema(BaseModel):
    activities: Set[str] = Field(default_factory=set)
    records: List[dict] = Field(default_factory=list) # one record per activity
    obj_records: Dict[str, List[dict]] = Field(default_factory=dict) # key: activity, value: list of object records
    obj_bp_data: Dict[str, Dict[str, List[float]]] = Field(default_factory=dict) # key: activity, value: dict of obj to list of bp values
    obj_rank: Dict[str, dict] = Field(default_factory=dict) # key: activity, value: dict of obj to rank
    
    
class RelationSchema(BaseModel):
    relations: Set[str] = Field(default_factory=set)
    records: List[dict] = Field(default_factory=list)
    obj_records: Dict[str, List[dict]] = Field(default_factory=dict) 
    obj_bp_data: Dict[str, Dict[str, List[float]]] = Field(default_factory=dict)
    obj_rank: Dict[str, dict] = Field(default_factory=dict)
    

class ObjectSchema(BaseModel):
    objects: Set[str] = Field(default_factory=set)
    records: List[dict] = Field(default_factory=list)
    rank: Dict = Field(default_factory=dict)
    bp_data: Dict[str, List[float]] = Field(default_factory=dict)
    perf_class: str = ""
    