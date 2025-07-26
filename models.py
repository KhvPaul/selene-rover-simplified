from sqlmodel import SQLModel, Field

import schemas


class RoverState(SQLModel, table=True):
    id: int | None = Field(1, primary_key=True)
    longitude: int
    latitude: int
    direction: schemas.Direction


class Command(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)
    command_input: str
