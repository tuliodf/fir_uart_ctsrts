library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.coefs_pkg.all;

entity fir_trans is port(
	clk			: in  std_logic;
	vld			: in  std_logic;
	rst			: in  std_logic;
	
	coef_in		: in 	signed(dataw-1 downto 0);
	coef_wr		: in 	std_logic;
	
	sample_in	: in 	signed(dataw-1 downto 0);
	sample_out	: out signed(dataw-1 downto 0);
	uart_debug	: out std_logic_vector(15 downto 0)
	);
end entity;

architecture rtl of fir_trans is 
	signal coef_pkg	: tap_array := coefs; 							  -- Coeficientes fixos do coefs_pkg.vhd
	signal coef_uart	: tap_array := (others => (others => '0')); -- Coeficientes vindo da UART
	signal coef_reg	: tap_array := (others => (others => '0')); -- Coeficientes do registrador
	
	signal coef_done	: signed(dataw-1 downto 0);
	signal coef_apply : std_logic;
	
	signal mult_out : mult_out_array := (others => (others => '0'));
	signal sum      : mult_out_array := (others => (others => '0'));
	signal reg_z    : mult_out_array := (others => (others => '0'));
begin
uart_debug <= std_logic_vector(coef_done);--coef_done  --coef_uart(0)
	gen_mult: for i in 0 to ntaps-1 generate
		U: entity work.mult
		port map(
			x => sample_in,
			y => coef_reg(i), --coef_pkg coef_reg
			z => mult_out(i));
	end generate;

	-- soma combinacional (forma transposta), sem if-generate
	sum_proc: process(mult_out, reg_z)
	begin
		sum(0) <= mult_out(0);
		for i in 1 to ntaps-1 loop
			sum(i) <= mult_out(i) + reg_z(i-1);
		end loop;
	end process;
	
	coef_apply <= '1' when coef_done = "0111111111111111" else '0';

	process(vld, rst)
	begin
		if rst = '1' then 
			reg_z <= (others => (others => '0')); 
		elsif rising_edge(vld) then
			for i in 0 to ntaps-1 loop
				reg_z(i) <= sum(i);
			end loop;
		end if;
	end process;

--Coeficientes vindos do UART
	gen_reg_uart: for i in 0 to ntaps generate
		first: if i = 0 generate
			U: entity work.reg port map(
				clk => clk,
				clr => rst,
				en	 => coef_wr,
				d   => coef_in,
				q   => coef_uart(i)
				);
		end generate first;
		
		other: if i > 0 and i < ntaps generate
			U: entity work.reg port map(
				clk => clk,
				clr => rst,
				en	 => coef_wr,
				d   => coef_uart(i-1),
				q   => coef_uart(i)
				);
		end generate other;
		
		gen_reg_apply: if i = ntaps generate
			U: entity work.reg port map(
				clk => clk,
				clr => rst,
				en	 => coef_wr,
				d	 => coef_uart(ntaps-1),
				q	 => coef_done
				);
		end generate gen_reg_apply;
	end generate;
	
--Registradores dos coeficientes ativos no filtro
	gen_reg_coefs: for i in 0 to ntaps-1 generate
		U: entity work.reg
		port map(
			clk => clk,
			clr => rst,
			en	 => coef_apply,
			d   => coef_uart(i),
			q   => coef_reg(i)
			);
	end generate;
	
	
	sample_out <= sum(ntaps-1)(2*dataw-2 downto dataw-1);

end architecture;