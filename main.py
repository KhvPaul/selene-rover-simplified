from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from sqlmodel import create_engine, SQLModel, Session

from config import settings
from models import Command, RoverState
from schemas import CommandSchema, Direction
from logger import logger


engine = create_engine(str(settings.DATABASE_ENDPOINT))


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# used to initialize db tables and land rover
@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()

    #initialize rover
    with Session(engine) as session:
        existing = session.get(RoverState, 1)
        if not existing:
            session.add(
                RoverState(
                    id=1,
                    longitude=settings.START_POSITION[0],
                    latitude=settings.START_POSITION[1],
                    direction=settings.START_DIRECTION,
                )
            )
            session.commit()
            logger.info("Initialized RoverState")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", response_model=RoverState)
def retrieve_rover_state(session: Session = Depends(get_session)):
    return session.get(RoverState, 1)


@app.post("/command", response_model=RoverState)
def run_command(command: CommandSchema, session: Session = Depends(get_session)):
    command_input = Command(command_input=command.command_input)
    rover_state = session.get(RoverState, 1)

    def get_new_state(old_state: (int, int, Direction), i: str) -> dict[str, int | Direction]:  # TODO: wtf!
        x = old_state[0]
        y = old_state[1]
        direction = old_state[2]

        if i in ("L", "R"):
            direction = direction.rotate(i)
        else:
            delta_x, delta_y = direction.move_delta(i)
            x += delta_x
            y += delta_y

        return {"longitude": x, "latitude": y, "direction": direction}

    for command in command.command_input:
        new_state = get_new_state(
            old_state=(rover_state.longitude, rover_state.latitude, rover_state.direction), i=command
        )
        # in case of rover runs into an obstacle logging it and scipping rover state update
        if (new_state["longitude"], new_state["latitude"]) in settings.INITIAL_OBSTACLES:
            logger.info(
                f"Rover({rover_state.longitude}, {rover_state.latitude} runs into an obstacle "
                f"({new_state["longitude"], new_state["latitude"]})"
            )
            break
        rover_state.longitude = new_state["longitude"]
        rover_state.latitude = new_state["latitude"]
        rover_state.direction = new_state["direction"]
    session.add(command_input)
    session.add(rover_state)
    return rover_state
