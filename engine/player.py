from discord import Member
from error import InternalError
from .hand import Hand

class Player:
    def __init__(self, user: Member):
        self._user = user
        self._hand = None

    @property
    def user(self):
        return self._user
    
    @property
    def hand(self):
        return self._hand
    
    @hand.setter
    def hand(self, new_hand: Hand):
        if not isinstance(new_hand, Hand):
            raise InternalError(f"when setting player hand, expect Hand, get {type(new_hand)}")
        self._hand = new_hand