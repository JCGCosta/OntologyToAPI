from Generator.DTO.Metadata import Metadata
from Generator.DTO.ExternalCode import ExternalCode

from typing import List, Optional
from pydantic import BaseModel

class BusinessModel(BaseModel):
    name: str
    communications: dict
    requiresMetadata: List[Metadata]
    resultsMetadata: List[Metadata]
    externalCode: Optional[ExternalCode]