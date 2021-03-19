
GHDL=ghdl
FLAGS="--std=08"
TOP=alu

all: run netlist

gold:
	@$(GHDL) -a $(FLAGS) testbench.vhd alu_gold.vhd
	@$(GHDL) -e $(FLAGS) alu_test
	@$(GHDL) -r $(FLAGS) alu_test --stop-time=1us

run:
	@$(GHDL) -a $(FLAGS) testbench.vhd submission.vhd
	@$(GHDL) -e $(FLAGS) alu_test
	@$(GHDL) -r $(FLAGS) alu_test --stop-time=1us

netlist:
	>&2 echo
	>&2 echo "~~~ GENERATING SVG ~~~"
	>&2 echo
	-rm work-obj08.cf > /dev/null
	$(GHDL) -a $(FLAGS) submission.vhd
	yosys -m $(GHDL) -p "ghdl $(FLAGS) $(TOP); prep -top $(TOP); write_json -compat-int svg.json" > /dev/null
