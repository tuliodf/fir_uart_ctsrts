-------------------------------------------------------------------------------
-- coef_pkg.vhd
-- Gerado automaticamente por gerar_coeficientes.py -- NAO EDITAR MANUALMENTE
-- Tipo de filtro   : Rejeita-Faixa (FILTER_SEL = "11")
-- Fs               : 48000.0 Hz
-- FC1              : 2000.0 Hz
-- FC2              : 5000.0 Hz
-- Formato          : Q1.15 (largura total 16 bits, complemento de dois)
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;

package coef_pkg is

    constant NUM_TAPS   : integer := 63;
    constant COEF_WIDTH : integer := 16;

    type coef_array_t is array (0 to NUM_TAPS-1) of std_logic_vector(COEF_WIDTH-1 downto 0);

    constant COEFS : coef_array_t := (
          0 => x"FFFF",  -- -1
          1 => x"0008",  -- 8
          2 => x"001B",  -- 27
          3 => x"0033",  -- 51
          4 => x"004A",  -- 74
          5 => x"0051",  -- 81
          6 => x"003B",  -- 59
          7 => x"0000",  -- 0
          8 => x"FFA8",  -- -88
          9 => x"FF4D",  -- -179
         10 => x"FF10",  -- -240
         11 => x"FF10",  -- -240
         12 => x"FF52",  -- -174
         13 => x"FFB8",  -- -72
         14 => x"0007",  -- 7
         15 => x"0000",  -- 0
         16 => x"FF81",  -- -127
         17 => x"FEA8",  -- -344
         18 => x"FDD8",  -- -552
         19 => x"FDA1",  -- -607
         20 => x"FE88",  -- -376
         21 => x"00C5",  -- 197
         22 => x"040C",  -- 1036
         23 => x"078C",  -- 1932
         24 => x"0A1C",  -- 2588
         25 => x"0A9E",  -- 2718
         26 => x"0867",  -- 2151
         27 => x"0395",  -- 917
         28 => x"FD20",  -- -736
         29 => x"F69D",  -- -2403
         30 => x"F1CD",  -- -3635
         31 => x"6FCE",  -- 28622
         32 => x"F1CD",  -- -3635
         33 => x"F69D",  -- -2403
         34 => x"FD20",  -- -736
         35 => x"0395",  -- 917
         36 => x"0867",  -- 2151
         37 => x"0A9E",  -- 2718
         38 => x"0A1C",  -- 2588
         39 => x"078C",  -- 1932
         40 => x"040C",  -- 1036
         41 => x"00C5",  -- 197
         42 => x"FE88",  -- -376
         43 => x"FDA1",  -- -607
         44 => x"FDD8",  -- -552
         45 => x"FEA8",  -- -344
         46 => x"FF81",  -- -127
         47 => x"0000",  -- 0
         48 => x"0007",  -- 7
         49 => x"FFB8",  -- -72
         50 => x"FF52",  -- -174
         51 => x"FF10",  -- -240
         52 => x"FF10",  -- -240
         53 => x"FF4D",  -- -179
         54 => x"FFA8",  -- -88
         55 => x"0000",  -- 0
         56 => x"003B",  -- 59
         57 => x"0051",  -- 81
         58 => x"004A",  -- 74
         59 => x"0033",  -- 51
         60 => x"001B",  -- 27
         61 => x"0008",  -- 8
         62 => x"FFFF"  -- -1
    );

end package coef_pkg;
