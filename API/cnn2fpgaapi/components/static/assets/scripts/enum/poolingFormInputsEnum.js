
const poolingFormInputsEnum = Object.freeze({
    fields : [ {label: "Tipo",
                attribute: "poolingType",
                inputType: "select",
                options: [{label: 'Max',
                           value : 'MAX'},
                           {label: 'Average',
                            value: 'AVG'
                           }]
                },
                {label: "Tamanho do Kernel (LinhasxColunas) Ex: 3x3",
                    attribute: "kernelSize",
                    inputType: "text",
                    placeholder: "Ex: 3x3"
                }
            ]
});

export default poolingFormInputsEnum;