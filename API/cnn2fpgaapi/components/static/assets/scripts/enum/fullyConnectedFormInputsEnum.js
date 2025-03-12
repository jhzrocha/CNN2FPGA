
const fullyConnectedFormInputsEnum = Object.freeze({
    fields : [ {label: "Função de Ativação",
                attribute: "activationFunction",
                inputType: "select",
                options: [{label: 'ReLU',
                           value : 'RELU'
                          },
                           {label: 'Sigmoid',
                            value: 'SIGMOID'
                           },
                           {label: 'Tangente Hiperbólica',
                            value: 'TANH'
                           }
                        ]
                },
                {   label: "Pesos",
                    attribute: "FCWeights",
                    inputType: "file"
                },
                {label: "Quantidade de Camadas",
                    attribute: "qtFCLayers",
                    inputType: "number",
                    generateNewInputs: true,
                    generatedInputsAttributes: 'qtNeuronLayer',
                    generatedInputsTitle: 'Quantidade de Neuronios por Camada', 
                    generatedInputsLabel: 'Camada ',
                    generatedInputsType: 'number'
                }
            ]
});

export default fullyConnectedFormInputsEnum;