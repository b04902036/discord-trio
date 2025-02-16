from enum import Enum, auto
import discord
from engine.player import Player
from engine.engine import Engine

class State(Enum):
    GETTING_USER_COUNT = auto()
    REGISTERING_USER = auto()
    GAME_RUNNING = auto()

class StatePersistence:
    """
    All data that will be persistent among states
    
    |@param                 |@type              |@explain|
    |-----------------------|-------------------|---------------|
    |state                  |State              |current state in state machine|
    |count                  |int                |player counts|
    |current_users          |[Player]           |registered user|
    |engine                 |Engine             |game engine|
    """
    def __init__(self, state: State, count: int, current_users: list[Player], engine: Engine):
        self.state = state
        self.count = count
        self.current_users = current_users
        self.engine = engine

    @property
    def persistence(self):
        return self
    
    

# Base class for states
class StateBase(StatePersistence):
    def __init__(self, persistence: StatePersistence):
        super().__init__(persistence.state, persistence.count, persistence.current_users, persistence.engine)

    async def init(self):
        """Anything you want to do when initializing, in asyncio"""

    async def banner(self) -> str:
        """Banner msg for this state"""
        raise NotImplementedError("Each state must implement its own `banner` method.")
    
    async def input(self, msg: discord.Message) -> State:
        """Process input and return output message + next state"""
        raise NotImplementedError("Each state must implement its own `input` method.")