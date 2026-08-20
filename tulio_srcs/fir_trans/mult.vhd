library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.coefs_pkg.all;

entity mult is port(
	x			: in  signed(dataw-1 downto 0);
	y			: in  signed(dataw-1 downto 0);
	z			: out signed(2*dataw-1 downto 0));
end entity;

architecture rtl of mult is 
begin
	z <= x * y;
end architecture;