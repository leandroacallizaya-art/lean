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
    initializeEmptyPiles();
    showMessage('Bienvenido al Solitario. Haz clic en "Nueva Partida" para comenzar.', 'info');
});

function initializeEventListeners() {
    document.getElementById('new-game-btn').addEventListener('click', startNewGame);

    document.getElementById('stock').addEventListener('click', drawFromStock);

    document.querySelector('.close').addEventListener('click', closeModal);

    window.addEventListener('click', (event) => {
        const modal = document.getElementById('modal');
        if (event.target === modal) {
            closeModal();
        }
    });
}

function initializeEmptyPiles() {
    const stockElement = document.getElementById('stock');
    stockElement.innerHTML = '<div class="card-back">20</div>';
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

function renderGame(gameState) {
    updateGameInfo(gameState);

    renderTableau(gameState.tableau);

    renderFoundations(gameState.foundations);

    renderWaste(gameState.waste);

    updateStock(gameState.stock_count);
}

function updateGameInfo(gameState) {
    document.getElementById('moves-count').textContent = gameState.moves_count;

    const score = calculateScore(gameState);
    document.getElementById('score-count').textContent = score;
}

function calculateScore(gameState) {
    let score = 0;

    Object.values(gameState.foundations).forEach(foundation => {
        score += foundation.length;
    });

    return score;
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
        stockElement.innerHTML = `<div class="card-back">${stockCount}</div>`;
        stockElement.style.cursor = 'pointer';
    } else {
        stockElement.innerHTML = '<div class="card-back" style="background: rgba(124, 58, 237, 0.3); color: #7c3aed;">↻</div>';
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
        <div class="card-top">
            <div class="card-value">${displayValue}</div>
            <div class="card-suit">${cardSymbols[card.suit]}</div>
        </div>
        <div class="card-bottom">
            <div class="card-value">${displayValue}</div>
            <div class="card-suit">${cardSymbols[card.suit]}</div>
        </div>
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
