const API_BASE_URL = 'http://localhost:5000/api';

let currentGameState = null;
let selectedCard = null;

const cardSymbols = {
    'hearts': '♥',
    'diamonds': '♦',
    'clubs': '♣',
    'spades': '♠'
};

const cardValues = {
    1: 'A',
    11: 'J',
    12: 'Q',
    13: 'K'
};

document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    showMessage('Bienvenido al Solitario. Haz clic en "Nuevo Juego" para comenzar.', 'info');
});

function initializeEventListeners() {
    document.getElementById('new-game-btn').addEventListener('click', startNewGame);
    document.getElementById('save-game-btn').addEventListener('click', saveGame);
    document.getElementById('load-game-btn').addEventListener('click', showLoadGameModal);
    document.getElementById('stats-btn').addEventListener('click', showStatistics);

    document.getElementById('stock').addEventListener('click', drawFromStock);

    document.querySelector('.close').addEventListener('click', closeModal);

    window.addEventListener('click', (event) => {
        const modal = document.getElementById('modal');
        if (event.target === modal) {
            closeModal();
        }
    });
}

async function startNewGame() {
    try {
        const response = await fetch(`${API_BASE_URL}/new_game`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                game_id: `game_${Date.now()}`
            })
        });

        const result = await response.json();

        if (result.success) {
            currentGameState = result.data;
            renderGame(currentGameState);
            showMessage('¡Nuevo juego iniciado! Buena suerte.', 'success');
        } else {
            showMessage(`Error: ${result.message}`, 'error');
        }
    } catch (error) {
        showMessage(`Error de conexión: ${error.message}`, 'error');
        console.error('Error:', error);
    }
}

async function drawFromStock() {
    if (!currentGameState) {
        showMessage('Inicia un nuevo juego primero.', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/draw_card`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        if (result.success) {
            currentGameState = result.state;
            renderGame(currentGameState);
        } else {
            showMessage(result.message, 'error');
        }
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
        console.error('Error:', error);
    }
}

async function moveCard(fromLocation, toLocation, cardIndex = -1) {
    try {
        const response = await fetch(`${API_BASE_URL}/move_card`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                from_location: fromLocation,
                to_location: toLocation,
                card_index: cardIndex
            })
        });

        const result = await response.json();

        if (result.success) {
            currentGameState = result.state;
            renderGame(currentGameState);

            if (currentGameState.game_won) {
                setTimeout(() => {
                    showWinModal();
                }, 500);
            }
        } else {
            showMessage(result.message, 'warning');
        }
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
        console.error('Error:', error);
    }
}

async function saveGame() {
    if (!currentGameState) {
        showMessage('No hay un juego activo para guardar.', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/save_game`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                game_id: currentGameState.game_id
            })
        });

        const result = await response.json();

        if (result.success) {
            showMessage('Partida guardada exitosamente.', 'success');
        } else {
            showMessage(`Error al guardar: ${result.message}`, 'error');
        }
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
        console.error('Error:', error);
    }
}

async function showLoadGameModal() {
    try {
        const response = await fetch(`${API_BASE_URL}/list_games`);
        const result = await response.json();

        if (result.success && result.data.length > 0) {
            const games = result.data;

            const gameListHTML = `
                <ul class="game-list">
                    ${games.map(game => `
                        <li onclick="loadGame('${game.game_id}')">
                            <div class="game-info-modal">
                                <strong>ID: ${game.game_id}</strong>
                                <span>Movimientos: ${game.moves_count}</span>
                                <span>Estado: ${game.game_won ? '✅ Ganado' : '🎮 En progreso'}</span>
                                <span>Guardado: ${new Date(game.saved_at).toLocaleString()}</span>
                            </div>
                            <button class="delete-btn" onclick="event.stopPropagation(); deleteGame('${game.game_id}')">Eliminar</button>
                        </li>
                    `).join('')}
                </ul>
            `;

            showModal('Cargar Partida', gameListHTML);
        } else {
            showMessage('No hay partidas guardadas.', 'info');
        }
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
        console.error('Error:', error);
    }
}

async function loadGame(gameId) {
    try {
        const response = await fetch(`${API_BASE_URL}/load_game/${gameId}`);
        const result = await response.json();

        if (result.success) {
            currentGameState = result.data;
            renderGame(currentGameState);
            closeModal();
            showMessage('Partida cargada exitosamente.', 'success');
        } else {
            showMessage(`Error al cargar: ${result.message}`, 'error');
        }
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
        console.error('Error:', error);
    }
}

async function deleteGame(gameId) {
    if (!confirm('¿Estás seguro de eliminar esta partida?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/delete_game/${gameId}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (result.success) {
            showMessage('Partida eliminada.', 'success');
            showLoadGameModal();
        } else {
            showMessage(`Error: ${result.message}`, 'error');
        }
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
        console.error('Error:', error);
    }
}

async function showStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/statistics`);
        const result = await response.json();

        if (result.success) {
            const stats = result.data;

            const statsHTML = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-value">${stats.total_games}</span>
                        <span class="stat-label">Total de Partidas</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">${stats.won_games}</span>
                        <span class="stat-label">Partidas Ganadas</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">${stats.win_rate.toFixed(1)}%</span>
                        <span class="stat-label">Tasa de Victoria</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-value">${stats.average_moves}</span>
                        <span class="stat-label">Promedio de Movimientos</span>
                    </div>
                </div>
            `;

            showModal('Estadísticas', statsHTML);
        } else {
            showMessage('No hay estadísticas disponibles.', 'info');
        }
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
        console.error('Error:', error);
    }
}

function renderGame(gameState) {
    updateGameInfo(gameState);

    renderTableau(gameState.tableau);

    renderFoundations(gameState.foundations);

    renderWaste(gameState.waste);

    updateStock(gameState.stock_count);
}

function updateGameInfo(gameState) {
    document.getElementById('moves-count').textContent = gameState.moves_count;

    const statusElement = document.getElementById('game-status');
    if (gameState.game_won) {
        statusElement.textContent = '🎉 ¡Ganado!';
        statusElement.style.color = '#28a745';
    } else {
        statusElement.textContent = '🎮 En juego';
        statusElement.style.color = '#1e3c72';
    }
}

function renderTableau(tableau) {
    tableau.forEach((pile, colIndex) => {
        const column = document.getElementById(`tableau-${colIndex}`);
        column.innerHTML = '';

        pile.forEach((card, cardIndex) => {
            const cardElement = createCardElement(card, `tableau_${colIndex}`, cardIndex);
            cardElement.style.top = `${cardIndex * 30}px`;
            column.appendChild(cardElement);
        });
    });
}

function renderFoundations(foundations) {
    Object.keys(foundations).forEach(suit => {
        const foundationPile = document.getElementById(`foundation-${suit}`);
        foundationPile.innerHTML = `<div class="foundation-placeholder">${cardSymbols[suit]}</div>`;

        const pile = foundations[suit];
        if (pile.length > 0) {
            const topCard = pile[pile.length - 1];
            const cardElement = createCardElement(topCard, `foundation_${suit}`, -1);
            foundationPile.appendChild(cardElement);
        }
    });
}

function renderWaste(waste) {
    const wasteElement = document.getElementById('waste');
    wasteElement.innerHTML = '';

    if (waste.length > 0) {
        const topCard = waste[waste.length - 1];
        const cardElement = createCardElement(topCard, 'waste', -1);
        wasteElement.appendChild(cardElement);
    }
}

function updateStock(stockCount) {
    const stockElement = document.getElementById('stock');

    if (stockCount > 0) {
        stockElement.innerHTML = '<div class="card-back">🂠</div>';
        stockElement.style.cursor = 'pointer';
    } else {
        stockElement.innerHTML = '<div class="foundation-placeholder">↻</div>';
        stockElement.style.cursor = 'pointer';
    }
}

function createCardElement(card, location, index) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'card';

    if (!card.face_up) {
        cardDiv.classList.add('face-down');
        return cardDiv;
    }

    const isRed = card.suit === 'hearts' || card.suit === 'diamonds';
    cardDiv.classList.add(isRed ? 'red' : 'black');

    const displayValue = cardValues[card.value] || card.value;

    cardDiv.innerHTML = `
        <div class="card-value">${displayValue}</div>
        <div class="card-suit">${cardSymbols[card.suit]}</div>
    `;

    cardDiv.addEventListener('click', () => handleCardClick(location, index, card));

    return cardDiv;
}

function handleCardClick(location, index, card) {
    if (!selectedCard) {
        selectedCard = { location, index, card };
        showMessage(`Carta seleccionada: ${getCardDisplay(card)}`, 'info');
    } else {
        moveCard(selectedCard.location, location, selectedCard.index);
        selectedCard = null;
    }
}

function getCardDisplay(card) {
    const displayValue = cardValues[card.value] || card.value;
    return `${displayValue}${cardSymbols[card.suit]}`;
}

function showWinModal() {
    const winHTML = `
        <div style="text-align: center; padding: 20px;">
            <h2 style="font-size: 3rem; margin-bottom: 20px;">🎉</h2>
            <h3 style="color: #28a745; margin-bottom: 10px;">¡Felicitaciones!</h3>
            <p style="font-size: 1.2rem;">Has ganado el juego en <strong>${currentGameState.moves_count}</strong> movimientos.</p>
            <button class="btn btn-primary" onclick="closeModal(); startNewGame();" style="margin-top: 20px;">
                Jugar de Nuevo
            </button>
        </div>
    `;
    showModal('¡Victoria!', winHTML);
}

function showModal(title, content) {
    const modal = document.getElementById('modal');
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-body').innerHTML = content;
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
}

function showMessage(message, type = 'info') {
    const messageBox = document.getElementById('message-box');
    messageBox.textContent = message;
    messageBox.className = `message-box ${type} show`;

    setTimeout(() => {
        messageBox.classList.remove('show');
    }, 3000);
}
