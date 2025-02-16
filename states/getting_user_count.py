import discord

from state import StateBase, State
from error import WrongParam
from config import ACCEPTED_USER_COUNT
from message import send_message

# Data expected as the state input
class GettingUserCountData():
    def __init__(self, msg: discord.Message):
        if not isinstance(msg, discord.Message):
            raise WrongParam(f"expect discord.Message as input, get {type(msg)}")

        try:
            count = int(msg.content)
        except Exception as e:
            raise WrongParam(f"expecting integer input, get {msg.content}") from e
        
        if count not in ACCEPTED_USER_COUNT:
            raise WrongParam(f"expect user count in {ACCEPTED_USER_COUNT}, get {count}")
        self._count = count

    @property
    def count(self):
        return self._count
    

# State Implementations
# TODO: use command help message here
class GettingUserCountState(StateBase):
    """
    Responsible of setting player count
    """

    async def banner(self):
        return ":pleading_face: Please input user number to start!"

    async def input(self, msg: discord.Message):
        if not isinstance(msg, discord.Message):
            raise WrongParam(f"expect discord.Message as input, get {type(msg)}")
        
        try:
            data = GettingUserCountData(msg)
        except Exception as e:
            print(f"failed to parse input in {self.state} state: {e}")
            await send_message(msg.channel,  ":x: Wrong input! Expecting number as players count")
            return self.state
        
        self.count = data.count
        await send_message(msg.channel,  f":white_check_mark: Starting a game with {self.count} users...")
        return State.REGISTERING_USER