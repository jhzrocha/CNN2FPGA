import { LayerConfigurationModal } from "./layerConfigurationModal.js";

export class LayersCards {
    dropZone = document.getElementById('dropZone');
    cardCount = 0;
    addCardButton = document.getElementById('addCardButton');
    dataHandler;
    layerConfigurationModal;


    initCards(dataHandler) {
        this.dataHandler = dataHandler;
        this.layerConfigurationModal = new LayerConfigurationModal();
        this.layerConfigurationModal.init(dataHandler);
        this.addCard();
        this.addEventOnAddLayerButton();
    }

    addEventOnAddLayerButton(){
        this.addCardButton.addEventListener('click', (event) => {
            event.preventDefault(); // Impede o recarregamento da página
            this.addCard();
        });
    }

    addOpenModalEvent(element){
        element.addEventListener("dblclick", () => {
            this.openConfigurationModal(element.id)
        });            
    }

    openConfigurationModal(layerId){
        this.layerConfigurationModal.show(layerId);
    }

    addCard() {
        this.cardCount++;
        const newCard = document.createElement('div');
        const layerTitle = document.createElement('div');
        const layerSubtitle = document.createElement('div');
        
        newCard.id = `layer${this.cardCount}`;
        newCard.className = 'camada-naoConfigurada';
        newCard.draggable = true;
        
        layerTitle.textContent = `Camada`;
        layerTitle.className = 'camada-title';
        layerTitle.id = `title-layer${this.cardCount}`;
        layerTitle.setAttribute('attributeName','name');

        layerSubtitle.textContent = 'Clique Duplo para Editar';
        layerSubtitle.className = 'camada-subtitle';
        layerSubtitle.id = `subtitle-layer${this.cardCount}`;
        layerSubtitle.setAttribute('attributeName','type');
    
        newCard.style.left = `${(this.cardCount - 1) * 250}px`;
        newCard.style.top = '120px'; // posição inicial para cada novo card
        newCard.addEventListener('dragstart', (e) => this.dragStart(e));
    
        this.addCloseButton(newCard); // Agora `this.addCloseButton` será chamado corretamente
        newCard.appendChild(layerTitle);
        newCard.appendChild(layerSubtitle);
    
        this.addOpenModalEvent(newCard);
        this.dropZone.removeChild(this.addCardButton);
        this.dropZone.appendChild(newCard);
        this.dropZone.appendChild(this.addCardButton);
        this.dataHandler.addLayer(this.cardCount);
    }

    addCloseButton(newCard) {
        const closeButton = document.createElement('div');
        const closeButtonContainer = document.createElement('div');
    
        closeButton.textContent = 'X';
        closeButton.className = 'close-button';
        closeButton.id = `layer${this.cardCount}`;
        closeButton.style.cursor = 'pointer'; // Mostra o cursor de pointer no X
        closeButton.addEventListener('click', (event) => {
            event.stopPropagation(); // Impede que o clique no "X" afete o card
            this.dataHandler.removeLayer(event.currentTarget.id);
            newCard.remove();            
            this.cardCount--; // Agora `this.cardCount` é usado corretamente
        });
    
        // Estilização para alinhar o botão à direita
        closeButtonContainer.className = 'close-button-container';
        closeButtonContainer.style.display = 'flex';
        closeButtonContainer.style.justifyContent = 'flex-end'; // Alinha o "X" à direita
        closeButtonContainer.append(closeButton);
    
        newCard.prepend(closeButtonContainer); // Adiciona o container no topo do card
    }
    
    dragStart(e) {
        const rect = e.target.getBoundingClientRect();
        e.dataTransfer.setData('offsetX', e.clientX - rect.left);
        e.dataTransfer.setData('offsetY', e.clientY - rect.top);
    }

    dragOver(e) {
        e.preventDefault(); // Necessário para permitir o drop
    }

    drop(e) {
        e.preventDefault();
        const offsetY = e.dataTransfer.getData('offsetY');
        const card = document.querySelector('.card.dragging');
        if (card) {
            card.style.top = `${e.clientY - offsetY}px`;
        }
    }

    abreModal() {
        $("#myModal").modal({
            show: true
        });
    }
}
