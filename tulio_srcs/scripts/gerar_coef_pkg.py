"""
gerar_coeficientes.py
----------------------
Gera coeficientes de filtro FIR (passa-baixas, passa-altas, passa-faixa,
rejeita-faixa) de acordo com uma variável de seleção de 2 bits, converte
para ponto fixo Q1.15 (16 bits com sinal) e escreve um pacote VHDL
(coef_pkg.vhd) no mesmo diretório deste script.

Mapeamento da variável de seleção (FILTER_SEL):
    "00" -> passa-baixas   (usa FC1 como frequência de corte)
    "01" -> passa-altas    (usa FC1 como frequência de corte)
    "10" -> passa-faixa    (usa FC1 e FC2 como bordas da banda)
    "11" -> rejeita-faixa  (usa FC1 e FC2 como bordas da banda)

Ajuste os parâmetros na seção CONFIGURAÇÃO abaixo conforme seu projeto
(ex: Fs = 48000 Hz para o WM8731 em modo Normal/48kHz).
"""

import os
import numpy as np
from scipy.signal import firwin

# ============================== CONFIGURAÇÃO ==============================

FILTER_SEL = "00"      # "00"=passa-baixas, "01"=passa-altas, "10"=passa-faixa, "11"=rejeita-faixa

FS = 48000.0            # Frequência de amostragem real (Hz) — deve bater com o SR configurado no R8 do codec
FC1 = 2000.0             # Frequência de corte 1 (Hz) — usada em todos os modos
FC2 = 5000.0             # Frequência de corte 2 (Hz) — usada só em passa-faixa/rejeita-faixa

NUM_TAPS = 5            # Número de coeficientes (ordem do filtro + 1). Deve ser ímpar para band-stop/high-pass com firwin.
num_taps_plusone = NUM_TAPS + 1

COEF_WIDTH = 16          # Largura em bits dos coeficientes de saída (ponto fixo)
FRAC_BITS = COEF_WIDTH - 1  # Q1.15 -> 1 bit de sinal + 15 bits fracionários

# ============================================================================


def gerar_coeficientes(filter_sel: str, fs: float, fc1: float, fc2: float, num_taps: int) -> np.ndarray:
    """Gera os coeficientes em ponto flutuante conforme o tipo de filtro selecionado."""
    nyquist = fs / 2.0

    if filter_sel == "00":
        # Passa-baixas
        coefs = firwin(num_taps, fc1 / nyquist, pass_zero=True)
        tipo = "Passa-Baixas"

    elif filter_sel == "01":
        # Passa-altas (exige num_taps ímpar)
        if num_taps % 2 == 0:
            raise ValueError("NUM_TAPS deve ser ímpar para filtro passa-altas.")
        coefs = firwin(num_taps, fc1 / nyquist, pass_zero=False)
        tipo = "Passa-Altas"

    elif filter_sel == "10":
        # Passa-faixa
        coefs = firwin(num_taps, [fc1 / nyquist, fc2 / nyquist], pass_zero=False)
        tipo = "Passa-Faixa"

    elif filter_sel == "11":
        # Rejeita-faixa (exige num_taps ímpar)
        if num_taps % 2 == 0:
            raise ValueError("NUM_TAPS deve ser ímpar para filtro rejeita-faixa.")
        coefs = firwin(num_taps, [fc1 / nyquist, fc2 / nyquist], pass_zero=True)
        tipo = "Rejeita-Faixa"

    else:
        raise ValueError(f"FILTER_SEL inválido: '{filter_sel}'. Use '00', '01', '10' ou '11'.")

    print(f"Tipo de filtro gerado : {tipo}")
    print(f"Fs                    : {fs} Hz")
    print(f"FC1                   : {fc1} Hz")
    if filter_sel in ("10", "11"):
        print(f"FC2                   : {fc2} Hz")
    print(f"Número de coeficientes: {len(coefs)}")

    return coefs, tipo


def converter_ponto_fixo(coefs: np.ndarray, frac_bits: int, width: int) -> list:
    """Converte coeficientes float [-1,1) para inteiros Q1.(width-1) com saturação."""
    escala = 2 ** frac_bits
    val_max = 2 ** (width - 1) - 1
    val_min = -(2 ** (width - 1))

    inteiros = np.round(coefs * escala).astype(int)
    inteiros = np.clip(inteiros, val_min, val_max)

    if np.any(np.round(coefs * escala) > val_max) or np.any(np.round(coefs * escala) < val_min):
        print("AVISO: um ou mais coeficientes saturaram no formato de ponto fixo escolhido.")

    return inteiros.tolist()


def escrever_vhdl(coefs_int: list, tipo: str, width: int, frac_bits: int, fs: float,
                   fc1: float, fc2: float, filter_sel: str, caminho_saida: str):
    """Escreve o pacote coefs_pkg.vhd com os coeficientes como constantes."""
    num_taps = len(coefs_int)

    linhas = []
    linhas.append("-------------------------------------------------------------------------------")
    linhas.append("-- coefs_pkg.vhd")
    linhas.append("-- Gerado automaticamente por fir_generator.py -- NAO EDITAR MANUALMENTE")
    linhas.append(f"-- Tipo de filtro   : {tipo} (FILTER_SEL = \"{filter_sel}\")")
    linhas.append(f"-- Fs               : {fs} Hz")
    linhas.append(f"-- FC1              : {fc1} Hz")
    if filter_sel in ("10", "11"):
        linhas.append(f"-- FC2              : {fc2} Hz")
    linhas.append(f"-- Formato          : Q1.{frac_bits} (signed, complemento de dois)")
    linhas.append("-------------------------------------------------------------------------------")
    linhas.append("")
    linhas.append("library ieee;")
    linhas.append("use ieee.std_logic_1164.all;")
    linhas.append("use ieee.numeric_std.all;")
    linhas.append("")
    linhas.append("package coefs_pkg is")
    linhas.append("")
    linhas.append(f"constant ntaps : integer := {num_taps_plusone};--{NUM_TAPS} taps ativos")
    linhas.append(f"constant dataw : integer := {width};")
    linhas.append("")
    linhas.append("type tap_array is array (0 to ntaps-1) of signed(dataw-1 downto 0);")
    linhas.append("type mult_out_array is array (0 to ntaps-1) of signed(2*dataw-1 downto 0);")
    linhas.append("")
    linhas.append("constant coefs : tap_array := (")

    # Adiciona cada coeficiente com vírgula no final
    for i, val in enumerate(coefs_int):
        linhas.append(f'    {i:3d} => to_signed({val}, dataw),')

    # Adiciona a cláusula others para zerar as posições restantes (se houver)
    linhas.append("    others => to_signed(0, dataw)")

    linhas.append(");")
    linhas.append("")
    linhas.append("end package coefs_pkg;")
    linhas.append("")

    with open(caminho_saida, "w") as f:
        f.write("\n".join(linhas))

    print(f"\nArquivo gerado: {caminho_saida}")


def main():
    coefs_float, tipo = gerar_coeficientes(FILTER_SEL, FS, FC1, FC2, NUM_TAPS)
    coefs_int = converter_ponto_fixo(coefs_float, FRAC_BITS, COEF_WIDTH)

    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_saida = os.path.join(diretorio_script, "coefs_pkg.vhd")

    escrever_vhdl(coefs_int, tipo, COEF_WIDTH, FRAC_BITS, FS, FC1, FC2, FILTER_SEL, caminho_saida)


if __name__ == "__main__":
    main()