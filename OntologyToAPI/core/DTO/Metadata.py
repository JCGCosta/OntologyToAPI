from OntologyToAPI.core.DTO.Source import Source

from pydantic import BaseModel

class Metadata(BaseModel):
    name: str
    type: str
    hasSource: Source