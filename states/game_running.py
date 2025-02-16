import discord

from state import StateBase, State
from error import WrongParam
from engine.engine import Engine
from engine.move import CMD_PICK_MIDDLE, CMD_PICK_PLAYER_HIGHEST, CMD_PICK_PLAYER_LOWEST, CMD_PICK_PLAYER

# State Implementations
# TODO: use command help message here
class GameRunningState(StateBase):
    """
    Generating game state for all user
    """
    def __init__(self, persistence):
        super().__init__(persistence)
        self.engine = Engine(self.current_users)
    
    async def init(self):
        await self.engine.broadcast_board()

    async def banner(self):
        response = "Choose one card to flip by one of following commands (all using zero index)\n"
        response += f" - {CMD_PICK_MIDDLE}<idx>\n"
        response += "    - Flip one card from the public place on table\n"
        response += f" - {CMD_PICK_PLAYER}<idx>{CMD_PICK_PLAYER_HIGHEST}\n"
        response += "   - Pick highest card from player at index <idx>\n"
        response += f" - {CMD_PICK_PLAYER}<idx>{CMD_PICK_PLAYER_LOWEST}\n"
        response += "   - Pick lowest card from player at index <idx>\n"
        response += f":pleading_face: Waiting for player {self.engine.expected_player.user} to move"
        return response

    async def input(self, msg: discord.Message):
        if not isinstance(msg, discord.Message):
            raise WrongParam(f"expect discord.Message as input, get {type(msg)}")
        await self.engine.move(msg)
        await self.engine.broadcast_board()
        return self.state