document.addEventListener('DOMContentLoaded', (event) => {
    const sideMenu = document.getElementById('sideMenu');
    const closeBtn = document.querySelector('.closeBtn');
    const dropZone = document.getElementById('dropZone');
    const addCardButton = document.getElementById('addCardButton');
    const removeAllCards = document.getElementById('removeAllCards');

    let cardCount = 0;
    let addedCards = {};
    function cleanCardArea(){
        dropZone.replaceChildren();
        addedCards = {};
        cardCount = 0;
    }
    function addCard() {
        cardCount++;        
        const newCard = document.createElement('div');
        newCard.id = `card${cardCount}`;
        newCard.className = 'card';
        newCard.draggable = true;
        newCard.textContent = `Camada`;
        newCard.style.left = `${(cardCount-1) * 250}px`;
        newCard.addEventListener('dblclick', openSideMenu)
        newCard.style.top = '0px'; // posição inicial para cada novo card
        newCard.setAttribute('layerID',cardCount)
        const newRemoveCardButton = document.createElement('a')
        newRemoveCardButton.id = `removeLayerButton${cardCount}`
        newRemoveCardButton.innerText = 'X';
        newRemoveCardButton.href = "javascript:void(0)";
        newRemoveCardButton.addEventListener('click', (event)=>{
            const card = event.target.offsetParent;
            card.parentNode.removeChild(card);
            cardCount--;
            console.log(addedCards);
        })
        newCard.appendChild(newRemoveCardButton);
        addedCards[cardCount] = newCard;
        dropZone.appendChild(newCard);
    }

    closeBtn.addEventListener('click', () => {
        sideMenu.style.width = '0';
    });

    function openSideMenu(){
        sideMenu.style.width = '500px';
    }
    addCardButton.addEventListener('click', addCard);
    removeAllCards.addEventListener('click',cleanCardArea)


    
});
