library IEEE;
use IEEE.std_logic_1164.all;

entity lfsr4 is
  port(
	  clk : in std_logic;
	  reset : in std_logic;
	  count : out std_logic_vector(3 downto 0)
  );
end lfsr4;

architecture synth of lfsr4 is
begin
  process(clk) is
  begin
    if rising_edge(clk) then
      if reset = '1' then
        count <= "0001";
      else
        count(3) <= count(0);
        count(2) <= count(3) xor count(0);
        count(1 downto 0) <= count (2 downto 1);
      end if;

    end if;
  end process;
end;

