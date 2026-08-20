--- ALGORITMO PARA COMUNICAÃ‡AO COM O COTROLADOR DO LCD ALFANUMÃ‰RICO
--- EDSON MANOEL DA SILVA
LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE IEEE.NUMERIC_STD.ALL;


ENTITY LCD_CONTROLADOR IS
	PORT
		(
			--//	Host Side
			iDATA : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
			iRS,iStart : IN STD_LOGIC;
			iCLK,iRST_N: IN STD_LOGIC;
			oDone : OUT STD_LOGIC;
			--//	LCD Interface
			LCD_DATA : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
			LCD_EN : OUT STD_LOGIC;
			LCD_RW : OUT STD_LOGIC;
			LCD_RS : OUT STD_LOGIC
		);
END ENTITY;


ARCHITECTURE FUNCIONAMENTO OF LCD_CONTROLADOR IS

--//	CLK
CONSTANT	CLK_Divide 		: STD_LOGIC_VECTOR(4 DOWNTO 0)	:=	"10000";

SIGNAL 	Cont 				: STD_LOGIC_VECTOR(4 DOWNTO 0);
SIGNAL 	ST   				: STD_LOGIC_VECTOR(1 DOWNTO 0);
SIGNAL  preStart,mStart		: STD_LOGIC;


BEGIN

	LCD_DATA <= iDATA;
	LCD_RW	 <=	'0';
	LCD_RS	 <=	iRS;
	
	PROCESS(iCLK, iRST_N)
	
	
		BEGIN

				IF(iRST_N = '0') THEN
					oDone	<=	'0';
					LCD_EN	<=	'0';
					preStart<=	'0';
					mStart	<=	'0';
					Cont	<=	(OTHERS => '0');
					ST		<=	(OTHERS => '0');
				ELSIF(iCLK'EVENT AND iCLK='1') THEN
					--//////	Input Start Detect ///////
					preStart  <= iStart;
					IF((preStart = '0') and (iStart='1'))THEN
						mStart	<=	'1';
						oDone	<=	'0';
					END IF;
					--//////////////////////////////////
					
					IF(mStart = '1') THEN	-- CASO SEJA RECEBIDO UM SINAL DE START, SÃƒO ENVIADOS ENTAO OS SINAIS DE COMANDO AO CONTROLADOR DO LCD
						CASE(ST) IS
							WHEN "00" =>	ST	<=	"01";	--//	Wait Setup
							
							WHEN "01" =>	
								LCD_EN	<=	'1';
								ST		<=	"10";
									
							WHEN "10" =>					
									IF(Cont<CLK_Divide) THEN
										Cont	<=	Cont+'1';
									ELSE
										ST		<=	"11";
									END IF;
									
							WHEN "11" =>
									LCD_EN	<=	'0';
									mStart	<=	'0';
									oDone	<=	'1';
									Cont	<=	(OTHERS => '0');
									ST		<=	"00";
							WHEN OTHERS =>
								ST		<=	"00";

						END CASE;
					END IF;
				END IF;
	END PROCESS;
	

END ARCHITECTURE;
