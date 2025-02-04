import layerType from "./enum/typesEnum.js";


export class LayerConfigurationModal {
    dataHandler;
    
    init(dataHandler){
        this.dataHandler = dataHandler;
    }
    
    show(layerId){
        this.configureModal(layerId);
        let htmlModal = document.getElementById("layerSettingsModal");
        let modal = new bootstrap.Modal(htmlModal, {
            backdrop: 'static', // impede fechamento ao clicar fora
            keyboard: true,    // impede fechamento com Esc
            focus: true         // foca automaticamente no modal
        });
        modal.show();
    }

    configureModal(layerId){
        const modalTitle = document.getElementById("layerConfigurationTitle");
        const layerType = document.getElementById("layerType");

        const newModalTitle = modalTitle.cloneNode(true); // Clone the element (true for deep clone)
        modalTitle.parentNode.replaceChild(newModalTitle, modalTitle);
        
        const newLayerType= layerType.cloneNode(true); // Clone the element (true for deep clone)
        layerType.parentNode.replaceChild(newLayerType, layerType);
        
        this.loadInputValueFromLocalstorage(newModalTitle,layerId);
        this.loadInputValueFromLocalstorage(newLayerType,layerId);        
        
        this.addUpdateDatahandlerEvent(newModalTitle,layerId);

        this.updateModalLayerType(newLayerType, layerId)
    }

    loadInputValueFromLocalstorage(element, layerId){
        element.value = this.dataHandler.getLayerAttribute(layerId, element.getAttribute('attributeName'))
    }

    updateModalLayerType(newLayerType, layerId){
        this.addUpdateDatahandlerEvent(newLayerType,layerId);
        this.addUpdateFormEvent(newLayerType,layerId);

    }

    addUpdateFormEvent(newLayerType,layerId){

    }

    addUpdateDatahandlerEvent(element, layerId) {
        const attribute = element.getAttribute('attributeName');
        element.addEventListener('blur', ()=>{
            if(element.value != undefined && element.value != this.dataHandler.getLayerAttribute(layerId, attribute)){
                this.dataHandler.setLayerAttribute(layerId,attribute, element.value);
                this.updateCardInformations(layerId);
            }
        });
    }

    updateCardInformations(layerID){
        const cardTitle = document.getElementById(`title-${layerID}`);
        const cardSubtitle = document.getElementById(`subtitle-${layerID}`);
        console.log(this.dataHandler.layers);
        cardTitle.textContent = this.dataHandler.getLayerAttribute(layerID, cardTitle.getAttribute('attributeName'));
        cardSubtitle.textContent = layerType[this.dataHandler.getLayerAttribute(layerID, cardSubtitle.getAttribute('attributeName'))];
    }

    
}