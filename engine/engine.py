"""
The game engine
"""
import random
from discord import Message
from error import InternalError, InvalidMove
from message import send_message
from .player import Player
from .card import card_to_int, CardBase
from .hand import Hand
from .move import Move, MoveType, CMD_PICK_PLAYER


# the card to be put in the midde of table
# this map the player cuont to the number of card
# to be put in the middle of table 
player_count_to_left_card_count = {
    3: 9,
    4: 8,
    5: 6,
    6: 6,
}

middle_card_idx = [
    ":zero:",
    ":one:",
    ":two:",
    ":three:",
    ":four:",
    ":five:",
    ":six:",
    ":seven:",
    ":eight:",
    ":nine:",
    ":ten:",
]

class Engine:
    def __init__(self, players: list[Player]):
        self._players = players[:]
        self._next_player_idx = 0
        self._opened_cards = []
        self._middle_cards = []
        self._cards = self.initial_cards()
        self._last_moves = []
        self._should_clear = True
        self.generate_table()

    def initial_cards(self) -> list[CardBase]:
        cards = []
        for k in card_to_int:
            for _ in range(3):
                cards.append(k())
        return cards

    def reset(self):
        self._next_player_idx = 0
        self._opened_cards = []
        self._cards = self.initial_cards()
        self._last_moves = []
        self._should_clear = True
        self.generate_table()

    def generate_table(self):
        """
        Generate the full game table according to player cuont
        1. Setup middle card
        2. Setup card in player's hand
        """
        if len(self._players) not in player_count_to_left_card_count:
            raise NotImplementedError(f"Player count {len(self._players)} not supported")
        
        left_card_count = player_count_to_left_card_count[len(self._players)]
        hand_card_count = (len(self._cards) - left_card_count) // len(self._players)
        if left_card_count + hand_card_count * len(self._players) != len(self._cards):
            raise InternalError(f"left_card_count({left_card_count}) + hand_card_count({hand_card_count}) * self.count({len(self._players)}) != len(self._cards)({len(self._cards)})")
    
        random.shuffle(self._cards)
        count = 0
        self._middle_cards = self._cards[count:count+left_card_count]
        count += left_card_count
        for player in self._players:
            player.hand = Hand(self._cards[count:count+hand_card_count])
            count += hand_card_count

    def current_table(self, viewer: Player):
        """
        Return the current table from specific player's perspective
        If viewer is None, return the full table with minimum exposure
        """
        response = ""

        # middle cards
        response += "Middle: \n"
        response += "\tcards: "
        for card in self._middle_cards:
            response += f"{card}"
        response += "\n"
        response += "\tindex: "
        for idx, _ in enumerate(self._middle_cards):
            response += f"{middle_card_idx[idx]}"
        response += "\n"

        for idx, player in enumerate(self._players):
            response += f"{CMD_PICK_PLAYER}{idx}({player.user.name}): \n"
            response += "  Hand:\t"
            if viewer and player.user.id == viewer.user.id:
                for card in player.hand.cards:
                    response += f"{card.show_face_up_if_exist()}"
            else:
                for card in player.hand.cards:
                    response += f"{card}"
            response += "\n"
            response += "  Completed:\t"
            for card in player.hand.completed:
                response += f"{card.show_face_up_if_exist()}"
            response += "\n"
        
        # last moves
        if self._should_clear:
            player_idx = self.prev_player_idx()
        else:
            player_idx = self._next_player_idx
        response += f"{CMD_PICK_PLAYER}{player_idx}'s last move(s): "
        for move in self._last_moves:
            response += f"[{move} {move.card.show_face_up()}]"
        response += "\n"

        response += f"Next player: {CMD_PICK_PLAYER}{self._next_player_idx} ({self._players[self._next_player_idx].user})\n"

        return response

    async def move(self, msg: Message):
        if not isinstance(msg, Message):
            raise InternalError(f"expecting msg as discord.Message, get {type(msg)}")
        
        move = Move(msg)
        await move.check()
        player = msg.author
        expected_player = self._players[self._next_player_idx]
        if player.id != expected_player.user.id:
            await send_message(player, f":x: Not your turn to play, {player.name}!")
            raise InvalidMove(f"expecting {expected_player} to play, get {player}")
        
        if move.type == MoveType.PICK_MIDDLE:
            card = self._middle_cards[move.card_idx]
        elif move.type == MoveType.PICK_PLAYER_LOWEST:
            if move.player_idx >= len(self._players):
                await send_message(player, ":x: Player index out of range, pick another player!")
                raise InvalidMove(f"player index out of range {move.player_idx}")
            
            target_player = self._players[move.player_idx]
            if target_player.hand.is_empty():
                await send_message(player, ":x: No card in their hand, pick another player!")
                raise InvalidMove(f"no card in player's hand {target_player.hand.cards}")
            
            card = target_player.hand.get_lowest()
        elif move.type == MoveType.PICK_PLAYER_HIGHEST:
            if move.player_idx >= len(self._players):
                await send_message(player, ":x: Player index out of range, pick another player!")
                raise InvalidMove(f"player index out of range {move.player_idx}")
            
            target_player = self._players[move.player_idx]
            if target_player.hand.is_empty():
                await send_message(player, ":x: No card in their hand, pick another player!")
                raise InvalidMove(f"no card in player's hand {target_player.hand.cards}")
            
            card = target_player.hand.get_highest()
        else:
            await send_message(player, ":x: Unknown move, pick another one!")
            raise InvalidMove(f"unknown move {move}")
        
        # cleanup first before any check
        if self._should_clear:  
            for _card in self._opened_cards:
                _card.turn_down()
            self._opened_cards = []
            self._last_moves = []
            self._should_clear = False

        if card.is_taken():
            await send_message(player, ":x: Card already taken, pick another one!")
            raise InvalidMove(f"card already taken {card} ")
        if card.is_face_up():
            await send_message(player, ":x: Card already facing up, pick another one!")
            raise InvalidMove(f"card already facing up {card}")
    
        move.card = card
        card.turn_up()
        self._last_moves.append(move)
        self._opened_cards.append(card)
        
        # check if all opened card are the same
        # we assuem if there are 2 opened card, they are the same
        if len(self._opened_cards) == 3:
            if self._opened_cards[1] == card:
                # cleanup and take the card
                for card in self._opened_cards:
                    card.take()
                self.inc_next_player_idx()
                self._should_clear = True

                # add to player's completed hand
                expected_player.hand.add_completed(card)

                # check if the player win
                if expected_player.hand.is_win():
                    await self.broadcast_winner(expected_player)
                return
        elif len(self._opened_cards) == 2:
            if self._opened_cards[0] == card:
                return
        else:
            return

        # if we didn't early return, means this user can't continue
        self._should_clear = True
        self.inc_next_player_idx()
            
    def inc_next_player_idx(self):
        self._next_player_idx = (self._next_player_idx + 1) % len(self._players)

    def prev_player_idx(self):
        return (self._next_player_idx + (len(self._players) - 1)) % len(self._players)

    async def broadcast_board(self):
        for player in self._players:
            board = self.current_table(player)
            await send_message(player.user, board)

    async def broadcast_winner(self, winner: Player):
        # turn up all cards, and show result
        for card in self._middle_cards:
            card.turn_up()
        for player in self._players:
            for card in player.hand.cards:
                card.turn_up()
        for player in self._players:
            await send_message(player.user, self.current_table(player))
            if player.user.id == winner.user.id:
                await send_message(player.user, ":tada: Congratulation! You win the game!")
            else:
                await send_message(player.user, f":cry: player {winner.user} wins!")
        
        # TODO: we directly exit here. Should try to reuse this bot
        exit(0)

    @property
    def expected_player(self):
        return self._players[self._next_player_idx]
    
    @property
    def opened_cards(self):
        return self._opened_cards
    
    @property
    def hands(self):
        return self._hands
    
    @property
    def middle_cards(self):
        return self._middle_cards
    
    @property
    def cards(self):
        return self._cards
    
    @property
    def players(self):
        return self._players