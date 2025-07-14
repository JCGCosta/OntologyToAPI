from pydantic import BaseModel

class Source(BaseModel):
    desc: str
    query: str
    comm_technology: object