from typing import Any, List, Type

from fastapi import HTTPException
from pydantic import BaseModel


def ensure_exists(obj: Any, 
                  entity_name:str, 
                  exception: Any, 
                  validate_scheme: Type[BaseModel] | None = None) -> Any:
    if obj is None:
        raise exception(entity_name)
    
    if validate_scheme:
        if isinstance(obj, list):
            return [validate_scheme.model_validate(o) for o in obj]
        return validate_scheme.model_validate(obj)
    return obj
