from pydantic import BaseModel, ConfigDict

class TableCreate(BaseModel):
    name: str
    seats: int
    location: str


class TableBase(TableCreate):
    id: int
    name: str
    seats: int
    location: str


class Table(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)

