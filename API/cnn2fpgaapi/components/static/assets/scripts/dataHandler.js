export class DataHandler {
    userLocalStorage = {}

    addLayer(layerID){
        this.userLocalStorage[`layer${layerID}`] = {name : `Camada ${layerID}`}
        this.userLocalStorage[`layer${layerID}`].type = '--';
        localStorage.setItem('userLocalStorage', JSON.stringify(this.userLocalStorage));
    }

    addAttribute(attribute, value){
        this.userLocalStorage[`${attribute}`] = value;
    }

    removeLayer(layerID){
        delete this.userLocalStorage[layerID];
        this.updateLayersAfterRemove(layerID);
    }

    updateLayersAfterRemove() {
        const entries = Object.entries(this.userLocalStorage)
            .sort((a, b) => {
                const numA = parseInt(a[0].replace('layer', ''));
                const numB = parseInt(b[0].replace('layer', ''));
                return numA - numB;
            });
    
        const layersRenomeados = {};
        entries.forEach((entry, index) => {
            const newKey = `layer${index + 1}`;
            layersRenomeados[newKey] = entry[1];
        });
    
        this.userLocalStorage = layersRenomeados;
        console.log(this.userLocalStorage);
    }

    getLayer(layerID){
        return this.userLocalStorage[`${layerID}`];
    }

    getLayerAttribute(layerId, attribute){
        const layer = this.getLayer(layerId);
        return layer[attribute];
    }

    setLayerAttribute(layerId, attribute, value){
        const layer = this.getLayer(layerId);
        layer[attribute] = value;
    }

    removeLayerAttribute(layerID, attribute) {
        delete this.userLocalStorage[`${layerID}`][attribute]; // Remove o atributo especificado
    }


}