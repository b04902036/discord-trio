from discord.ext import commands
from engine.card import card_to_int, int_to_card, Seven
from config import GAME_MODE, GameMode
from message import send_message

class RuleCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rule(self, ctx):
        response = ""
        if GAME_MODE == GameMode.SIMPLE:
            response += ":sound: Your winning condition is to gather 3 completed set\n"
        elif GAME_MODE == GameMode.TRIO:
            response += ":sound: Your winning condition is to gather a pair of chain, chain info as follows\n"
            cards = [card() for card in card_to_int]
            cards.sort()
            for card in cards:
                response += f"\t{card.show_face_up()}: {[int_to_card[c]().show_face_up() for c in card.chain()]}\n"
            response += f":sound: Noted that {Seven().show_face_up()} is special, you win as long as you get it!\n"
        else:
            response += f":x: Game mode {GAME_MODE} not supported!\n"
        await send_message(ctx, response)

async def setup(bot):
    await bot.add_cog(RuleCommand(bot))