"""
This file will generate card.py
"""

# Need to provide following definition for all cards in following format
# [card_name, card_chain_target, card_face_up]
CARDS = [
    ["One", [6, 8], ":one:"],
    ["Two", [5, 9], ":two:"],
    ["Three", [4, 10], ":three:"],
    ["Four", [3, 11], ":four:"],
    ["Five", [2, 12], ":five:"],
    ["Six", [1], ":six:"],
    ["Seven", [7], ":seven:"],
    ["Eight", [1], ":eight:"],
    ["Nine", [2], ":nine:"],
    ["Ten", [3], ":keycap_ten:"],
    ["Eleven", [4], "⏸️"],
    ["Twelve", [5], "🔢"],
]

BASE_DEFINITION = """
import functools
from enum import Enum, auto
from error import InternalError

class CardStatus(Enum):
    FACE_UP = auto()
    FACE_DOWN = auto()
    TAKEN = auto()


@functools.total_ordering
class CardBase:
    \"\"\"
    Base of all cards
    \"\"\"
    def __init__(self):
        self._type = CardStatus.FACE_DOWN

    def chain(self) -> list[int]:
        \"\"\"
        Return the chaining target of this card
        \"\"\"

    def __str__(self) -> str:
        \"\"\"
        Showing the card current status and value
        \"\"\"
        if self._type == CardStatus.FACE_UP:
            return self.show_face_up()
        if self._type == CardStatus.FACE_DOWN:
            return self.show_face_down()
        return self.show_taken()


    def show_face_up(self) -> str:
        \"\"\"
        Show the card value
        \"\"\"
    
    def show_face_up_if_exist(self) -> str:
        if self.is_taken():
            return self.show_taken()
        return self.show_face_up()
    
    def show_face_down(self) -> str:
        \"\"\"
        Show the card back
        \"\"\"
        return ":question:"
    
    def show_taken(self) -> str:
        return ":x:"
    
    def turn_up(self):
        if not self.is_taken():
            self._type = CardStatus.FACE_UP
    
    def is_face_up(self):
        return self._type == CardStatus.FACE_UP

    def turn_down(self):
        if not self.is_taken():
            self._type = CardStatus.FACE_DOWN
    
    def is_face_down(self):
        return self._type == CardStatus.FACE_DOWN
            
    def take(self):
        if self.is_taken():
            raise InternalError(f"this card already taken {self}")
        self._type = CardStatus.TAKEN
    
    def is_taken(self) -> bool:
        return self._type == CardStatus.TAKEN

    def is_chain_with(self, other: "CardBase") -> bool:
        \"\"\"
        Whether this card can chain with the other card
        \"\"\"
        return card_to_int[other.__class__] in self.chain()

    def __eq__(self, other: "CardBase") -> bool:
        return card_to_int[self.__class__] == card_to_int[other.__class__]
    
    def __lt__(self, other: "CardBase") -> bool:
        return card_to_int[self.__class__] < card_to_int[other.__class__]

    def __hash__(self):
        return hash(card_to_int[self.__class__])

    @property
    def type(self):
        return self._type
"""

CARD_DEFINITION = """
@functools.total_ordering
class {}(CardBase):
    def chain(self) -> list[int]:
        return {}
    
    def show_face_up(self) -> str:
        return "{}"

"""



if __name__ == "__main__":
    with open("card.py", "w", encoding="utf-8") as f:
        f.write(BASE_DEFINITION)

        for (card, chain, face_up) in CARDS:
            f.write(CARD_DEFINITION.format(card, chain, face_up))

        # write int_to_card
        f.write("int_to_card = {\n")
        for i, (card, _, _) in enumerate(CARDS):
            f.write(f"    {i+1}: {card},\n")
        f.write("}\n\n")

        # write card_to_int
        f.write("card_to_int = {v: k for k, v in int_to_card.items()}\n")
