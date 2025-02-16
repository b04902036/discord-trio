"""
Representing the hand of each player
"""
from sortedcontainers import SortedSet
from config import GameMode, GAME_MODE
from error import InvalidMove
from .card import CardBase, int_to_card

class Hand:
    def __init__(self, cards: list[CardBase]):
        self._cards = cards
        self._cards.sort()
        self._completed = SortedSet()

    def add_completed(self, card: CardBase):
        self._completed.add(card.__class__())

    def is_empty(self):
        return len(self._cards) == 0

    def get_lowest(self) -> CardBase:
        for card in self._cards:
            if card.is_face_down():
                return card
        raise InvalidMove("no card in hands")
    
    def get_highest(self) -> CardBase:
        for card in self._cards[::-1]:
            if card.is_face_down():
                return card
        raise InvalidMove("no card in hands")
    
    def is_win(self):
        if GAME_MODE == GameMode.SIMPLE:
            return len(self._completed) >= 3
        elif GAME_MODE == GameMode.TRIO:
            # check if there is chain pair in self._completed
            for completed in self._completed:
                target_chains = completed.chain()
                for target in target_chains:
                    # what we get from int_to_card is just class type, not instance
                    target = int_to_card[target]()
                    if target in self._completed:
                        return True
            return False
        else:
            raise NotImplementedError(f"game mode not implemented {GAME_MODE}")
    
    @property
    def cards(self):
        return self._cards

    @property
    def completed(self) -> set[CardBase]:
        return self._completed
    