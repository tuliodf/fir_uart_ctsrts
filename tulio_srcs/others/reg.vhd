library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;

library work;
use work.coefs_pkg.all;

entity reg is
    Port (
        clk : in  std_logic;
        clr	: in  std_logic;
        en 	: in  std_logic;
        d  	: in  signed(dataw-1 downto 0);
        q   : out signed(dataw-1 downto 0)
    );
end entity;

architecture rtl of reg is
    signal reg : signed(dataw-1 downto 0);
begin

    process(clk)
    begin
        if rising_edge(clk) then
            if clr = '1' then
                reg <= (others => '0');
            elsif en = '1' then
                reg <= d;
            end if;
        end if;
    end process;

    q <= reg;

end architecture;