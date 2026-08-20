#!/usr/bin/env python3

import serial
import time

PORTA = "/dev/ttyUSB0"   # Altere conforme necessário
BAUD = 57600

try:
    with serial.Serial(PORTA, BAUD, timeout=1, ctsrts=True) as ser:
        #for i in range(22):
            byte  = 0x3F
            bytee = 0xFF
            ser.write(bytes([byte]))
            time.sleep(0.02)
            ser.write(bytes([bytee]))
            print(f"Enviado: 0x{byte:02X}")
            time.sleep(0.02)

except Exception as e:
    print(f"Erro: {e}")

'''
sudo /bin/python3 "/home/linse/Documentos/Tulio/codes/DE2_exemplos/DE2_115 (fir_uart)(copia)/tulio_srcs/fir_trans/uart_terminal.py"
'''