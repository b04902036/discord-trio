import discord
from discord.ext import commands
from discord.channel import TextChannel, DMChannel

from config import GAME_CHANNEL_NAME
from state_manager import StateManager

class Bot(commands.Bot):
    def __init__(self):
        # Ensure the bot can read message content
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

        self.registered_users = set()
        self.state_manager = StateManager()
        
    # Event that runs when the bot is ready
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    # Event that listens for messages
    async def on_message(self, message):
        # Make sure the bot doesn't reply to itself
        if message.author == self.user:
            return
        
        # Only response to message in GAME_CHANNEL_NAME or DM
        if isinstance(message.channel, TextChannel):
            if message.channel.name != GAME_CHANNEL_NAME:
                return
        elif not isinstance(message.channel, DMChannel):
            return
        
        # Process other commands if there are any
        if message.content.startswith(self.command_prefix):
            await self.process_commands(message)
        else:
            await self.state_manager.process_input(message) 
        

    async def setup_hook(self):
        """Load cogs on startup."""
        await self.load_extension("cogs.trio")
        await self.load_extension("cogs.rule")
