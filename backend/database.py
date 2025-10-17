"""
Módulo database.py - Simula una base de datos usando archivos JSON.
Requisito: Uso del módulo json para persistencia de datos.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class Database:
    """
    Clase Database que simula una base de datos usando JSON.
    Requisito: Uso del módulo json.

    Permite guardar y cargar partidas del juego de Solitario.

    Atributos:
        db_path (str): Ruta al archivo JSON de la base de datos
        data (dict): Datos en memoria
    """

    def __init__(self, db_path: str = "solitaire_games.json"):
        """
        Inicializa la base de datos.

        Args:
            db_path (str): Ruta al archivo de base de datos
        """
        self.db_path = db_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """
        Carga los datos desde el archivo JSON.

        Returns:
            dict: Datos cargados o estructura vacía
        """
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar la base de datos: {e}")
                return self._get_empty_structure()
        return self._get_empty_structure()

    def _get_empty_structure(self) -> Dict:
        """
        Retorna la estructura vacía de la base de datos.

        Returns:
            dict: Estructura base
        """
        return {
            'games': {},
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'last_modified': datetime.now().isoformat(),
                'total_games': 0
            }
        }

    def _save_data(self) -> bool:
        """
        Guarda los datos en el archivo JSON.

        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            self.data['metadata']['last_modified'] = datetime.now().isoformat()

            with open(self.db_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error al guardar la base de datos: {e}")
            return False

    def save_game(self, game_id: str, game_data: Dict) -> bool:
        """
        Guarda una partida en la base de datos.

        Args:
            game_id (str): Identificador único del juego
            game_data (dict): Datos del juego

        Returns:
            bool: True si se guardó exitosamente
        """
        game_data['saved_at'] = datetime.now().isoformat()

        self.data['games'][game_id] = game_data

        if game_id not in self.data['games']:
            self.data['metadata']['total_games'] += 1

        return self._save_data()

    def load_game(self, game_id: str) -> Optional[Dict]:
        """
        Carga una partida específica.

        Args:
            game_id (str): Identificador del juego

        Returns:
            dict | None: Datos del juego o None si no existe
        """
        return self.data['games'].get(game_id)

    def list_games(self) -> List[Dict]:
        """
        Lista todas las partidas guardadas.

        Returns:
            list: Lista de partidas con información básica
        """
        games_list = []

        for game_id, game_data in self.data['games'].items():
            games_list.append({
                'game_id': game_id,
                'moves_count': game_data.get('moves_count', 0),
                'game_won': game_data.get('game_won', False),
                'saved_at': game_data.get('saved_at', 'Unknown')
            })

        games_list.sort(key=lambda x: x['saved_at'], reverse=True)

        return games_list

    def delete_game(self, game_id: str) -> bool:
        """
        Elimina una partida de la base de datos.

        Args:
            game_id (str): Identificador del juego

        Returns:
            bool: True si se eliminó exitosamente
        """
        if game_id in self.data['games']:
            del self.data['games'][game_id]
            self.data['metadata']['total_games'] -= 1
            return self._save_data()
        return False

    def game_exists(self, game_id: str) -> bool:
        """
        Verifica si una partida existe.

        Args:
            game_id (str): Identificador del juego

        Returns:
            bool: True si existe
        """
        return game_id in self.data['games']

    def get_statistics(self) -> Dict:
        """
        Obtiene estadísticas generales de las partidas.

        Returns:
            dict: Estadísticas
        """
        total_games = len(self.data['games'])
        won_games = sum(
            1 for game in self.data['games'].values()
            if game.get('game_won', False)
        )

        total_moves = sum(
            game.get('moves_count', 0)
            for game in self.data['games'].values()
        )

        avg_moves = total_moves / total_games if total_games > 0 else 0

        return {
            'total_games': total_games,
            'won_games': won_games,
            'lost_games': total_games - won_games,
            'win_rate': (won_games / total_games * 100) if total_games > 0 else 0,
            'total_moves': total_moves,
            'average_moves': round(avg_moves, 2)
        }

    def clear_all_games(self) -> bool:
        """
        Elimina todas las partidas (usar con precaución).

        Returns:
            bool: True si se eliminaron exitosamente
        """
        self.data['games'] = {}
        self.data['metadata']['total_games'] = 0
        return self._save_data()

    def export_game(self, game_id: str, export_path: str) -> bool:
        """
        Exporta una partida específica a un archivo JSON separado.

        Args:
            game_id (str): Identificador del juego
            export_path (str): Ruta donde exportar

        Returns:
            bool: True si se exportó exitosamente
        """
        game_data = self.load_game(game_id)

        if game_data is None:
            return False

        try:
            with open(export_path, 'w', encoding='utf-8') as file:
                json.dump(game_data, file, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error al exportar el juego: {e}")
            return False

    def import_game(self, import_path: str, game_id: str = None) -> Optional[str]:
        """
        Importa una partida desde un archivo JSON.

        Args:
            import_path (str): Ruta del archivo a importar
            game_id (str): ID opcional para la partida

        Returns:
            str | None: ID del juego importado o None si falló
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as file:
                game_data = json.load(file)

            if game_id is None:
                game_id = game_data.get('game_id', f"imported_{datetime.now().timestamp()}")

            self.save_game(game_id, game_data)
            return game_id

        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al importar el juego: {e}")
            return None

    def backup_database(self, backup_path: str) -> bool:
        """
        Crea una copia de seguridad de la base de datos completa.

        Args:
            backup_path (str): Ruta donde guardar el backup

        Returns:
            bool: True si se creó exitosamente
        """
        try:
            with open(backup_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error al crear backup: {e}")
            return False

    def __str__(self) -> str:
        """
        Representación en string de la base de datos.

        Returns:
            str: Descripción
        """
        return f"Database(path={self.db_path}, games={len(self.data['games'])})"

    def __repr__(self) -> str:
        """
        Representación para debugging.

        Returns:
            str: Representación detallada
        """
        return f"Database(db_path='{self.db_path}', total_games={len(self.data['games'])})"
