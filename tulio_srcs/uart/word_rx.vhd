library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity word_rx is
  port (clk               : in  std_logic;
        rst               : in  std_logic;

        -- [FIX] entradas vindas do uart_top, em vez de uart_rx bruto
        rx_valid	         : in  std_logic;                     -- <= rx_valid do uart_top
        rx_data            : in  std_logic_vector(7 downto 0);  -- <= rx_data  do uart_top

        word_ready : out std_logic := '0';
        word       : out std_logic_vector(15 downto 0));
end entity word_rx;

architecture rtl of word_rx is
  type state_t is (recebeH, recebeL, done);
  signal estado    : state_t := recebeH;
--  signal word_done : std_logic;
begin

  process (clk)
  begin
    if rising_edge(clk) then
      if rst = '1' then
        estado    <= recebeH;
        word_ready <= '0';
      else
        word_ready <= '0';

          case estado is
            when recebeH =>
              if rx_valid = '1' then
                word(15 downto 8) <= rx_data;
                estado            <= recebeL;
              end if;

            when recebeL =>
              if rx_valid = '1' then
                word(7 downto 0) <= rx_data;
                estado           <= done;
              end if;

            when done =>
              word_ready <= '1';
              estado    <= recebeH;

          end case;
end if;
end if;
  end process;

end architecture rtl;