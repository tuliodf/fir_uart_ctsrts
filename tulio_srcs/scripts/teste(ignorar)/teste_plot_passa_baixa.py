import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz, firwin

# 1. Definições do filtro
fs = 48000.0  # Frequência de amostragem em Hz
fc = 5000.0   # Frequência de corte em Hz
taps = 255    # Número de coeficientes (ímpar)

# Cria um array de coeficientes (FIR Passa-Baixas como exemplo)
coefs = firwin(taps, fc / (fs / 2.0), pass_zero=True)

# -------------------------------------------------------------------------
# 2. Uso do FREQZ
# -------------------------------------------------------------------------
# b = coefs (numerador / coefs do FIR)
# a = 1.0   (denominador / para filtro FIR é sempre 1.0)
# worN = 2048 (quantidade de pontos de frequência para calcular)
# fs = fs   (passando a freq. de amostragem, 'w' já retorna em Hz)
w, h = freqz(b=coefs, a=1.0, worN=2048, fs=fs)

# 3. Converte a magnitude complexa 'h' para escala em Decibéis (dB)
magnitude_db = 20 * np.log10(np.abs(h))

# 4. Plota o gráfico da Resposta em Frequência
plt.figure(figsize=(9, 4.5))
plt.plot(w, magnitude_db, color='blue', linewidth=1.5, label='Magnitude')

# Formatação do Gráfico
plt.title('Resposta em Frequência do Filtro (Magnitude)', fontsize=12, fontweight='bold')
plt.xlabel('Frequência (Hz)', fontsize=10)
plt.ylabel('Ganho (dB)', fontsize=10)
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.ylim(-80, 5)  # Limita o eixo Y para visualizar bem a banda de rejeição
plt.xlim(0, fs / 2)  # Mostra até a Frequência de Nyquist

plt.tight_layout()
plt.show()