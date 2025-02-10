
import { LayersCards } from "./layersCards.js";
import { DataHandler } from "./dataHandler.js";

const layerCardsHandler = new LayersCards();
const dataHandler = new DataHandler();

document.addEventListener('DOMContentLoaded', (event) => {
    layerCardsHandler.initCards(dataHandler);
});
