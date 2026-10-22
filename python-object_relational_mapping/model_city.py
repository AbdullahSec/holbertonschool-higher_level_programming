#!/usr/bin/python3
"""Define the City model for the cities table."""

from sqlalchemy import Column, ForeignKey, Integer, String

from model_state import Base


class City(Base):
    """Represent a city linked to a state."""

    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(128), nullable=False)
    state_id = Column(Integer, ForeignKey('states.id'), nullable=False)
