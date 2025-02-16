
import functools
from enum import Enum, auto
from error import InternalError

class CardStatus(Enum):
    FACE_UP = auto()
    FACE_DOWN = auto()
    TAKEN = auto()


@functools.total_ordering
class CardBase:
    """
    Base of all cards
    """
    def __init__(self):
        self._type = CardStatus.FACE_DOWN

    def chain(self) -> list[int]:
        """
        Return the chaining target of this card
        """

    def __str__(self) -> str:
        """
        Showing the card current status and value
        """
        if self._type == CardStatus.FACE_UP:
            return self.show_face_up()
        if self._type == CardStatus.FACE_DOWN:
            return self.show_face_down()
        return self.show_taken()


    def show_face_up(self) -> str:
        """
        Show the card value
        """
    
    def show_face_up_if_exist(self) -> str:
        if self.is_taken():
            return self.show_taken()
        return self.show_face_up()
    
    def show_face_down(self) -> str:
        """
        Show the card back
        """
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
        """
        Whether this card can chain with the other card
        """
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

@functools.total_ordering
class One(CardBase):
    def chain(self) -> list[int]:
        return [6, 8]
    
    def show_face_up(self) -> str:
        return ":one:"


@functools.total_ordering
class Two(CardBase):
    def chain(self) -> list[int]:
        return [5, 9]
    
    def show_face_up(self) -> str:
        return ":two:"


@functools.total_ordering
class Three(CardBase):
    def chain(self) -> list[int]:
        return [4, 10]
    
    def show_face_up(self) -> str:
        return ":three:"


@functools.total_ordering
class Four(CardBase):
    def chain(self) -> list[int]:
        return [3, 11]
    
    def show_face_up(self) -> str:
        return ":four:"


@functools.total_ordering
class Five(CardBase):
    def chain(self) -> list[int]:
        return [2, 12]
    
    def show_face_up(self) -> str:
        return ":five:"


@functools.total_ordering
class Six(CardBase):
    def chain(self) -> list[int]:
        return [1]
    
    def show_face_up(self) -> str:
        return ":six:"


@functools.total_ordering
class Seven(CardBase):
    def chain(self) -> list[int]:
        return [7]
    
    def show_face_up(self) -> str:
        return ":seven:"


@functools.total_ordering
class Eight(CardBase):
    def chain(self) -> list[int]:
        return [1]
    
    def show_face_up(self) -> str:
        return ":eight:"


@functools.total_ordering
class Nine(CardBase):
    def chain(self) -> list[int]:
        return [2]
    
    def show_face_up(self) -> str:
        return ":nine:"


@functools.total_ordering
class Ten(CardBase):
    def chain(self) -> list[int]:
        return [3]
    
    def show_face_up(self) -> str:
        return ":keycap_ten:"


@functools.total_ordering
class Eleven(CardBase):
    def chain(self) -> list[int]:
        return [4]
    
    def show_face_up(self) -> str:
        return "⏸️"


@functools.total_ordering
class Twelve(CardBase):
    def chain(self) -> list[int]:
        return [5]
    
    def show_face_up(self) -> str:
        return "🔢"

int_to_card = {
    1: One,
    2: Two,
    3: Three,
    4: Four,
    5: Five,
    6: Six,
    7: Seven,
    8: Eight,
    9: Nine,
    10: Ten,
    11: Eleven,
    12: Twelve,
}

card_to_int = {v: k for k, v in int_to_card.items()}
