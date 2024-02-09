transcript on
if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vcom -93 -work work {C:/Users/jhzro/OneDrive/햞ea de Trabalho/CNN2FPGA/CNN2FPGA/VHDL/multiplicator.vhd}
vcom -93 -work work {C:/Users/jhzro/OneDrive/햞ea de Trabalho/CNN2FPGA/CNN2FPGA/VHDL/Adder_9in.vhd}
vcom -93 -work work {C:/Users/jhzro/OneDrive/햞ea de Trabalho/CNN2FPGA/CNN2FPGA/VHDL/MatrixMultiplier.vhd}
vcom -93 -work work {C:/Users/jhzro/OneDrive/햞ea de Trabalho/CNN2FPGA/CNN2FPGA/VHDL/CNN2FPGAVHDL.vhd}

