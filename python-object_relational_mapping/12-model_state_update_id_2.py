#!/usr/bin/python3
"""Rename state number two."""

import sys

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

from model_state import Base, State


if __name__ == "__main__":
    engine = create_engine(
        URL.create(
            'mysql+mysqldb', username=sys.argv[1], password=sys.argv[2],
            host='localhost', port=3306, database=sys.argv[3]
        ),
        pool_pre_ping=True
    )
    Base.metadata.create_all(engine)
    session = Session(engine)
    state = session.query(State).filter(State.id == 2).first()
    if state is not None:
        state.name = 'New Mexico'
        session.commit()
    session.close()
