"""
This file stores all possible move for a user
"""
from discord import Message
from enum import Enum, auto
from error import WrongParam, InvalidMove
from message import send_message


CMD_PICK_MIDDLE = "m"
CMD_PICK_PLAYER = "p"
CMD_PICK_PLAYER_LOWEST = "l"
CMD_PICK_PLAYER_HIGHEST = "h"

class MoveType(Enum):
    PICK_MIDDLE = auto()
    PICK_PLAYER_LOWEST = auto()
    PICK_PLAYER_HIGHEST = auto()


class Move:
    def __init__(self, msg: Message):
        self._msg = msg
        self._player_idx = 0
        self._type = None
        self._card_idx = 0
        self._card = None

    async def check(self):
        if not isinstance(self._msg, Message):
            raise WrongParam(f"expect msg as discord.Message, get {type(self._msg)}")
        self._player_idx = 0

        content = self._msg.content.replace(" ", "").replace("\n", "")
        if len(content) < 2:
            await self.wrong_move(content)
        
        cmd, content = content[0], content[1:]
        if cmd == CMD_PICK_MIDDLE:
            self._type = MoveType.PICK_MIDDLE
            card_idx = content
            if not card_idx.isdigit():
                await self.wrong_move(content) 
            self._card_idx = int(card_idx)
        elif cmd == CMD_PICK_PLAYER and content[:-1].isdigit():
            self._player_idx = int(content[:-1])
            card_idx = content[-1]
            if card_idx == CMD_PICK_PLAYER_LOWEST:
                self._type = MoveType.PICK_PLAYER_LOWEST
            elif card_idx == CMD_PICK_PLAYER_HIGHEST:
                self._type = MoveType.PICK_PLAYER_HIGHEST
            else:
                await self.wrong_move(content)
        else:
            await self.wrong_move(content)
        

    async def wrong_move(self, content: list[str]):
        await send_message(self._msg.author, ":x: Wrong move! type !trio for help")
        raise InvalidMove(f"got unknown move command {content}")

    def __str__(self) -> str:
        return self._msg.content

    @property
    def type(self):
        return self._type
    
    @property
    def card_idx(self):
        return self._card_idx
    
    @property
    def player_idx(self):
        return self._player_idx
    
    @property
    def card(self):
        return self._card
    
    @card.setter
    def card(self, new_card):
        self._card = new_card
    