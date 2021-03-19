
GHDL=ghdl
FLAGS=--std=08
TOP=top

all: run netlist

run:
	>&2 echo
	>&2 echo "~~~ RUNNING TESTBENCH ~~~"
	>&2 echo
	@$(GHDL) -a $(FLAGS) submission.vhd
	@$(GHDL) -e $(FLAGS) $(TOP)
	@$(GHDL) -r $(FLAGS) $(TOP) --stop-time=1us

netlist:
	>&2 echo
	>&2 echo "~~~ GENERATING SVG ~~~"
	>&2 echo
	-rm work-obj08.cf > /dev/null
	-$(GHDL) -a $(FLAGS) submission.vhd
	-yosys -m $(GHDL) -p "ghdl $(FLAGS) $(TOP); prep -top $(TOP); write_json -compat-int svg.json" > /dev/null
	-yosys -m $(GHDL) -p '$(GHDL) $(FLAGS) $(TOP); synth_ice40 -json $(TOP).json' | grep -A 9 "=== $(TOP) ===" | sed "s/=== $(TOP) ===/Device utilization:/g"
