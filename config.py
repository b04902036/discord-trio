from enum import Enum, auto

class GameMode(Enum):
    # Win condition is to get 3 completed set
    SIMPLE = auto()
    # Win condition is to get 2 completed set which is chain to each other
    # Special case is 7, only need 1 completed set
    TRIO = auto()
    # Not implemented yet
    # TEAM = auto()

ACCEPTED_USER_COUNT = [1, 2, 3, 4, 5, 6]
GAME_CHANNEL_NAME = 'trio'
GAME_MODE = GameMode.TRIO