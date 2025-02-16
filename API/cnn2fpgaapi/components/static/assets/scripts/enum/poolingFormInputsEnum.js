
const poolingFormInputsEnum = Object.freeze({
    fields : [ {label: "Tipo",
                attribute: "poolingType",
                inputType: "text"
                },
                {label: "Linhas no Kernel",
                    attribute: "qtRows",
                    inputType: "number"
                },
                {label: "Colunas no Kernel",
                    attribute: "qtCols",
                    inputType: "number"
                }
            ]
});

export default poolingFormInputsEnum;