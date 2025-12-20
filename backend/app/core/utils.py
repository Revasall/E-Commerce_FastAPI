from typing import Any, List, Type

from fastapi import HTTPException
from pydantic import BaseModel


def ensure_exists(obj: Any, 
                  entity_name:str, 
                  exception:HTTPException, 
                  validate_sheme: Type[BaseModel]) -> BaseModel | List[BaseModel]:
    if obj is None:
        raise exception(entity_name)
    
    if isinstance(obj, list):
        return [validate_sheme.model_validate(o) for o in obj]
    return validate_sheme.model_validate(obj)