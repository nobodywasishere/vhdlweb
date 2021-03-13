
GHDL=ghdl
FLAGS="--std=08"
TOP=abc

all: run netlist

gold:
	@$(GHDL) -a $(FLAGS) testbench.vhd abc_gold.vhd
	@$(GHDL) -e $(FLAGS) abc_test
	@$(GHDL) -r $(FLAGS) abc_test --stop-time=1us

run:
	@$(GHDL) -a $(FLAGS) testbench.vhd submission.vhd
	@$(GHDL) -e $(FLAGS) abc_test
	@$(GHDL) -r $(FLAGS) abc_test --stop-time=1us

netlist:
	-rm work-obj08.cf > /dev/null
	$(GHDL) -a $(FLAGS) submission.vhd
	yosys -m $(GHDL) -p "ghdl $(FLAGS) $(TOP); prep -top $(TOP); write_json -compat-int svg.json" > /dev/null
	sed -i 's/"top": "[0]{31}1"/"top": 1/g' svg.json
	sed -i 's/"z"/"x"/g' svg.json
