library IEEE;
use IEEE.std_logic_1164.all;

entity gene_findtt is
  port(
    clk : in std_logic;
    nuc_in : in std_logic_vector(1 downto 0); -- Input nucleotide
    nuc_out : out std_logic_vector(1 downto 0); -- Input nucleotide
    is_double : out std_logic -- Whether the output nucleotide is part of a pair of thymines
  );
end;

architecture synth of gene_findtt is
begin
  -- We don't even have to clock this...
  nuc_out <= nuc_in;
  is_double <= '1' when (nuc_in = "11") else '0';
end;

