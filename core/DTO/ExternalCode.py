from typing import List, Optional
from pydantic import BaseModel

class ExternalCode(BaseModel):
    pythonFile: str
    function: str
    requiresLib: List[str]