import discord
from state import StateBase, State, StatePersistence
from error import WrongParam
from engine.player import Player
from message import send_message

# Data expected as the state input
class RegisteringUserData():
    def __init__(self, msg: discord.Message):
        if not isinstance(msg, discord.Message):
            raise WrongParam(f"expect msg as discord.Message, get {type(msg)}")
        if not msg.mentions:
            raise WrongParam("expect mentions in message")
        
        self._users = [member for member in msg.mentions]      
    
    @property
    def users(self):
        return self._users
    
class RegisteringUserState(StateBase):
    def __init__(self, persistence: StatePersistence):
        super().__init__(persistence)
        self._current_user_ids = []
        for user in self.current_users:
            self._current_user_ids.append(user.id)

    async def banner(self):
        response = ":heavy_plus_sign: "
        if len(self.current_users) == 0:
            response += "Get people in! Register someone by `@<user1> @<user2>`"
        else:
            response += f"Users {[u.name for u in self.current_users]} already in! Get {self.count - len(self.current_users)} more people here!"
        
        return response

    async def input(self, msg: discord.Message):
        if not isinstance(msg, discord.Message):
            raise WrongParam(f"expect msg as discord.Message, get {type(msg)}")
        
        try:
            data = RegisteringUserData(msg)
        except Exception as e:
            print(f"failed to parse input in {self.state} state: {e}")
            await send_message(msg.channel,  ":x: Wrong input! Expecting mention(s), e.g. @user1")
            return self.state

        response = ""
        to_add = []
        for user in data.users:
            if user.id in self.current_user_ids:
                response += f":white_check_mark: {user.name} already added\n"
            else:
                to_add.append(user)

        if len(self.current_users) + len(to_add) > self.count:
            await send_message(msg.channel,  response + f":no_pedestrians: However too many people here! Expecting {self.count - len(self.current_users)} more, get {[u.name for u in to_add]}")
            return self.state
        
        for user in to_add:
            response += f":ballot_box_with_check: {user.name} registered\n"
            self.current_users.append(Player(user))
            self._current_user_ids.append(user.id)
            await send_message(user, ":white_check_mark: You have been registered for the game!")

        if len(self.current_users) == self.count:
            await send_message(msg.channel,  response + ":white_check_mark: All set!")
            return State.GAME_RUNNING
        
        await send_message(msg.channel,  response + f"{self.count - len(self.current_users)} more left!")
        return State.REGISTERING_USER
    
    @property
    def current_user_ids(self):
        return self._current_user_ids