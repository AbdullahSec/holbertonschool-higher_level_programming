#!/usr/bin/python3
"""List states whose names contain a."""

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
    states = session.query(State).filter(
        State.name.like('%a%')
    ).order_by(State.id).all()
    for state in states:
        print('{}: {}'.format(state.id, state.name))
    session.close()
