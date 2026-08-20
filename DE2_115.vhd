--- CÓDIGO PADRÃO PARA A PLACA DE2_115 IMPLEMENTADO POR EDSON MANOEL DA SILVA
--- AS IMPLEMENTAÇOES DE ALGUNS BLOCOS DE CONTROLE DOS COMPONENETES SECUNDÁRIOS SÃO BASEADOS NO PROJETO
--- D:\Edson\Quartus\PLACA_DE2_115\DE2_115_demonstrations\DE2_115_Default

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE IEEE.NUMERIC_STD.ALL;

ENTITY DE2_115 IS
	PORT
		(
		--//////////// CLOCK //////////
			CLOCK_50 : IN STD_LOGIC;
			CLOCK2_50: IN STD_LOGIC;
			CLOCK3_50: IN STD_LOGIC;
		--//////////// Sma //////////
			SMA_CLKIN : IN STD_LOGIC;
			SMA_CLKOUT: OUT STD_LOGIC;
		--//////////// LED //////////
			LEDG	   : OUT STD_LOGIC_VECTOR(8 DOWNTO 0);
			LEDR	   : OUT STD_LOGIC_VECTOR(17 DOWNTO 0);
		--//////////// KEY //////////
			KEY	   : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		--//////////// EX_IO //////////
			EX_IO	   : inout STD_LOGIC_VECTOR(6 DOWNTO 0);
		--//////////// SW //////////
			SW		   : IN	STD_LOGIC_VECTOR(17 DOWNTO 0);

		--//////////// SEG7 //////////
			HEX0	   : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
			HEX1	   : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
			HEX2	   : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
			HEX3	   : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
			HEX4	   : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
			HEX5	   : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
			HEX6	   : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
			HEX7	   : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		--//////////// LCD //////////
			LCD_BLON	: OUT STD_LOGIC;
			LCD_DATA	: inout STD_LOGIC_VECTOR(7 DOWNTO 0);
			LCD_EN 		: OUT STD_LOGIC;
			LCD_ON		: OUT STD_LOGIC;
			LCD_RS		: OUT STD_LOGIC;
			LCD_RW		: OUT STD_LOGIC;
			
		--//////////// RS232 //////////
			UART_CTS	: IN STD_LOGIC;
			UART_RTS	: OUT  STD_LOGIC;
			UART_RXD	: IN  STD_LOGIC;
			UART_TXD	: OUT STD_LOGIC;
		--//////////// PS2 for Keyboard and Mouse //////////
			PS2_CLK		: inout STD_LOGIC;
			PS2_CLK2	: inout STD_LOGIC;
			PS2_DAT 	: inout STD_LOGIC;
			PS2_DAT2 	: inout STD_LOGIC;
		--//////////// SDCARD //////////
			SD_CLK		: OUT	STD_LOGIC;
			SD_CMD		: inout STD_LOGIC;
			SD_DAT		: inout STD_LOGIC_VECTOR(3 DOWNTO 0);
			SD_WP_N		: IN 	STD_LOGIC;
		--//////////// VGA //////////
			VGA_B		: OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
			VGA_BLANK_N	: OUT STD_LOGIC;
			VGA_CLK		: OUT STD_LOGIC;
			VGA_G		: OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
			VGA_HS		: OUT STD_LOGIC;
			VGA_R		: OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
			VGA_SYNC_N	: OUT STD_LOGIC;
			VGA_VS		: OUT STD_LOGIC;

		--//////////// Audio //////////
			AUD_ADCDAT	: IN STD_LOGIC;
			AUD_ADCLRCK	: inout STD_LOGIC;
			AUD_BCLK	: inout STD_LOGIC;
			AUD_DACDAT	: OUT STD_LOGIC;
			AUD_DACLRCK	: inout STD_LOGIC;
			AUD_XCK		: OUT STD_LOGIC;

		--//////////// I2C for EEPROM //////////
			EEP_I2C_SCLK: OUT STD_LOGIC;
			EEP_I2C_SDAT: inout STD_LOGIC;

		--//////////// I2C for Audio Tv-Decoder  //////////
			I2C_SCLK	: OUT STD_LOGIC;
			I2C_SDAT 	: inout STD_LOGIC;

		--//////////// Ethernet 0 //////////
			ENET0_GTX_CLK: OUT STD_LOGIC;
			ENET0_INT_N	 : IN  STD_LOGIC;
			ENET0_LINK100: IN  STD_LOGIC;
			ENET0_MDC	 : OUT STD_LOGIC;
			ENET0_MDIO	 : inout STD_LOGIC;
			ENET0_RST_N	 : OUT	STD_LOGIC;
			ENET0_RX_CLK : IN STD_LOGIC;
			ENET0_RX_COL : IN STD_LOGIC;
			ENET0_RX_CRS : IN STD_LOGIC;
			ENET0_RX_DATA: IN STD_LOGIC_VECTOR(3 DOWNTO 0);
			ENET0_RX_DV	 : IN STD_LOGIC;
			ENET0_RX_ER	 : IN STD_LOGIC;
			ENET0_TX_CLK : IN STD_LOGIC;
			ENET0_TX_DATA: OUT STD_LOGIC_VECTOR(3 DOWNTO 0);
			ENET0_TX_EN	 : OUT STD_LOGIC;
			ENET0_TX_ER	 : OUT STD_LOGIC;
			ENETCLK_25	 : IN STD_LOGIC;

		--//////////// Ethernet 1 //////////
			ENET1_GTX_CLK: OUT STD_LOGIC;
			ENET1_INT_N	 : IN  STD_LOGIC;
			ENET1_LINK100: IN  STD_LOGIC;
			ENET1_MDC	 : OUT STD_LOGIC;
			ENET1_MDIO	 : inout STD_LOGIC;
			ENET1_RST_N	 : OUT STD_LOGIC;
			ENET1_RX_CLK : IN STD_LOGIC;
			ENET1_RX_COL : IN STD_LOGIC;
			ENET1_RX_CRS : IN STD_LOGIC;
			ENET1_RX_DATA: IN STD_LOGIC_VECTOR(3 DOWNTO 0);
			ENET1_RX_DV	 : IN STD_LOGIC;
			ENET1_RX_ER	 : IN STD_LOGIC;
			ENET1_TX_CLK : IN STD_LOGIC;
			ENET1_TX_DATA: OUT STD_LOGIC_VECTOR(3 DOWNTO 0);
			ENET1_TX_EN	 : OUT STD_LOGIC;
			ENET1_TX_ER	 : OUT STD_LOGIC;

		--//////////// TV Decoder //////////
			TD_CLK27	: IN STD_LOGIC;
			TD_DATA		: IN STD_LOGIC_VECTOR(7 DOWNTO 0);
			TD_HS		: IN STD_LOGIC;
			TD_RESET_N	: OUT STD_LOGIC;
			TD_VS		: IN STD_LOGIC;

		--//////////// USB 2.0 OTG //////////
			OTG_ADDR	: OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
			OTG_CS_N	: OUT STD_LOGIC;
			OTG_DACK_N	: OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
			OTG_DATA	: inout STD_LOGIC_VECTOR(15 DOWNTO 0);
			OTG_DREQ	: IN STD_LOGIC_VECTOR(1 DOWNTO 0);	
			OTG_FSPEED	: inout STD_LOGIC;
			OTG_INT		: IN STD_LOGIC_VECTOR(1 DOWNTO 0);
			OTG_LSPEED	: inout STD_LOGIC;
			OTG_RD_N	: OUT STD_LOGIC;
			OTG_RST_N	: OUT STD_LOGIC;
			OTG_WE_N	: OUT STD_LOGIC;

		--//////////// IR Receiver //////////
			IRDA_RXD	: IN STD_LOGIC;

		--//////////// SDRAM //////////
			DRAM_ADDR	: OUT STD_LOGIC_VECTOR(12 DOWNTO 0);
			DRAM_BA		: OUT STD_LOGIC_VECTOR(1 DOWNTO 0);	
			DRAM_CAS_N	: OUT STD_LOGIC;
			DRAM_CKE	: OUT STD_LOGIC;
			DRAM_CLK	: OUT STD_LOGIC;
			DRAM_CS_N	: OUT STD_LOGIC;
			DRAM_DQ		: inout STD_LOGIC_VECTOR(31 DOWNTO 0);
			DRAM_DQM	: OUT STD_LOGIC_VECTOR(3 DOWNTO 0);
			DRAM_RAS_N	: OUT STD_LOGIC;
			DRAM_WE_N	: OUT STD_LOGIC;

		--//////////// SRAM //////////
			SRAM_ADDR	: OUT STD_LOGIC_VECTOR(19 DOWNTO 0);
			SRAM_CE_N	: OUT STD_LOGIC;
			SRAM_DQ		: inout STD_LOGIC_VECTOR(15 DOWNTO 0);
			SRAM_LB_N   : OUT STD_LOGIC;
			SRAM_OE_N	: OUT STD_LOGIC;
			SRAM_UB_N	: OUT STD_LOGIC;
			SRAM_WE_N	: OUT STD_LOGIC;

		--//////////// Flash //////////
			FL_ADDR		: OUT STD_LOGIC_VECTOR(22 DOWNTO 0);
			FL_CE_N		: OUT STD_LOGIC;
			FL_DQ		: inout STD_LOGIC_VECTOR(7 DOWNTO 0);
			FL_OE_N		: OUT STD_LOGIC;
			FL_RST_N	: OUT STD_LOGIC;
			FL_RY		: IN STD_LOGIC;
			FL_WE_N		: OUT STD_LOGIC;
			FL_WP_N		: OUT STD_LOGIC
		);
END ENTITY;


ARCHITECTURE FUNCIONAMENTO OF DE2_115 IS



--------------------------------------- DECLARAÇÃO DE COMPONENTES---------------------------
COMPONENT DISPLAY7SEG
	PORT
	(
		iDIG		:	 IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		oSEG		:	 OUT STD_LOGIC_VECTOR(6 DOWNTO 0)
	);
END COMPONENT;

COMPONENT TESTE_LCD
	PORT
	(
		iCLK		:	 IN STD_LOGIC;
		iRST_N		:	 IN STD_LOGIC;
		LCD_DATA	:	 OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
		LCD_RW		:	 OUT STD_LOGIC;
		LCD_EN		:	 OUT STD_LOGIC;
		LCD_RS		:	 OUT STD_LOGIC
	);
END COMPONENT;


COMPONENT RESET_DELAY
	PORT
	(
		iCLK		:	 IN STD_LOGIC;
		oRESET		:	 OUT STD_LOGIC
	);
END COMPONENT;


component PLL1
	PORT
	(
		inclk0	: IN STD_LOGIC  := '0'; -- 50 MHZ
		c0		: OUT STD_LOGIC 		-- 18.433180 MHZ
	);
end component;


component PLL2
	PORT
	(
		inclk0	: IN STD_LOGIC  := '0';
		c0		: OUT STD_LOGIC 
	);
end component;


COMPONENT audio_codec_controller
	PORT
	(
		RESET				:	 IN STD_LOGIC;
		CLOCK				:	 IN STD_LOGIC;
		i2cClock20KHz		:	 IN STD_LOGIC;
		SCL					:	 OUT STD_LOGIC;
		SDA					:	 INOUT STD_LOGIC;
		dacLIN				:	 IN STD_LOGIC_VECTOR(15 DOWNTO 0);
		dacRIN				:	 IN STD_LOGIC_VECTOR(15 DOWNTO 0);
		adcLOUT				:	 OUT STD_LOGIC_VECTOR(15 DOWNTO 0);
		adcROUT				:	 OUT STD_LOGIC_VECTOR(15 DOWNTO 0);
		adcData				:	 IN STD_LOGIC;
		dacData				:	 OUT STD_LOGIC;
		RL_DATA_OUT_VALID	:	 OUT STD_LOGIC;
		audioClock			:	 IN STD_LOGIC;
		adcLRSelect			:	 OUT STD_LOGIC;
		dacLRSelect			:	 OUT STD_LOGIC;
		dacLRSelect_ACK		:	 OUT STD_LOGIC
	);
END COMPONENT;



--------------------------------------------------------------------------------------------



--------------------------------------- DECLARAÇÃO DE SINAIS -------------------------------
SIGNAL UNIDADE : STD_LOGIC_VECTOR(3 DOWNTO 0);
SIGNAL DEZENA  : STD_LOGIC_VECTOR(3 DOWNTO 0);
SIGNAL LCD_ON_1: STD_LOGIC;
SIGNAL LCD_BLON_1:STD_LOGIC;
SIGNAL LCD_D_1 : STD_LOGIC_VECTOR(7 DOWNTO 0) ;
SIGNAL LCD_RW_1: STD_LOGIC;
SIGNAL LCD_EN_1: STD_LOGIC;
SIGNAL LCD_RS_1: STD_LOGIC;
SIGNAL DLY_RST : STD_LOGIC;
SIGNAL SCL_SIG,AUDIO_CLOCK_SIG,CLOCK_50_DELAY,I2C_CLOCK20khz,RL_DATA_OUT_VALID_SIG : STD_LOGIC := '0';
SIGNAL adcLRC,adcdat,dacLRC,dacDat : STD_LOGIC := '0';
SIGNAL dacLIN_SIG,dacRIN_SIG,adcLOUT_SIG,adcROUT_SIG : STD_LOGIC_VECTOR(15 DOWNTO 0);

--adicionado por TD
signal fir_in		: signed(15 downto 0);
signal fir_out		: signed(15 downto 0);

signal RST			: std_logic;

signal dKEY			: std_logic_vector(3 downto 0);
signal dSW			: std_logic_vector(17  downto 0);

signal rx_valid_s	: std_logic;
signal rx_data_s	: std_logic_vector(7 downto 0);

signal word			: std_logic_vector(15 downto 0);
signal word_ready : std_logic;




--------------------------------------------------------------------------------------------

BEGIN

--------------------------------------- INSTANCIAÇÃO DE COMPONENETES -----------------------
INST_DISP0:DISPLAY7SEG
	PORT MAP
		(
			iDIG => UNIDADE(3 DOWNTO 0),
			oSEG => HEX0		
		);


INST_DISP1:DISPLAY7SEG
	PORT MAP
		(
			iDIG => DEZENA(3 DOWNTO 0),
			oSEG => HEX1		
		);

INST_DISP2:DISPLAY7SEG
	PORT MAP
		(
			iDIG => X"0",
			oSEG => HEX2		
		);

INST_DISP3:DISPLAY7SEG
	PORT MAP
		(
			iDIG => X"0",
			oSEG => HEX3		
		);

INST_DISP4:DISPLAY7SEG
	PORT MAP
		(
			iDIG => X"0",
			oSEG => HEX4		
		);
		
INST_DISP5:DISPLAY7SEG
	PORT MAP
		(
			iDIG => X"0",
			oSEG => HEX5		
		);
		
INST_DISP6:DISPLAY7SEG
	PORT MAP
		(
			iDIG => X"0",
			oSEG => HEX6		
		);
		
INST_DISP7:DISPLAY7SEG
	PORT MAP
		(
			iDIG => X"0",
			oSEG => HEX7		
		);

INST_TESTE_LCD:TESTE_LCD
	PORT MAP
	(
		--//	Host Side
		iCLK 	 => CLOCK_50,
		iRST_N	 => SW(17),--DLY_RST,
		--//	LCD Side
		LCD_DATA => LCD_D_1,
		LCD_RW	 => LCD_RW_1,
		LCD_EN	 => LCD_EN_1,
		LCD_RS	 => LCD_RS_1	
	);

INST_DELAY_RESET:RESET_DELAY
	PORT MAP	
	(
		iCLK	=> CLOCK_50, 
		oRESET	=> DLY_RST   
	);
RST <= not(DLY_RST) or not(KEY(1)); -- reset invertido adicionado por TD
PLL1_inst : PLL1 
	PORT MAP 
	(
		inclk0	 => CLOCK_50,        -- 50 MHZ
		c0	 	 => AUDIO_CLOCK_SIG  -- 12 MHZ
	);
	
PLL2_inst : PLL2 
	PORT MAP
	(
		inclk0	 => CLOCK_50,
		c0	 	 => I2C_CLOCK20khz
	);
	
AUDIO_CODEC_INST : AUDIO_CODEC_CONTROLLER	
	PORT MAP
	(
		RESET			=> DLY_RST,--SW(17),
		CLOCK			=> CLOCK_50,
		i2cClock20KHz	=> I2C_CLOCK20khz,
		SCL				=> SCL_SIG,
		SDA				=> I2C_SDAT,
		dacLIN			=> dacLIN_SIG,		--comentario de TD: escreve em dacLIN_SIG
		dacRIN			=> dacRIN_SIG,
		adcLOUT			=> adcLOUT_SIG,	--comentario de TD: le do codec e escreve em adcLOUT_SIG
		adcROUT			=> adcROUT_SIG,	--comentario de TD 
		adcData			=> adcDat,
		dacData			=> dacDat,
		RL_DATA_OUT_VALID	=>	 RL_DATA_OUT_VALID_SIG,
		audioClock		=> AUDIO_CLOCK_SIG,
		adcLRSelect		=> adcLRC,
		dacLRSelect		=> dacLRC,
		dacLRSelect_ACK	=> open

	);
fir : work.fir_trans port map(  --adicionado por TD
		clk			=> CLOCK_50,
		vld			=> RL_DATA_OUT_VALID_SIG,
		rst			=> RST,
		coef_in		=> signed(word),
		coef_wr		=> word_ready,
		sample_in	=> fir_in,
		sample_out	=> fir_out,
		uart_debug  => LEDR(15 downto 0)
		);
--	LEDR(15 downto 0) <= word;
	LEDR(16) <= KEY(1);
--	LEDR( 7 downto 0) <= rx_data_s; LEDR(8) <=DLY_RST;
	LEDR(17) <= RST;
  u_uart_top : work.uart_top
    port map (clock            => CLOCK_50,
              reset_n          => RST,
              uart_rx          => UART_RXD,
              uart_tx          => UART_TXD,
              uart_rts_n       => UART_RTS,
              uart_cts_n       => UART_CTS,
              rx_valid         => rx_valid_s,
              rx_data          => rx_data_s);
 
  u_word_rx : work.word_rx
    port map (clk                => CLOCK_50,
              rst                => RST,
              rx_valid	         => rx_valid_s,
              rx_data            => rx_data_s,
              word_ready         => word_ready,
              word               => word);

				  
				  
ksd : work.keys_sws_debounce_full port map(
		clk     => CLOCK_50,
		rst_n   => RST,
		key_in  => KEY,
		sw_in   => SW,
		key_out => dKEY,
		sw_out  => dSW
		);
---------------------------------------------------------------------------------------------

LCD_DATA <= LCD_D_1;
LCD_RW   <= LCD_RW_1;
LCD_EN   <= LCD_EN_1;
LCD_RS   <= LCD_RS_1; 
LCD_ON   <= '1';
LCD_BLON <= '0'; --//not supported;

-- send out the clocks
I2C_SCLK <= SCL_SIG;
AUD_BCLK <= NOT(AUDIO_CLOCK_SIG);
AUD_XCK  <= NOT(AUDIO_CLOCK_SIG);


-- output assignments
AUD_ADCLRCK <= adcLRC;
AUD_DACLRCK <= dacLRC;


--EX_IO(0) <= NOT(AUDIO_CLOCK_SIG);
--EX_IO(1) <= AUD_ADCDAT;
--EX_IO(2) <= dacDat;
--EX_IO(3) <= RL_DATA_OUT_VALID_SIG;
--EX_IO(4) <= dacLRC;


	PROCESS(DLY_RST)
	BEGIN
		IF (DLY_RST) = '0' THEN
			adcDat <= '0';
			AUD_DACDAT <= '0';
			dacLIN_SIG <= (OTHERS => '0');
			dacRIN_SIG <= (OTHERS => '0');
		ELSE
		-- output from adc
			adcDat <= AUD_ADCDAT;
		-- input of dac
			AUD_DACDAT  <= dacDat;
		--- BYPASS ----
		--	dacLIN_SIG <= adcLOUT_SIG;
		--	dacRIN_SIG <= adcROUT_SIG;
		
		-- TD adicionou o FIR e comentou o BYPASS
		
		--FIR
		fir_in	  <= signed(adcLOUT_SIG);
		dacLIN_SIG <= std_logic_vector(fir_out);
		dacRIN_SIG <= adcROUT_SIG;
		---------------
		END IF;
	END PROCESS;


 	--parte excluida por TD: PROCESS(CLOCK_50,SW(17))

END ARCHITECTURE;