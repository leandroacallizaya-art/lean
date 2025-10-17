"""
Módulo deck.py - Define la clase Deck (Mazo) con CRUD completo.
Requisito: Clase principal con 5 atributos y operaciones CRUD.
"""

import random
from collections import deque
from typing import List, Optional, Dict
from backend.card import Card


class Deck:
    """
    Clase Deck que representa un mazo de cartas.
    Requisito: Clase principal con 5 atributos (uno encapsulado).

    Atributos públicos:
        deck_id (str): Identificador único del mazo
        created_at (str): Timestamp de creación
        shuffled (bool): Indica si el mazo está mezclado
        size (int): Número de cartas en el mazo

    Atributo encapsulado:
        __cards (deque): Cola de cartas del mazo (privado)
    """

    def __init__(self, deck_id: str = "default", created_at: str = None):
        """
        Inicializa un mazo de cartas.

        Args:
            deck_id (str): Identificador del mazo
            created_at (str): Timestamp de creación
        """
        self.deck_id = deck_id
        self.created_at = created_at or self._get_timestamp()
        self.shuffled = False
        self.size = 0
        self.__cards = deque()

    def _get_timestamp(self) -> str:
        """
        Obtiene el timestamp actual.

        Returns:
            str: Timestamp en formato ISO
        """
        from datetime import datetime
        return datetime.now().isoformat()

    def initialize_standard_deck(self) -> None:
        """
        Inicializa un mazo estándar de 52 cartas.
        Crea todas las combinaciones de palos y valores.
        """
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        self.__cards.clear()

        for suit in suits:
            for value in range(1, 14):
                card = Card(suit, value)
                self.__cards.append(card)

        self.size = len(self.__cards)
        self.shuffled = False

    def shuffle(self) -> None:
        """
        Mezcla las cartas del mazo usando random.shuffle.
        Requisito: Uso del módulo random.
        """
        cards_list = list(self.__cards)
        random.shuffle(cards_list)
        self.__cards = deque(cards_list)
        self.shuffled = True

    def draw_card(self) -> Optional[Card]:
        """
        Extrae una carta del mazo.

        Returns:
            Card | None: Carta extraída o None si el mazo está vacío
        """
        if len(self.__cards) > 0:
            card = self.__cards.popleft()
            self.size = len(self.__cards)
            return card
        return None

    def add_card(self, card: Card) -> None:
        """
        Agrega una carta al final del mazo.

        Args:
            card (Card): Carta a agregar
        """
        self.__cards.append(card)
        self.size = len(self.__cards)

    def peek_top(self) -> Optional[Card]:
        """
        Muestra la carta superior sin extraerla.

        Returns:
            Card | None: Carta superior o None si está vacío
        """
        if len(self.__cards) > 0:
            return self.__cards[0]
        return None

    def is_empty(self) -> bool:
        """
        Verifica si el mazo está vacío.

        Returns:
            bool: True si está vacío, False en caso contrario
        """
        return len(self.__cards) == 0

    def get_all_cards(self) -> List[Card]:
        """
        Obtiene todas las cartas del mazo (sin modificarlo).

        Returns:
            list: Lista de cartas
        """
        return list(self.__cards)

    def create_card(self, suit: str, value: int, face_up: bool = False) -> Card:
        """
        CREATE - Crea una nueva carta y la agrega al mazo.
        Requisito: Operación CREATE del CRUD.

        Args:
            suit (str): Palo de la carta
            value (int): Valor de la carta
            face_up (bool): Si está boca arriba

        Returns:
            Card: La carta creada
        """
        card = Card(suit, value, face_up)
        self.__cards.append(card)
        self.size = len(self.__cards)
        return card

    def read_card(self, index: int) -> Optional[Card]:
        """
        READ - Lee una carta en una posición específica.
        Requisito: Operación READ del CRUD.

        Args:
            index (int): Índice de la carta

        Returns:
            Card | None: La carta en esa posición o None
        """
        if 0 <= index < len(self.__cards):
            return self.__cards[index]
        return None

    def update_card(self, index: int, suit: str = None, value: int = None,
                    face_up: bool = None) -> bool:
        """
        UPDATE - Actualiza los atributos de una carta existente.
        Requisito: Operación UPDATE del CRUD.

        Args:
            index (int): Índice de la carta
            suit (str): Nuevo palo (opcional)
            value (int): Nuevo valor (opcional)
            face_up (bool): Nuevo estado (opcional)

        Returns:
            bool: True si se actualizó, False si no existe
        """
        if 0 <= index < len(self.__cards):
            card = self.__cards[index]

            if suit is not None:
                card.suit = suit
            if value is not None:
                card.value = value
            if face_up is not None:
                card.face_up = face_up

            return True
        return False

    def delete_card(self, index: int) -> Optional[Card]:
        """
        DELETE - Elimina una carta en una posición específica.
        Requisito: Operación DELETE del CRUD.

        Args:
            index (int): Índice de la carta a eliminar

        Returns:
            Card | None: La carta eliminada o None si no existe
        """
        if 0 <= index < len(self.__cards):
            cards_list = list(self.__cards)
            removed_card = cards_list.pop(index)
            self.__cards = deque(cards_list)
            self.size = len(self.__cards)
            return removed_card
        return None

    def to_dict(self) -> Dict:
        """
        Convierte el mazo a diccionario para serialización.
        Requisito: Soporte para guardado en JSON.

        Returns:
            dict: Representación del mazo
        """
        return {
            'deck_id': self.deck_id,
            'created_at': self.created_at,
            'shuffled': self.shuffled,
            'size': self.size,
            'cards': [card.to_dict() for card in self.__cards]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Deck':
        """
        Crea un mazo desde un diccionario.

        Args:
            data (dict): Diccionario con los datos del mazo

        Returns:
            Deck: Nueva instancia de mazo
        """
        deck = cls(
            deck_id=data.get('deck_id', 'default'),
            created_at=data.get('created_at')
        )
        deck.shuffled = data.get('shuffled', False)
        deck.size = data.get('size', 0)

        cards_data = data.get('cards', [])
        for card_data in cards_data:
            card = Card.from_dict(card_data)
            deck.__cards.append(card)

        return deck

    def __len__(self) -> int:
        """
        Polimorfismo: Sobrecarga del operador len().

        Returns:
            int: Número de cartas en el mazo
        """
        return len(self.__cards)

    def __str__(self) -> str:
        """
        Representación en string del mazo.

        Returns:
            str: Descripción del mazo
        """
        return f"Deck(id={self.deck_id}, cards={self.size}, shuffled={self.shuffled})"

    def __repr__(self) -> str:
        """
        Representación para debugging.

        Returns:
            str: Representación detallada
        """
        return f"Deck(deck_id='{self.deck_id}', size={self.size}, shuffled={self.shuffled})"
