export class DataHandler {
    layers = {}

    addLayer(layerID){
        this.layers[`layer${layerID}`] = {name : `Camada ${layerID}`}
        this.layers[`layer${layerID}`].type = '--';
        localStorage.setItem('layers', JSON.stringify(this.layers));
    }

    removeLayer(layerID){
        delete this.layers[layerID];
        this.updateLayersAfterRemove(layerID);
    }

    updateLayersAfterRemove() {
        const entries = Object.entries(this.layers)
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
    
        this.layers = layersRenomeados;
        console.log(this.layers);
    }

    getLayer(layerID){
        return this.layers[`${layerID}`];
    }

    getLayerAttribute(layerId, attribute){
        const layer = this.getLayer(layerId);
        return layer[attribute];
    }

    setLayerAttribute(layerId, attribute, value){
        const layer = this.getLayer(layerId);
        layer[attribute] = value;
    }
}