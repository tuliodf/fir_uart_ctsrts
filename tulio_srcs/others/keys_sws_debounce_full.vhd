-------------------------------------------------------------------------------
-- keys_sws_debounce.vhd
--
-- Debounce simples, em uma única entity/architecture, para os vetores
-- KEY(3 downto 0) e SW(17 downto 0) da DE2-115. Sem instanciação de
-- componentes: toda a lógica (sincronizador + contador) fica direto no
-- mesmo processo, percorrendo cada bit dos vetores com "for".
--
-- Funcionamento (igual para cada bit dos dois vetores):
--   1) Sincroniza a entrada com 2 flip-flops (evita metaestabilidade).
--   2) Só atualiza a saída depois que o valor sincronizado ficar estável
--      por DEBOUNCE_CYCLES ciclos seguidos.
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity keys_sws_debounce_full is
    generic (
        KEY_DEBOUNCE_CYCLES : integer := 500000;  -- ~10ms @ 50MHz
        SW_DEBOUNCE_CYCLES  : integer := 250000   -- ~5ms  @ 50MHz
    );
    port (
        clk     : in  std_logic;
        rst_n   : in  std_logic;                      -- reset assíncrono, ativo em '1'
        key_in  : in  std_logic_vector(3 downto 0);   -- KEY[3:0], bruto
        sw_in   : in  std_logic_vector(17 downto 0);  -- SW[17:0], bruto
        key_out : out std_logic_vector(3 downto 0);   -- KEY[3:0], debounced
        sw_out  : out std_logic_vector(17 downto 0)   -- SW[17:0], debounced
    );
end entity keys_sws_debounce_full;

architecture rtl of keys_sws_debounce_full is

    -- sincronizadores (2 flip-flops cada bit)
    signal key_sync1, key_sync2 : std_logic_vector(3 downto 0)  := (others => '0');
    signal sw_sync1,  sw_sync2  : std_logic_vector(17 downto 0) := (others => '0');

    -- contadores de estabilidade, um por bit
    type key_cnt_array is array (0 to 3) of unsigned(31 downto 0);
    type sw_cnt_array  is array (0 to 17) of unsigned(31 downto 0);
    signal key_cnt : key_cnt_array := (others => (others => '0'));
    signal sw_cnt  : sw_cnt_array  := (others => (others => '0'));

    signal key_stable : std_logic_vector(3 downto 0)  := (others => '0');
    signal sw_stable   : std_logic_vector(17 downto 0) := (others => '0');

begin

    -- Sincronizadores
    process(clk, rst_n)
    begin
        if rst_n = '1' then
            key_sync1 <= (others => '0');
            key_sync2 <= (others => '0');
            sw_sync1  <= (others => '0');
            sw_sync2  <= (others => '0');
        elsif rising_edge(clk) then
            key_sync1 <= key_in;
            key_sync2 <= key_sync1;
            sw_sync1  <= sw_in;
            sw_sync2  <= sw_sync1;
        end if;
    end process;

    -- Debounce das KEYs
    process(clk, rst_n)
    begin
        if rst_n = '1' then
            key_stable <= (others => '0');
            key_cnt    <= (others => (others => '0'));
        elsif rising_edge(clk) then
            for i in 0 to 3 loop
                if key_sync2(i) /= key_stable(i) then
                    if key_cnt(i) >= to_unsigned(KEY_DEBOUNCE_CYCLES - 1, 32) then
                        key_stable(i) <= key_sync2(i);
                        key_cnt(i)    <= (others => '0');
                    else
                        key_cnt(i) <= key_cnt(i) + 1;
                    end if;
                else
                    key_cnt(i) <= (others => '0');
                end if;
            end loop;
        end if;
    end process;

    -- Debounce das SWs
    process(clk, rst_n)
    begin
        if rst_n = '1' then
            sw_stable <= (others => '0');
            sw_cnt    <= (others => (others => '0'));
        elsif rising_edge(clk) then
            for i in 0 to 17 loop
                if sw_sync2(i) /= sw_stable(i) then
                    if sw_cnt(i) >= to_unsigned(SW_DEBOUNCE_CYCLES - 1, 32) then
                        sw_stable(i) <= sw_sync2(i);
                        sw_cnt(i)    <= (others => '0');
                    else
                        sw_cnt(i) <= sw_cnt(i) + 1;
                    end if;
                else
                    sw_cnt(i) <= (others => '0');
                end if;
            end loop;
        end if;
    end process;

    key_out <= key_stable;
    sw_out  <= sw_stable;

end architecture rtl;