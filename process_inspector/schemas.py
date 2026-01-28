from typing import Dict, List, Tuple
from pydantic import BaseModel, Field

class ActivitySchema(BaseModel):
    records: List[dict] = Field(default_factory=list)
    obj_records: Dict[str, List[dict]] = Field(default_factory=dict)
    obj_bp_data: Dict[str, Dict[str, List[float]]] = Field(default_factory=dict)
    obj_rank: Dict[str, Dict[str, int]] = Field(default_factory=dict)
    
    
class RelationSchema(BaseModel):
    records: List[dict] = Field(default_factory=list)
    obj_records: Dict[Tuple[str, str], List[dict]] = Field(default_factory=dict) # tuple keys cant be serialized to json
    obj_bp_data: Dict[Tuple[str, str], Dict[str, List[float]]] = Field(default_factory=dict)
    obj_rank: Dict[Tuple[str, str], Dict[str, int]] = Field(default_factory=dict)
    

class ObjectSchema(BaseModel):
    records: List[dict] = Field(default_factory=list)
    rank: Dict[str, int] = Field(default_factory=dict)
    bp_data: Dict[str, List[float]] = Field(default_factory=dict)
    perf_class: str = ""
    