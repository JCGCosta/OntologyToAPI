from OntologyToAPI.core.DTO.Metadata import Metadata
from OntologyToAPI.core.DTO.ExternalCode import ExternalCode

from typing import List, Optional
from pydantic import BaseModel

class BusinessModel(BaseModel):
    name: str
    requiresMetadata: Optional[List[Metadata]]
    requiresParameters: Optional[dict]
    externalCode: Optional[ExternalCode]