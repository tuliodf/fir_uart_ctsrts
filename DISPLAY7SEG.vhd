-- COMPONENTE PARA UTILIZAR OS DISPLAYS DE 7 SEGMENTOS DA PLACA
-- EDSON MANOEL DA SILVA

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;


ENTITY DISPLAY7SEG IS
	PORT(
			iDIG	: IN STD_LOGIC_VECTOR(3 DOWNTO 0);
			oSEG	: OUT STD_LOGIC_VECTOR(6 DOWNTO 0)
		);
END ENTITY;

ARCHITECTURE FUNCIONAMENTO OF DISPLAY7SEG IS
	

BEGIN

	PROCESS(iDIG)
		BEGIN
			case(iDIG) IS
				WHEN X"1"=> oSEG <= "1111001";	-- ---t----
				WHEN X"2"=> oSEG <= "0100100"; 	-- |	  |
				WHEN X"3"=> oSEG <= "0110000"; 	-- lt	 rt
				WHEN X"4"=> oSEG <= "0011001"; 	-- |	  |
				WHEN X"5"=> oSEG <= "0010010"; 	-- ---m----
				WHEN X"6"=> oSEG <= "0000010"; 	-- |	  |
				WHEN X"7"=> oSEG <= "1111000"; 	-- lb	 rb
				WHEN X"8"=> oSEG <= "0000000"; 	-- |	  |
				WHEN X"9"=> oSEG <= "0011000"; 	-- ---b----
				WHEN X"A"=> oSEG <= "0001000";
				WHEN X"B"=> oSEG <= "0000011";
				WHEN X"C"=> oSEG <= "1000110";
				WHEN X"D"=> oSEG <= "0100001";
				WHEN X"E"=> oSEG <= "0000110";
				WHEN X"F"=> oSEG <= "0001110";
				WHEN X"0"=> oSEG <= "1000000";
				WHEN OTHERS => oSEG <= "1000000";
			end case;
	END PROCESS;

END ARCHITECTURE;