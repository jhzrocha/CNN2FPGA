
const convolutionalFormInputsEnum = Object.freeze({
    fields : [ {label: "Pesos",
                attribute: "weights",
                inputType: "number"
                },
                {label: "Bias",
                    attribute: "bias",
                    inputType: "number"
                },
                {label: "Tamanho do Kernel",
                    attribute: "kernelSize",
                    inputType: "number"
                }
            ]
});

export default convolutionalFormInputsEnum;