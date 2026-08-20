#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import numpy as np
from scipy.signal import firwin, freqz
from PIL import Image, ImageTk

# sudo /bin/python3 "/home/linse/Documentos/Tulio/codes/DE2_exemplos/DE2_115 (fir_uart_ctsrts)/tulio_srcs/fir_trans/gui_plot.py"

# --- IMPORTAÇÕES DO MATPLOTLIB PARA TKINTER ---
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ============================== CONFIGURAÇÃO GLOBAL ==============================
FILTER_SEL = "11"     # "00"=passa-baixas, "01"=passa-altas, "10"=passa-faixa, "11"=rejeita-faixa
NUM_REGS   = 256      # Número total de registradores no hardware FPGA
SENTINEL   = 0x7FFF   # Marcador de início de pacote
# =================================================================================


# --- FUNÇÕES AUXILIARES DE PORTA UART ---
def listar_portas_uart():
    portas_brutas = serial.tools.list_ports.comports()
    portas_filtradas = [
        port.device for port in portas_brutas
        if any(term in port.device for term in ["ttyUSB", "ttyACM", "COM"])
    ]
    return portas_filtradas if portas_filtradas else ["Nenhuma porta USB"]

def atualizar_lista_portas():
    portas = listar_portas_uart()
    combo_porta['values'] = portas
    if portas and combo_porta.get() not in portas:
        combo_porta.set(portas[0])


# --- SELEÇÃO DO FILTRO ---
def selecionar_filtro(botao_clicado, codigo_filtro, nome_filtro):
    global FILTER_SEL
    FILTER_SEL = codigo_filtro

    for btn in todos_botoes:
        btn.config(relief="raised", bd=2, bg="#f0f0f0", fg="black")

    botao_clicado.config(relief="sunken", bd=3, bg="#007ACC", fg="white")
    texto_principal.config(text=f"Filter selected: {nome_filtro} ({codigo_filtro})", fg="black")

    if codigo_filtro in ["10", "11"]:
        spin_fc2.config(state="normal")
    else:
        spin_fc2.config(state="disabled")


# --- CÁLCULO DOS COEFICIENTES ---
def gerar_coeficientes(filter_sel, fs, fc1, fc2, num_taps, num_regs):
    nyquist = fs / 2.0

    if fc1 >= nyquist:
        raise ValueError(f"FC1 ({fc1} Hz) deve ser menor que Nyquist ({nyquist} Hz)!")

    if filter_sel in ["10", "11"]:
        if fc2 >= nyquist:
            raise ValueError(f"FC2 ({fc2} Hz) deve ser menor que Nyquist ({nyquist} Hz)!")
        if fc1 >= fc2:
            raise ValueError(f"FC1 ({fc1} Hz) deve ser menor que FC2 ({fc2} Hz)!")

    # 1. Calcula coeficientes ativos (puros)
    if filter_sel == "00":
        coefs_puros = firwin(num_taps, fc1 / nyquist, pass_zero=True)
    elif filter_sel == "01":
        coefs_puros = firwin(num_taps, fc1 / nyquist, pass_zero=False)
    elif filter_sel == "10":
        coefs_puros = firwin(num_taps, [fc1 / nyquist, fc2 / nyquist], pass_zero=False)
    elif filter_sel == "11":
        coefs_puros = firwin(num_taps, [fc1 / nyquist, fc2 / nyquist], pass_zero=True)
    else:
        raise ValueError(f"FILTER_SEL inválido: {filter_sel}")

    # 2. Converte para inteiro Q1.15
    coefs_int = [int(round(c * 32768)) for c in coefs_puros]
    coefs_int = [max(-32768, min(32767, c)) for c in coefs_int]

    if num_regs < num_taps:
        raise ValueError(f"NUM_REGS ({num_regs}) não pode ser menor que NUM_TAPS ({num_taps})!")
    
    # Preenche com zeros para os registradores
    coefs_int_padded = coefs_int + [0] * (num_regs - num_taps)
    
    return coefs_puros, coefs_int_padded


def valor_para_bytes(valor):
    if valor < 0:
        valor += 1 << 16
    return [(valor >> 8) & 0xFF, valor & 0xFF]


# --- ATUALIZAR GRÁFICO FREQZ NA GUI ---
def desenhar_grafico_freqz(coefs, fs):
    w, h = freqz(b=coefs, a=1.0, worN=1024, fs=fs)
    magnitude_db = 20 * np.log10(np.abs(h) + 1e-12)  # 1e-12 evita log de zero

    ax.clear()
    ax.plot(w, magnitude_db, color='#007ACC', linewidth=1.5)
    ax.set_title("Frequency Response (Magnitude)", fontsize=9, fontweight='bold')
    ax.set_xlabel("Frequency (Hz)", fontsize=8)
    ax.set_ylabel("Gain (dB)", fontsize=8)
    ax.set_ylim(-80, 5)
    ax.set_xlim(0, fs / 2.0)
    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    canvas.draw()


# --- AÇÃO DO BOTÃO APPLY FILTER ---
def aplicar_e_enviar_filtro():
    try:
        taps = int(spin_taps.get())
        fs = float(spin_fs.get())
        fc1 = float(spin_fc1.get())
        fc2 = float(spin_fc2.get()) if FILTER_SEL in ["10", "11"] else 0.0
        porta = combo_porta.get()
        baud = int(spin_baud.get())

        # 1. Gera coeficientes puros (para o gráfico) e inteiros com zeros (para a FPGA)
        coefs_puros, coefs_int = gerar_coeficientes(FILTER_SEL, fs, fc1, fc2, taps, NUM_REGS)

        # 2. Desenha/Atualiza o gráfico na interface
        desenhar_grafico_freqz(coefs_puros, fs)

        if porta in ["Nenhuma porta USB", "Sem portas USB", ""]:
            messagebox.showwarning("Porta Inválida", "Por favor, selecione uma porta UART válida!")
            return

        # 3. Transmite via UART
        ordem_envio = [SENTINEL] + coefs_int
        with serial.Serial(porta, baud, timeout=1, rtscts=True) as ser:
            for valor in ordem_envio:
                for byte in valor_para_bytes(valor):
                    ser.write(bytes([byte]))
            ser.flush()

        texto_principal.config(
            text=f"✅ Coeficientes enviados para {porta} com sucesso!",
            fg="#006600"
        )

    except ValueError as e:
        messagebox.showerror("Erro nos Parâmetros", f"Erro nos valores informados:\n{e}")
    except serial.SerialException as e:
        messagebox.showerror("Erro UART", f"Falha ao comunicar com a porta {porta}.\n\nDetalhes: {e}")


# ============================== INTERFACE GRÁFICA ==============================

janela = tk.Tk()
janela.title("FIR Filter Generator & UART Transmitter")
janela.config(padx=15, pady=10)

# --- COLUNA DA ESQUERDA (CONFIGURAÇÕES) ---
frame_esquerda = tk.Frame(janela)
frame_esquerda.grid(row=0, column=0, sticky="nw", padx=(0, 10))

# Logo
try:
    PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
    imagem_original = Image.open(os.path.join(PASTA_ATUAL, "logo-linse.png"))
    imagem_redimensionada = imagem_original.resize((280, 120))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
    label_imagem = tk.Label(frame_esquerda, image=imagem_tk)
    label_imagem.image = imagem_tk
    label_imagem.grid(row=0, column=0, columnspan=2, pady=5)
except Exception:
    label_imagem = tk.Label(frame_esquerda, text="[ LINSE LOGO ]", font=("Arial", 14, "bold"))
    label_imagem.grid(row=0, column=0, columnspan=2, pady=10)

# Status
texto_principal = tk.Label(frame_esquerda, text="Select the filter:", font=("Arial", 10, "bold"), width=42, anchor="w")
texto_principal.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 5))

# Botões dos Filtros
frame_botoes = tk.Frame(frame_esquerda)
frame_botoes.grid(row=2, column=0, sticky="nw", padx=(0, 5))

low_pass_button = tk.Button(frame_botoes, text="Low pass", width=12, command=lambda: selecionar_filtro(low_pass_button, "00", "Low pass"))
low_pass_button.pack(pady=3)

high_pass_button = tk.Button(frame_botoes, text="High pass", width=12, command=lambda: selecionar_filtro(high_pass_button, "01", "High pass"))
high_pass_button.pack(pady=3)

range_pass_button = tk.Button(frame_botoes, text="Range pass", width=12, command=lambda: selecionar_filtro(range_pass_button, "10", "Range pass"))
range_pass_button.pack(pady=3)

rejects_range_button = tk.Button(frame_botoes, text="Rejects range", width=12, command=lambda: selecionar_filtro(rejects_range_button, "11", "Rejects range"))
rejects_range_button.pack(pady=3)

todos_botoes = [low_pass_button, high_pass_button, range_pass_button, rejects_range_button]

# Parâmetros
frame_params = tk.LabelFrame(frame_esquerda, text=" Parameters ", font=("Arial", 8, "bold"), padx=8, pady=5)
frame_params.grid(row=2, column=1, sticky="nsew")

tk.Label(frame_params, text="NUM_TAPS:", font=("Arial", 8, "bold")).grid(row=0, column=0, sticky="w")
spin_taps = tk.Spinbox(frame_params, from_=1, to=255, increment=2, width=10, font=("Arial", 8))
spin_taps.delete(0, "end"); spin_taps.insert(0, "199")
spin_taps.grid(row=1, column=0, sticky="w", pady=(0, 3))

tk.Label(frame_params, text="FS (Hz):", font=("Arial", 8, "bold")).grid(row=2, column=0, sticky="w")
spin_fs = tk.Spinbox(frame_params, from_=1000, to=192000, increment=1000, width=10, font=("Arial", 8))
spin_fs.delete(0, "end"); spin_fs.insert(0, "48000.0")
spin_fs.grid(row=3, column=0, sticky="w", pady=(0, 3))

tk.Label(frame_params, text="FC1 (Hz):", font=("Arial", 8, "bold")).grid(row=4, column=0, sticky="w")
spin_fc1 = tk.Spinbox(frame_params, from_=100, to=96000, increment=500, width=10, font=("Arial", 8))
spin_fc1.delete(0, "end"); spin_fc1.insert(0, "6000.0")
spin_fc1.grid(row=5, column=0, sticky="w")

tk.Label(frame_params, text="PORTA:", font=("Arial", 8, "bold")).grid(row=0, column=1, sticky="w", padx=(5,0))
frame_porta = tk.Frame(frame_params)
frame_porta.grid(row=1, column=1, sticky="w", padx=(5,0), pady=(0, 3))

portas_encontradas = listar_portas_uart()
combo_porta = ttk.Combobox(frame_porta, values=portas_encontradas, width=9, font=("Arial", 8), state="readonly")
combo_porta.pack(side="left")
if "/dev/ttyUSB0" in portas_encontradas: combo_porta.set("/dev/ttyUSB0")
elif portas_encontradas: combo_porta.set(portas_encontradas[0])

btn_refresh_porta = tk.Button(frame_porta, text="🔄", command=atualizar_lista_portas, font=("Arial", 6), width=2)
btn_refresh_porta.pack(side="left", padx=(2, 0))

tk.Label(frame_params, text="BAUD Rate:", font=("Arial", 8, "bold")).grid(row=2, column=1, sticky="w", padx=(5,0))
spin_baud = tk.Spinbox(frame_params, values=(9600, 19200, 38400, 57600, 115200), width=10, font=("Arial", 8))
spin_baud.delete(0, "end"); spin_baud.insert(0, "57600")
spin_baud.grid(row=3, column=1, sticky="w", padx=(5,0), pady=(0, 3))

tk.Label(frame_params, text="FC2 (Hz):", font=("Arial", 8, "bold")).grid(row=4, column=1, sticky="w", padx=(5,0))
spin_fc2 = tk.Spinbox(frame_params, from_=100, to=96000, increment=500, width=10, font=("Arial", 8))
spin_fc2.delete(0, "end"); spin_fc2.insert(0, "8000.0")
spin_fc2.grid(row=5, column=1, sticky="w", padx=(5,0))

# Botão Apply
btn_apply = tk.Button(
    frame_esquerda, text="🚀 Apply Filter & Plot", font=("Arial", 10, "bold"),
    bg="#28a745", fg="white", activebackground="#218838", activeforeground="white",
    pady=6, command=aplicar_e_enviar_filtro
)
btn_apply.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 0))


# --- COLUNA DA DIREITA (CONTAINER DO GRÁFICO) ---
frame_grafico = tk.LabelFrame(janela, text=" Frequency Response ", font=("Arial", 9, "bold"), padx=5, pady=5)
frame_grafico.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

# Cria Figura do Matplotlib e adiciona ao Tkinter
fig = Figure(figsize=(5.2, 3.8), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Seleciona filtro padrão inicial
selecionar_filtro(rejects_range_button, "11", "Rejects range")

# Plota um gráfico inicial vazio ao abrir a interface
desenhar_grafico_freqz(firwin(199, [6000.0/24000.0, 8000.0/24000.0], pass_zero=True), 48000.0)

janela.mainloop()