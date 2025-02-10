
const fullyConnectedFormInputsEnum = Object.freeze({
    fields : [ {label: "Pesos",
                attribute: "weights",
                inputType: "file"
                },
                {label: "Bias",
                    attribute: "bias",
                    inputType: "file"
                },
                {label: "Tamanho do Kernel",
                    attribute: "kernelSize",
                    inputType: "number"
                }
            ]
});

export default fullyConnectedFormInputsEnum;