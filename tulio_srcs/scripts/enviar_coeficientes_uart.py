#!/usr/bin/env python3
"""Gera coeficientes de um filtro FIR e envia via UART."""

import serial
from scipy.signal import firwin
import time

'''
sudo /bin/python3 "/home/linse/Documentos/Tulio/codes/DE2_exemplos/DE2_115 (fir_uart)(copia)/tulio_srcs/fir_trans/enviar_coeficientes_uart.py"
'''

# ============================== CONFIGURAÇÃO ==============================

PORTA = "/dev/ttyUSB0"
BAUD  = 57600

FILTER_SEL = "00"   # "00"=passa-baixas, "01"=passa-altas, "10"=passa-faixa, "11"=rejeita-faixa

FS  = 48000.0       # frequência de amostragem (Hz)
FC1 = 6000.0        # frequência de corte 1 (Hz)
FC2 = 8000.0        # frequência de corte 2 (Hz), usada só em passa-faixa/rejeita-faixa

NUM_TAPS = 199        # número de coeficientes (ímpar para passa-altas/rejeita-faixa)
NUM_REGS = 201        # número total de registradores no hardware (diferença NUM_REGS-NUM_TAPS = zeros enviados)

SENTINEL = 0x7FFF

# ============================================================================


def gerar_coeficientes():
    nyquist = FS / 2.0

    if FILTER_SEL == "00":
        coefs = firwin(NUM_TAPS, FC1 / nyquist, pass_zero=True)
    elif FILTER_SEL == "01":
        coefs = firwin(NUM_TAPS, FC1 / nyquist, pass_zero=False)
    elif FILTER_SEL == "10":
        coefs = firwin(NUM_TAPS, [FC1 / nyquist, FC2 / nyquist], pass_zero=False)
    elif FILTER_SEL == "11":
        coefs = firwin(NUM_TAPS, [FC1 / nyquist, FC2 / nyquist], pass_zero=True)
    else:
        raise ValueError(f"FILTER_SEL inválido: {FILTER_SEL}")

    # converte para inteiro Q1.15 (16 bits, complemento de dois)
    coefs_int = [int(round(c * 32768)) for c in coefs]
    coefs_int = [max(-32768, min(32767, c)) for c in coefs_int]  # satura, por segurança

    # completa com zeros até NUM_REGS valores no total
    if NUM_REGS < NUM_TAPS:
        raise ValueError(f"NUM_REGS ({NUM_REGS}) não pode ser menor que NUM_TAPS ({NUM_TAPS})")
    coefs_int += [0] * (NUM_REGS - NUM_TAPS)

    return coefs_int


def valor_para_bytes(valor):
    if valor < 0:
        valor += 1 << 16
    byte_alto = (valor >> 8) & 0xFF
    byte_baixo = valor & 0xFF
    return [byte_alto, byte_baixo]  # byte mais significativo primeiro


def main():
    coefs_int = gerar_coeficientes()
    print(f"Coeficientes ativos: {NUM_TAPS}  |  Registradores totais: {NUM_REGS}  |  Zeros enviados: {NUM_REGS - NUM_TAPS}")
    print(f"Valores ({len(coefs_int)}): {coefs_int}")

    # envia em ordem inversa (ver observação abaixo)
    ordem_envio = list(coefs_int)
    ordem_envio = [SENTINEL] + ordem_envio
    #ordem_envio = list(reversed(coefs_int))

    # [FIX-RTSCTS] rtscts=True habilita o flow control por hardware:
    # o driver do adaptador USB-serial passa a monitorar o pino CTS
    # (ligado ao RTS de saída da FPGA) e pausa a transmissão sozinho
    # sempre que a FPGA sinalizar "busy". Isso substitui o time.sleep()
    # que estava comentado abaixo.
    with serial.Serial(PORTA, BAUD, timeout=1, rtscts=True) as ser:
        for valor in ordem_envio:
            for byte in valor_para_bytes(valor):
                ser.write(bytes([byte]))   # um byte por vez
                #time.sleep(0.02)          # [FIX-RTSCTS] não é mais necessário
                #print(f"  byte enviado: 0x{byte:02X}")
            #print(f"Enviado valor: {valor}")
        ser.flush()   # [FIX-RTSCTS] garante que o buffer esvazie antes de fechar a porta

    print("Envio concluído.")


if __name__ == "__main__":
    main()

'''
sudo /bin/python3 "/home/linse/Documentos/Tulio/codes/DE2_exemplos/DE2_115 (fir_uart)(copia)/tulio_srcs/fir_trans/enviar_coeficientes_uart.py"
'''