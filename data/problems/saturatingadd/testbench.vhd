--  Testbench for saturating adder
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

entity saturatingadd_test is
-- No ports, since this is a testbench
end saturatingadd_test;

architecture test of saturatingadd_test is

component saturatingadd is
  port(
	  a : in unsigned(7 downto 0);
	  b : in unsigned(7 downto 0);
	  result : out unsigned(7 downto 0)
  );
end component;

signal a : unsigned(7 downto 0) := 8d"0";
signal b : unsigned(7 downto 0) := 8d"0";
signal result : unsigned(7 downto 0);

begin

  dut : saturatingadd port map(a, b, result);

  process
    variable errors : integer := 0;

    -- Standard check function
    procedure check(condition : boolean; message : string) is
    begin
      if not condition then
        report message;
        errors := errors + 1;
      end if;
    end check;


  begin

    a <= to_unsigned(1, 8);
    b <= to_unsigned(1, 8);
    wait for 10 ns;
    check(result = to_unsigned(2, 8), "Test failed for 1 + 1, got " & to_string(to_integer(result)));

    a <= to_unsigned(150, 8);
    b <= to_unsigned(100, 8);
    wait for 10 ns;
    check(result = to_unsigned(250, 8), "Test failed for 150 + 100, got " & to_string(to_integer(result)));

    a <= to_unsigned(255, 8);
    b <= to_unsigned(1, 8);
    wait for 10 ns;
    check(result = to_unsigned(255, 8), "Test failed for 255 + 1, got " & to_string(to_integer(result)));

    a <= to_unsigned(128, 8);
    b <= to_unsigned(128, 8);
    wait for 10 ns;
    check(result = to_unsigned(255, 8), "Test failed for 128 + 128, got " & to_string(to_integer(result)));

    a <= to_unsigned(127, 8);
    b <= to_unsigned(127, 8);
    wait for 10 ns;
    check(result = to_unsigned(254, 8), "Test failed for 127 + 127, got " & to_string(to_integer(result)));

    a <= to_unsigned(254, 8);
    b <= to_unsigned(254, 8);
    wait for 10 ns;
    check(result = to_unsigned(255, 8), "Test failed for 254 + 254, got " & to_string(to_integer(result)));

    if errors = 0 then
      write (output, "TEST PASSED." & LF);
    else
      write (output, "Test failed with " & to_string(errors) &  " errors." & LF);
    end if;

    wait;
  end process;
end test;

