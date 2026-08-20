-------------------------------------------------------------------------------
-- sampler_generator.vhd
--
-- Gera um pulso (baudrate_out) de 1 ciclo de clock no meio de cada bit de um
-- frame UART, sincronizado pela borda de descida do start bit em uart_rx.
--
-- Funcionamento:
--   1. Em repouso (idle), monitora uart_rx esperando uma borda de descida
--      (1 -> 0), que é o start bit.
--   2. Ao detectar a borda, conta metade do período de bit (CLKS_PER_BIT/2)
--      e gera o primeiro pulso -- isso posiciona a amostragem no MEIO do
--      start bit, o ponto mais seguro (longe das bordas, onde há mais risco
--      de erro de amostragem).
--   3. A partir daí, gera um pulso a cada período de bit completo
--      (CLKS_PER_BIT), cobrindo os 8 bits de dado + o stop bit
--      (10 pulsos no total: start + 8 dados + stop).
--   4. Após os 10 pulsos, volta a monitorar a linha para o próximo frame.
--
-- Generics:
--   CLK_FREQ_HZ : frequência do clock do sistema, em Hz
--   BAUD_RATE   : taxa de transmissão desejada, em bits/segundo
-------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity sampler_generator is
  generic (CLK_FREQ_HZ : integer := 50_000_000;
           BAUD_RATE   : integer := 57_600);
  port (clock        : in  std_logic;
        uart_rx      : in  std_logic;
        baudrate_out : out std_logic);
end entity sampler_generator;

architecture rtl of sampler_generator is

  constant CLKS_PER_BIT : integer := CLK_FREQ_HZ / BAUD_RATE;

  -- sincronizador de 2 FFs para detectar a borda de uart_rx com segurança
  signal rx_sync0, rx_sync1, rx_sync2 : std_logic := '1';

  signal counting     : std_logic := '0';
  signal counter      : integer range 0 to CLKS_PER_BIT - 1 := 0;
  signal bit_index     : integer range 0 to 9 := 0;  -- start + 8 dados + stop = 10
  signal baudrate_out_s : std_logic := '0';

begin

  baudrate_out <= baudrate_out_s;

  process (clock) is
  begin
    if rising_edge(clock) then
      -- sincronizador simples de 2 FFs (mais rx_sync2 guarda o valor anterior
      -- para deteccao de borda)
      rx_sync0 <= uart_rx;
      rx_sync1 <= rx_sync0;
      rx_sync2 <= rx_sync1;

      baudrate_out_s <= '0';  -- default: pulso de 1 ciclo

      if counting = '0' then
        -- procurando borda de descida (1 -> 0) = start bit
        if rx_sync2 = '1' and rx_sync1 = '0' then
          counting   <= '1';
          bit_index  <= 0;
          -- primeiro pulso no meio do bit: metade do periodo, ajustado pelo
          -- atraso de 2 ciclos ja gasto no sincronizador
          if CLKS_PER_BIT / 2 > 2 then
            counter <= CLKS_PER_BIT / 2 - 2;
          else
            counter <= 0;
          end if;
        end if;

      else
        if counter = 0 then
          baudrate_out_s <= '1';
          counter        <= CLKS_PER_BIT - 1;

          if bit_index = 9 then
            -- ja geramos os 10 pulsos (start + 8 dados + stop): rearma
            counting  <= '0';
            bit_index <= 0;
          else
            bit_index <= bit_index + 1;
          end if;
        else
          counter <= counter - 1;
        end if;
      end if;
    end if;
  end process;

end architecture rtl;
