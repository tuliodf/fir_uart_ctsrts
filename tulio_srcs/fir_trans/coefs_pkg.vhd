	-------------------------------------------------------------------------------
-- coefs_pkg.vhd
-- Gerado automaticamente por fir_generator.py -- NAO EDITAR MANUALMENTE
-- Tipo de filtro   : Passa-Baixas (FILTER_SEL = "00")
-- Fs               : 48000.0 Hz
-- FC1              : 2000.0 Hz
-- Formato          : Q1.15 (signed, complemento de dois)
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package coefs_pkg is

constant ntaps : integer := 4; --256
constant dataw : integer := 16;

type tap_array is array (0 to ntaps-1) of signed(dataw-1 downto 0);
type mult_out_array is array (0 to ntaps-1) of signed(2*dataw-1 downto 0);

constant coefs : tap_array := (
      0 => to_signed(1127, dataw),
		others => to_signed(0, dataw)
);

end package coefs_pkg;
