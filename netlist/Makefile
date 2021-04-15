
GHDL=ghdl
FLAGS="--std=08"
NETLIST=netlist.json

run:
	@$(GHDL) -a $(FLAGS) submission.vhd

$(NETLIST):
	@$(GHDL) -a $(FLAGS) submission.vhd
	@yosys -m ghdl -p "ghdl $(FLAGS) top; prep -top top; write_json -compat-int $(NETLIST)"
