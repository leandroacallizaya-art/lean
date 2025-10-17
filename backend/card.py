"""
Módulo card.py - Define la clase Card que representa una carta del juego.
Cumple con el requisito de herencia de clase abstracta.
"""

from abc import ABC, abstractmethod
from typing import Optional


class AbstractCard(ABC):
    """
    Clase abstracta que define el comportamiento básico de una carta.
    Requisito: Herencia de clase abstracta.
    """

    @abstractmethod
    def get_value(self) -> int:
        """Obtiene el valor numérico de la carta."""
        pass

    @abstractmethod
    def get_suit(self) -> str:
        """Obtiene el palo de la carta."""
        pass

    @abstractmethod
    def is_red(self) -> bool:
        """Determina si la carta es roja."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Convierte la carta a diccionario para serialización."""
        pass


class Card(AbstractCard):
    """
    Clase Card que representa una carta del mazo.
    Hereda de AbstractCard (clase abstracta).

    Atributos:
        suit (str): Palo de la carta (hearts, diamonds, clubs, spades)
        value (int): Valor numérico (1-13, donde 1=As, 11=J, 12=Q, 13=K)
        face_up (bool): Indica si la carta está boca arriba
    """

    SUITS = {
        'hearts': '♥',
        'diamonds': '♦',
        'clubs': '♣',
        'spades': '♠'
    }

    VALUES = {
        1: 'A',
        11: 'J',
        12: 'Q',
        13: 'K'
    }

    def __init__(self, suit: str, value: int, face_up: bool = False):
        """
        Inicializa una carta.

        Args:
            suit (str): Palo de la carta
            value (int): Valor numérico (1-13)
            face_up (bool): Si la carta está visible
        """
        if suit not in self.SUITS:
            raise ValueError(f"Palo inválido: {suit}")
        if value < 1 or value > 13:
            raise ValueError(f"Valor inválido: {value}")

        self.suit = suit
        self.value = value
        self.face_up = face_up

    def get_value(self) -> int:
        """
        Obtiene el valor numérico de la carta.
        Implementación del método abstracto.

        Returns:
            int: Valor de la carta (1-13)
        """
        return self.value

    def get_suit(self) -> str:
        """
        Obtiene el palo de la carta.
        Implementación del método abstracto.

        Returns:
            str: Palo de la carta
        """
        return self.suit

    def is_red(self) -> bool:
        """
        Determina si la carta es roja (corazones o diamantes).
        Implementación del método abstracto.

        Returns:
            bool: True si es roja, False si es negra
        """
        return self.suit in ['hearts', 'diamonds']

    def flip(self) -> None:
        """Voltea la carta (cambia entre boca arriba y boca abajo)."""
        self.face_up = not self.face_up

    def can_place_on(self, other: Optional['Card']) -> bool:
        """
        Verifica si esta carta puede colocarse sobre otra según las reglas del Solitario.

        Args:
            other (Card | None): Carta sobre la que se quiere colocar

        Returns:
            bool: True si se puede colocar, False en caso contrario
        """
        if other is None:
            return self.value == 13

        return (self.value == other.value - 1 and
                self.is_red() != other.is_red())

    def to_dict(self) -> dict:
        """
        Convierte la carta a un diccionario para serialización JSON.
        Implementación del método abstracto.

        Returns:
            dict: Representación de la carta
        """
        return {
            'suit': self.suit,
            'value': self.value,
            'face_up': self.face_up
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Card':
        """
        Crea una carta desde un diccionario.

        Args:
            data (dict): Diccionario con los datos de la carta

        Returns:
            Card: Nueva instancia de carta
        """
        return cls(
            suit=data['suit'],
            value=data['value'],
            face_up=data.get('face_up', False)
        )

    def get_display_value(self) -> str:
        """
        Obtiene el valor de la carta para mostrar (A, 2-10, J, Q, K).

        Returns:
            str: Representación del valor
        """
        if self.value in self.VALUES:
            return self.VALUES[self.value]
        return str(self.value)

    def get_symbol(self) -> str:
        """
        Obtiene el símbolo del palo de la carta.

        Returns:
            str: Símbolo unicode del palo
        """
        return self.SUITS[self.suit]

    def __str__(self) -> str:
        """
        Representación en string de la carta.

        Returns:
            str: Carta en formato legible
        """
        if not self.face_up:
            return "[???]"
        return f"{self.get_display_value()}{self.get_symbol()}"

    def __repr__(self) -> str:
        """
        Representación para debugging.

        Returns:
            str: Representación detallada
        """
        return f"Card({self.suit}, {self.value}, face_up={self.face_up})"

    def __eq__(self, other) -> bool:
        """
        Compara dos cartas por igualdad.
        Polimorfismo: sobrecarga del operador ==

        Args:
            other: Otra carta

        Returns:
            bool: True si son iguales
        """
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.value == other.value
