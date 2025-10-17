"""
Módulo main.py - Punto de entrada del juego de Solitario.
Requisito: Función main() y servidor Flask para la interfaz web.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys
from backend.game_manager import GameManager
from backend.database import Database


app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

db = Database('solitaire_games.json')

current_game = None


@app.route('/')
def index():
    """
    Ruta principal que sirve la interfaz HTML.

    Returns:
        HTML: Página principal del juego
    """
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/new_game', methods=['POST'])
def new_game():
    """
    Inicia un nuevo juego de Solitario.

    Returns:
        JSON: Estado inicial del juego
    """
    global current_game

    try:
        data = request.get_json() or {}
        game_id = data.get('game_id', 'game_1')

        current_game = GameManager(game_id=game_id)
        game_state = current_game.new_game()

        return jsonify({
            'success': True,
            'message': 'Nuevo juego iniciado',
            'data': game_state
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear el juego: {str(e)}'
        }), 500


@app.route('/api/draw_card', methods=['POST'])
def draw_card():
    """
    Extrae una carta del mazo de robo.

    Returns:
        JSON: Resultado de la operación
    """
    global current_game

    if current_game is None:
        return jsonify({
            'success': False,
            'message': 'No hay un juego activo'
        }), 400

    try:
        result = current_game.draw_from_stock()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al extraer carta: {str(e)}'
        }), 500


@app.route('/api/move_card', methods=['POST'])
def move_card():
    """
    Mueve una o más cartas entre ubicaciones.

    Body JSON:
        from_location (str): Ubicación origen
        to_location (str): Ubicación destino
        card_index (int): Índice de la carta (opcional, default=-1)

    Returns:
        JSON: Resultado del movimiento
    """
    global current_game

    if current_game is None:
        return jsonify({
            'success': False,
            'message': 'No hay un juego activo'
        }), 400

    try:
        data = request.get_json()
        from_location = data.get('from_location')
        to_location = data.get('to_location')
        card_index = data.get('card_index', -1)

        if not from_location or not to_location:
            return jsonify({
                'success': False,
                'message': 'Faltan parámetros requeridos'
            }), 400

        result = current_game.move_card(from_location, to_location, card_index)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al mover carta: {str(e)}'
        }), 500


@app.route('/api/game_state', methods=['GET'])
def game_state():
    """
    Obtiene el estado actual del juego.

    Returns:
        JSON: Estado del juego
    """
    global current_game

    if current_game is None:
        return jsonify({
            'success': False,
            'message': 'No hay un juego activo'
        }), 400

    try:
        state = current_game.get_game_state()
        return jsonify({
            'success': True,
            'data': state
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener estado: {str(e)}'
        }), 500


@app.route('/api/save_game', methods=['POST'])
def save_game():
    """
    Guarda la partida actual en la base de datos.

    Body JSON:
        game_id (str): Identificador del juego (opcional)

    Returns:
        JSON: Resultado de la operación
    """
    global current_game

    if current_game is None:
        return jsonify({
            'success': False,
            'message': 'No hay un juego activo para guardar'
        }), 400

    try:
        data = request.get_json() or {}
        game_id = data.get('game_id', current_game.game_id)

        game_data = current_game.to_dict()
        success = db.save_game(game_id, game_data)

        if success:
            return jsonify({
                'success': True,
                'message': f'Juego guardado exitosamente: {game_id}'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Error al guardar el juego'
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al guardar: {str(e)}'
        }), 500


@app.route('/api/load_game/<game_id>', methods=['GET'])
def load_game(game_id):
    """
    Carga una partida guardada.

    Args:
        game_id (str): Identificador del juego

    Returns:
        JSON: Estado del juego cargado
    """
    global current_game

    try:
        game_data = db.load_game(game_id)

        if game_data is None:
            return jsonify({
                'success': False,
                'message': f'Juego no encontrado: {game_id}'
            }), 404

        current_game = GameManager.from_dict(game_data)

        return jsonify({
            'success': True,
            'message': 'Juego cargado exitosamente',
            'data': current_game.get_game_state()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al cargar juego: {str(e)}'
        }), 500


@app.route('/api/list_games', methods=['GET'])
def list_games():
    """
    Lista todas las partidas guardadas.

    Returns:
        JSON: Lista de partidas
    """
    try:
        games = db.list_games()
        return jsonify({
            'success': True,
            'data': games
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al listar juegos: {str(e)}'
        }), 500


@app.route('/api/delete_game/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    """
    Elimina una partida guardada.

    Args:
        game_id (str): Identificador del juego

    Returns:
        JSON: Resultado de la operación
    """
    try:
        success = db.delete_game(game_id)

        if success:
            return jsonify({
                'success': True,
                'message': f'Juego eliminado: {game_id}'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Juego no encontrado: {game_id}'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al eliminar juego: {str(e)}'
        }), 500


@app.route('/api/statistics', methods=['GET'])
def statistics():
    """
    Obtiene estadísticas de las partidas.

    Returns:
        JSON: Estadísticas generales
    """
    try:
        stats = db.get_statistics()
        return jsonify({
            'success': True,
            'data': stats
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener estadísticas: {str(e)}'
        }), 500


def main():
    """
    Función principal del programa.
    Requisito: Función main() como punto de entrada.
    """
    print("=" * 50)
    print("    SOLITARIO - Proyecto Programación III")
    print("=" * 50)
    print()
    print("Iniciando servidor Flask...")
    print()
    print("Accede al juego en: http://localhost:5000")
    print()
    print("Presiona Ctrl+C para detener el servidor")
    print("=" * 50)
    print()

    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\nServidor detenido. ¡Hasta luego!")
        sys.exit(0)


if __name__ == '__main__':
    main()
