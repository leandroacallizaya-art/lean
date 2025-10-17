"""
Módulo game_manager.py - Gestiona la lógica principal del juego de Solitario.
Requisito: Relación de uso entre clases (usa Deck y Card).
"""

from typing import List, Dict, Optional
from collections import deque
from backend.deck import Deck
from backend.card import Card
import re


class GameManager:
    """
    Clase GameManager que gestiona el estado y lógica del juego de Solitario (Klondike).

    Estructura del juego:
    - 7 columnas (tableau)
    - 4 fundaciones (foundations) - una por palo
    - 1 mazo de robo (stock)
    - 1 pila de descarte (waste)

    Atributos:
        game_id (str): Identificador único del juego
        deck (Deck): Mazo principal (relación de uso)
        tableau (list): 7 pilas de cartas en juego
        foundations (dict): 4 pilas de cartas ordenadas por palo
        stock (deque): Mazo de robo
        waste (deque): Pila de descarte
        moves_count (int): Contador de movimientos
        game_won (bool): Indica si el juego fue ganado
    """

    def __init__(self, game_id: str = "game_1"):
        """
        Inicializa un nuevo juego de Solitario.

        Args:
            game_id (str): Identificador del juego
        """
        self.game_id = game_id
        self.deck = Deck(deck_id=f"deck_{game_id}")
        self.tableau = [[] for _ in range(7)]
        self.foundations = {
            'hearts': [],
            'diamonds': [],
            'clubs': [],
            'spades': []
        }
        self.stock = deque()
        self.waste = deque()
        self.moves_count = 0
        self.game_won = False

    def new_game(self) -> Dict:
        """
        Inicia un nuevo juego de Solitario.
        Mezcla el mazo y reparte las cartas.

        Returns:
            dict: Estado inicial del juego
        """
        self.deck.initialize_standard_deck()
        self.deck.shuffle()

        self.tableau = [[] for _ in range(7)]
        self.foundations = {
            'hearts': [],
            'diamonds': [],
            'clubs': [],
            'spades': []
        }
        self.stock = deque()
        self.waste = deque()
        self.moves_count = 0
        self.game_won = False

        for col in range(7):
            for row in range(col + 1):
                card = self.deck.draw_card()
                if card:
                    if row == col:
                        card.face_up = True
                    self.tableau[col].append(card)

        while not self.deck.is_empty():
            card = self.deck.draw_card()
            if card:
                self.stock.append(card)

        return self.get_game_state()

    def draw_from_stock(self) -> Dict:
        """
        Extrae una carta del mazo de robo y la coloca en el descarte.

        Returns:
            dict: Resultado de la operación
        """
        if len(self.stock) > 0:
            card = self.stock.popleft()
            card.face_up = True
            self.waste.append(card)
            self.moves_count += 1
            return {
                'success': True,
                'message': 'Carta extraída del mazo',
                'state': self.get_game_state()
            }
        else:
            while len(self.waste) > 0:
                card = self.waste.pop()
                card.face_up = False
                self.stock.append(card)

            return {
                'success': True,
                'message': 'Mazo reiniciado',
                'state': self.get_game_state()
            }

    def move_card(self, from_location: str, to_location: str,
                  card_index: int = -1) -> Dict:
        """
        Mueve una o más cartas entre ubicaciones.
        Requisito: Uso del módulo re para validar formato de ubicación.

        Args:
            from_location (str): Ubicación origen (ej: 'tableau_0', 'waste', 'foundation_hearts')
            to_location (str): Ubicación destino
            card_index (int): Índice de la carta a mover (-1 = última carta)

        Returns:
            dict: Resultado de la operación
        """
        pattern = r'^(tableau_\d|foundation_\w+|waste|stock)$'
        if not re.match(pattern, from_location) or not re.match(pattern, to_location):
            return {
                'success': False,
                'message': 'Formato de ubicación inválido',
                'state': self.get_game_state()
            }

        from_pile = self._get_pile(from_location)
        to_pile = self._get_pile(to_location)

        if from_pile is None or to_pile is None:
            return {
                'success': False,
                'message': 'Ubicación no encontrada',
                'state': self.get_game_state()
            }

        if len(from_pile) == 0:
            return {
                'success': False,
                'message': 'No hay cartas en la ubicación origen',
                'state': self.get_game_state()
            }

        if card_index == -1:
            card_index = len(from_pile) - 1

        if card_index < 0 or card_index >= len(from_pile):
            return {
                'success': False,
                'message': 'Índice de carta inválido',
                'state': self.get_game_state()
            }

        card = from_pile[card_index]

        if not card.face_up and card_index != len(from_pile) - 1:
            return {
                'success': False,
                'message': 'No puedes mover cartas boca abajo',
                'state': self.get_game_state()
            }

        if 'foundation' in to_location:
            if not self._can_move_to_foundation(card, to_location):
                return {
                    'success': False,
                    'message': 'Movimiento no válido a la fundación',
                    'state': self.get_game_state()
                }

            cards_to_move = [from_pile.pop(card_index)]
        else:
            if not self._can_move_to_tableau(from_pile, card_index, to_pile):
                return {
                    'success': False,
                    'message': 'Movimiento no válido al tableau',
                    'state': self.get_game_state()
                }

            cards_to_move = from_pile[card_index:]
            del from_pile[card_index:]

        for card in cards_to_move:
            to_pile.append(card)

        if len(from_pile) > 0 and not from_pile[-1].face_up:
            from_pile[-1].face_up = True

        self.moves_count += 1

        self._check_win_condition()

        return {
            'success': True,
            'message': 'Movimiento exitoso',
            'state': self.get_game_state()
        }

    def _get_pile(self, location: str):
        """
        Obtiene la pila correspondiente a una ubicación.

        Args:
            location (str): Ubicación de la pila

        Returns:
            list | deque | None: La pila o None si no existe
        """
        if location.startswith('tableau_'):
            index = int(location.split('_')[1])
            if 0 <= index < 7:
                return self.tableau[index]

        elif location.startswith('foundation_'):
            suit = location.split('_')[1]
            if suit in self.foundations:
                return self.foundations[suit]

        elif location == 'waste':
            return list(self.waste)

        elif location == 'stock':
            return list(self.stock)

        return None

    def _can_move_to_foundation(self, card: Card, foundation_location: str) -> bool:
        """
        Verifica si una carta puede moverse a una fundación.

        Args:
            card (Card): Carta a mover
            foundation_location (str): Ubicación de la fundación

        Returns:
            bool: True si es válido
        """
        suit = foundation_location.split('_')[1]

        if card.suit != suit:
            return False

        foundation = self.foundations[suit]

        if len(foundation) == 0:
            return card.value == 1

        return card.value == foundation[-1].value + 1

    def _can_move_to_tableau(self, from_pile: List[Card], card_index: int,
                             to_pile: List[Card]) -> bool:
        """
        Verifica si una o más cartas pueden moverse a una columna del tableau.

        Args:
            from_pile (list): Pila origen
            card_index (int): Índice de la carta
            to_pile (list): Pila destino

        Returns:
            bool: True si es válido
        """
        card = from_pile[card_index]

        if len(to_pile) == 0:
            return card.value == 13

        top_card = to_pile[-1]
        return card.can_place_on(top_card)

    def _check_win_condition(self) -> None:
        """
        Verifica si el jugador ha ganado el juego.
        Gana cuando todas las cartas están en las fundaciones.
        """
        total_cards = sum(len(foundation) for foundation in self.foundations.values())
        if total_cards == 52:
            self.game_won = True

    def get_game_state(self) -> Dict:
        """
        Obtiene el estado completo del juego.

        Returns:
            dict: Estado del juego
        """
        return {
            'game_id': self.game_id,
            'tableau': [
                [card.to_dict() for card in pile]
                for pile in self.tableau
            ],
            'foundations': {
                suit: [card.to_dict() for card in pile]
                for suit, pile in self.foundations.items()
            },
            'stock_count': len(self.stock),
            'waste': [card.to_dict() for card in self.waste] if self.waste else [],
            'moves_count': self.moves_count,
            'game_won': self.game_won
        }

    def to_dict(self) -> Dict:
        """
        Convierte el juego completo a diccionario para guardar.

        Returns:
            dict: Representación completa del juego
        """
        return {
            'game_id': self.game_id,
            'deck': self.deck.to_dict(),
            'tableau': [
                [card.to_dict() for card in pile]
                for pile in self.tableau
            ],
            'foundations': {
                suit: [card.to_dict() for card in pile]
                for suit, pile in self.foundations.items()
            },
            'stock': [card.to_dict() for card in self.stock],
            'waste': [card.to_dict() for card in self.waste],
            'moves_count': self.moves_count,
            'game_won': self.game_won
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'GameManager':
        """
        Reconstruye un juego desde un diccionario.

        Args:
            data (dict): Datos del juego

        Returns:
            GameManager: Instancia del juego
        """
        game = cls(game_id=data.get('game_id', 'game_1'))

        if 'deck' in data:
            game.deck = Deck.from_dict(data['deck'])

        game.tableau = [
            [Card.from_dict(card_data) for card_data in pile]
            for pile in data.get('tableau', [[] for _ in range(7)])
        ]

        game.foundations = {
            suit: [Card.from_dict(card_data) for card_data in pile]
            for suit, pile in data.get('foundations', {}).items()
        }

        game.stock = deque(
            Card.from_dict(card_data) for card_data in data.get('stock', [])
        )

        game.waste = deque(
            Card.from_dict(card_data) for card_data in data.get('waste', [])
        )

        game.moves_count = data.get('moves_count', 0)
        game.game_won = data.get('game_won', False)

        return game

    def __str__(self) -> str:
        """
        Representación en string del juego.

        Returns:
            str: Descripción del juego
        """
        return f"GameManager(id={self.game_id}, moves={self.moves_count}, won={self.game_won})"
