from typing import Any, List, Type

from fastapi import HTTPException
from pydantic import BaseModel


def ensure_exists(obj: Any, 
                  entity_name:str, 
                  exception: Any, 
                  validate_scheme: Type[BaseModel] | None = None) -> Any:
    """
    Validates the existence of an object and optionally parses it into a Pydantic model.

    This utility is designed to reduce boilerplate code in services and repositories
    by handling common 'Not Found' checks and schema transformations in one call.
    """
    
    if obj is None:
        raise exception(entity_name)
    
    if validate_scheme:
        if isinstance(obj, list):
            return [validate_scheme.model_validate(o) for o in obj]
        return validate_scheme.model_validate(obj)
    return obj
