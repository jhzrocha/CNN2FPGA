document.addEventListener('DOMContentLoaded', (event) => {
    const dropZone = document.getElementById('dropZone');
    const addCardButton = document.getElementById('addCardButton');
    let cardCount = 0;

    addCardButton.addEventListener('click', addCard);

    function addCard() {
        cardCount++;
        const newCard = document.createElement('div');
        newCard.id = `card${cardCount}`;
        newCard.className = 'card';
        newCard.draggable = true;
        newCard.textContent = `Arraste-me ${cardCount}`;
        newCard.style.left = `${(cardCount-1) * 250}px`;
        
        newCard.style.top = '120px'; // posição inicial para cada novo card
        newCard.addEventListener('dragstart', dragStart);
        dropZone.appendChild(newCard);
    }

    function dragStart(e) {
        e.dataTransfer.setData('text/plain', null); // Required for Firefox
        const rect = e.target.getBoundingClientRect();
        e.dataTransfer.setData('offsetX', e.clientX - rect.left);
        e.dataTransfer.setData('offsetY', e.clientY - rect.top);
    }

    function dragOver(e) {
        e.preventDefault(); // Necessary to allow drop
    }

    function drop(e) {
        e.preventDefault();
        const offsetY = e.dataTransfer.getData('offsetY');
        const card = document.querySelector('.card.dragging');
        if (card) {
            card.style.top = `${e.clientY - offsetY}px`;
        }
    }

    dropZone.addEventListener('dragover', dragOver);
    dropZone.addEventListener('drop', drop);

    dropZone.addEventListener('dragstart', (e) => {
        if (e.target.classList.contains('card')) {
            e.target.classList.add('dragging');
        }
    });

    dropZone.addEventListener('dragend', (e) => {
        if (e.target.classList.contains('card')) {
            e.target.classList.remove('dragging');
        }
    });

    
});
