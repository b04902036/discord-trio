from discord.ext import commands
from message import send_message

class TrioCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trio(self, ctx):
        banner = await self.bot.state_manager.banner()
        await send_message(ctx, banner)

async def setup(bot):
    await bot.add_cog(TrioCommand(bot))