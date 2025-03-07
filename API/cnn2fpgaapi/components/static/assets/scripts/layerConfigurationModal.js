import layerType from "./enum/typesEnum.js";
import convolutionalFormInputsEnum from "./enum/convolutionalFormInputsEnum.js";
import poolingFormInputsEnum from "./enum/poolingFormInputsEnum.js";
import fullyConnectedFormInputsEnum from "./enum/fullyConnectedFormInputsEnum.js";

export class LayerConfigurationModal {
    dataHandler;
    layerType;
    layerId;
    
    init(dataHandler){
        this.dataHandler = dataHandler;
    }
    
    show(layerId){
        let htmlModal = document.getElementById("layerSettingsModal");
        this.configureModal(layerId);
        let modal = new bootstrap.Modal(htmlModal, {
            backdrop: 'static', 
            keyboard: true, 
            focus: true
        });
        modal.show();
    }

    configureModal(layerId){
        this.layerId = layerId;
        this.layerType = this.dataHandler.getLayerAttribute(layerId, 'type');
        
        const modalTitle = document.getElementById("layerConfigurationTitle");
        const layerType = document.getElementById("layerType");
        const form = document.getElementById("layerConfiguration");

        const newModalTitle = modalTitle.cloneNode(true); // Clone the element (true for deep clone)
        modalTitle.parentNode.replaceChild(newModalTitle, modalTitle);
        this.loadInputValueFromLocalstorage(newModalTitle,layerId);
        this.addUpdateDatahandlerEvent(newModalTitle,layerId);

        const newLayerType= layerType.cloneNode(true); // Clone the element (true for deep clone)
        layerType.parentNode.replaceChild(newLayerType, layerType);
        this.loadInputValueFromLocalstorage(newLayerType,layerId);

        const newForm = form.cloneNode(true); // Clone the element (true for deep clone)
        form.parentNode.replaceChild(newForm, form);
        this.updateFormByLayerType(this.layerType)

        this.updateModalLayerType(newLayerType, layerId)
    }

    loadInputValueFromLocalstorage(element, layerId){
        const valueOnLocalStorage = this.dataHandler.getLayerAttribute(layerId, element.getAttribute('attributeName'));
        if (element.type != "file" && valueOnLocalStorage){
            element.value = valueOnLocalStorage;
        }
        this.dataHandler.setLayerAttribute(layerId,element.getAttribute('attributeName'), element.value);
    }

    updateModalLayerType(newLayerType, layerId){
        this.addUpdateDatahandlerEvent(newLayerType,layerId);
        this.addUpdateFormEvent(newLayerType);

    }

    addUpdateFormEvent(newLayerType){
        const element= document.getElementById("layerType");
        element.addEventListener("change", (event) =>{
            this.updateFormByLayerType(event.currentTarget.value);
        });
    }

    updateMultiGeneratedOnDataHandler(newValue, oldValue, attribute){
        if(oldValue > newValue){
            for (let i = newValue; newValue < oldValue; newValue++){
                this.dataHandler.removeLayerAttribute(this.layerId, `${attribute}_${i}`);
            }
        }
    }

    addMultiGeneratedInputs(inputField, oldValue){
        console.log(`Old Value = ${oldValue}`);
        if(inputField.value != undefined){
            const generatedInputsDiv = document.querySelector(`.${inputField.getAttribute('name')}_generatedInputs`);
            if (generatedInputsDiv){
                generatedInputsDiv.innerHTML = `<p></p><br><label class="form-label">${generatedInputsDiv.getAttribute('generatedInputsTitle')}</label><br>`;
                for(let i=0; i < parseInt(inputField.value); i++){
                    let generatedInputConf = {
                        attribute: `${generatedInputsDiv.getAttribute('generatedInputsAttributes')}_${i}`,
                        inputType: generatedInputsDiv.getAttribute('generatedInputsType'),
                        label: `${generatedInputsDiv.getAttribute('generatedInputsLabel')} ${i}`
                    }

                    const generatedInput = this.createLabelInputByEnum(generatedInputConf);
                    generatedInput.classList.add('col');
                    this.addUpdateDatahandlerEvent(generatedInput, this.layerId);
                    this.loadInputValueFromLocalstorage(generatedInput,this.layerId);
                    generatedInputsDiv.appendChild(generatedInput);
                }
            this.updateMultiGeneratedOnDataHandler(inputField.value, oldValue, `${generatedInputsDiv.getAttribute('generatedInputsAttributes')}`);
            }
        }
    }

    createLabelInputByEnum(field){
        let div = document.createElement("div");
        
        let label = document.createElement("label");
        label.textContent = field.label;
        label.setAttribute("for", field.attribute);
        label.classList.add("form-label");
        div.appendChild(label);
        if(field.inputType != 'select'){
            let input = document.createElement("input");
            input.setAttribute("attributeName", field.attribute);
            input.setAttribute("type", field.inputType);
            input.setAttribute("name", field.attribute);
            input.classList.add("form-control");
            if (field.placeholder){
                input.setAttribute("placeholder", field.placeholder);
            }
            this.addUpdateDatahandlerEvent(input, this.layerId);
            this.loadInputValueFromLocalstorage(input,this.layerId);
            div.appendChild(input);
            if (field.generateNewInputs){
                let generatedInputsDiv = document.createElement("div");
                generatedInputsDiv.setAttribute('generatedInputsAttributes', field.generatedInputsAttributes);
                generatedInputsDiv.setAttribute('generatedInputsLabel', field.generatedInputsLabel);
                generatedInputsDiv.setAttribute('generatedInputsType', field.generatedInputsType);
                generatedInputsDiv.setAttribute('generatedInputsTitle', field.generatedInputsTitle);                
                generatedInputsDiv.classList.add(`${field.attribute}_generatedInputs`);
                generatedInputsDiv.classList.add('row');
                generatedInputsDiv.classList.add('align-items-start');                
                div.appendChild(generatedInputsDiv);
            }
        } else {
            let select = document.createElement('select');
            select.setAttribute("attributeName", field.attribute);
            select.setAttribute("type", field.inputType);
            select.setAttribute("name", field.attribute);
            select.classList.add("form-control");
            
            field.options.forEach((option) =>{
                let optionElement = document.createElement('option');
                optionElement.setAttribute("value", option.value);
                optionElement.value = option.value;      
                optionElement.textContent = option.label;  
                select.appendChild(optionElement);     
            });
            this.addUpdateDatahandlerEvent(select, this.layerId);
            this.loadInputValueFromLocalstorage(select,this.layerId);
            div.appendChild(select);
        }
        return div;
    }   

    setInputsByEnum(updatedForm, inputEnum){
        inputEnum.fields.forEach(field => {
            updatedForm.appendChild(this.createLabelInputByEnum(field));
        });
    }

    updateFormByLayerType(newLayerType) {
        let opcoesDiv = document.getElementById("layerConfiguration");
        opcoesDiv.innerHTML = "";
        
        let updatedForm = document.createElement("div");
        
        if (newLayerType === "P") {
            this.setInputsByEnum(updatedForm, poolingFormInputsEnum);
        } else if (newLayerType === "C") {
            this.setInputsByEnum(updatedForm, convolutionalFormInputsEnum);
        } else if (newLayerType === "FC") {
            this.setInputsByEnum(updatedForm, fullyConnectedFormInputsEnum);
        }
        opcoesDiv.appendChild(updatedForm);
    }
    

    addUpdateDatahandlerEvent(element, layerId) {
        const attribute = element.getAttribute('attributeName');
        element.addEventListener('blur', ()=>{
            if(element.value != undefined && element.value != this.dataHandler.getLayerAttribute(layerId, attribute)){
                this.addMultiGeneratedInputs(element, this.dataHandler.getLayerAttribute(layerId, attribute));
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