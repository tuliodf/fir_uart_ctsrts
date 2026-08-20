#!/usr/bin/env python3
import os
import time
import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
from scipy.signal import firwin, freqz
from PIL import Image, ImageTk

# sudo /bin/python3 "/home/linse/Documentos/Tulio/codes/DE2_exemplos/DE2_115 (fir_uart_ctsrts)/tulio_srcs/fir_trans/bora.py"
#Coeficiente texto principal tk.Label Parameters Filter 201 Apply taps to

# ============================== CONFIGURAÇÃO GLOBAL ==============================
FILTER_SEL = "00"     # "00"=passa-baixas, "01"=passa-altas, "10"=passa-faixa, "11"=rejeita-faixa
NUM_REGS   = 256      # Número total de registradores no hardware FPGA
SENTINEL   = 0x7FFF   # Marcador de início de pacote
# =================================================================================


# --- FUNÇÃO PARA DETECTAR PORTAS UART ---
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


# --- FUNÇÃO PARA TRATAR A SELEÇÃO DO FILTRO ---
def selecionar_filtro(botao_clicado, codigo_filtro, nome_filtro):
    global FILTER_SEL
    FILTER_SEL = codigo_filtro

    # 1. Reseta o visual dos botões
    for btn in todos_botoes:
        btn.config(relief="raised", bd=2, bg="#f0f0f0", fg="black")

    # 2. Destaca o botão selecionado
    botao_clicado.config(relief="sunken", bd=3, bg="#007ACC", fg="white")

    # 3. Atualiza o texto de status
    #texto_principal.config(text=f"Filter selected: {nome_filtro} ({codigo_filtro})", fg="black")

    # 4. Habilita/Desabilita FC2
    if codigo_filtro in ["10", "11"]:
        spin_fc2.config(state="normal")
    else:
        spin_fc2.config(state="disabled")


# --- CÁLCULO DOS COEFICIENTES E FORMATO Q1.15 ---
def gerar_coeficientes(filter_sel, fs, fc1, fc2, num_taps, num_regs):
    nyquist = fs / 2.0

    # Validações de Frequência de Nyquist
    if fc1 >= nyquist:
        raise ValueError(f"FC1 ({fc1} Hz) deve ser menor que Nyquist ({nyquist} Hz)!")

    if filter_sel in ["10", "11"]:
        if fc2 >= nyquist:
            raise ValueError(f"FC2 ({fc2} Hz) deve ser menor que Nyquist ({nyquist} Hz)!")
        if fc1 >= fc2:
            raise ValueError(f"FC1 ({fc1} Hz) deve ser menor que FC2 ({fc2} Hz)!")

    # Cálculo dos coeficientes flutuantes
    if filter_sel == "00":
        coefs = firwin(num_taps, fc1 / nyquist, pass_zero=True)
    elif filter_sel == "01":
        coefs = firwin(num_taps, fc1 / nyquist, pass_zero=False)
    elif filter_sel == "10":
        coefs = firwin(num_taps, [fc1 / nyquist, fc2 / nyquist], pass_zero=False)
    elif filter_sel == "11":
        coefs = firwin(num_taps, [fc1 / nyquist, fc2 / nyquist], pass_zero=True)
    else:
        raise ValueError(f"FILTER_SEL inválido: {filter_sel}")

    # Converte para inteiro Q1.15 (16 bits em complemento de dois)
    coefs_int = [int(round(c * 32768)) for c in coefs]
    coefs_int = [max(-32768, min(32767, c)) for c in coefs_int]  # Saturação por segurança

    # Preenche com zeros até completar NUM_REGS
    if num_regs < num_taps:
        raise ValueError(f"NUM_REGS ({num_regs}) não pode ser menor que NUM_TAPS ({num_taps})!")
    
    coefs_int += [0] * (num_regs - num_taps)
    return coefs_int


def valor_para_bytes(valor):
    if valor < 0:
        valor += 1 << 16
    byte_alto = (valor >> 8) & 0xFF
    byte_baixo = valor & 0xFF
    return [byte_alto, byte_baixo]  # Big-Endian


# --- AÇÃO DO BOTÃO "APPLY FILTER" (ENVIO UART) ---
def aplicar_e_enviar_filtro():
    try:
        taps = int(spin_taps.get())
        fs = float(spin_fs.get())
        fc1 = float(spin_fc1.get())
        fc2 = float(spin_fc2.get()) if FILTER_SEL in ["10", "11"] else 0.0
        porta = combo_porta.get()
        baud = int(spin_baud.get())

        if porta in ["Nenhuma porta USB", "Sem portas USB", ""]:
            messagebox.showwarning("Porta Inválida", "Por favor, selecione uma porta UART válida!")
            return

        # 1. Gera os coeficientes Q1.15201
        coefs_int = gerar_coeficientes(FILTER_SEL, fs, fc1, fc2, taps, NUM_REGS)

        # 2. Insere a Sentinela no início
        ordem_envio = [SENTINEL] + coefs_int

        print(f"\n=== TRANSMITINDO VIA UART ===")
        print(f"Porta: {porta} | Baud Rate: {baud}")
        print(f"Tipo: {FILTER_SEL} | TAPs Ativos: {taps} | Total Registradores: {NUM_REGS}")
        print(f"Valores ({len(ordem_envio)}): {ordem_envio}")

        # 3. Transmite com controle de fluxo RTS/CTS habilitado
        with serial.Serial(porta, baud, timeout=1, rtscts=True) as ser:
            for valor in ordem_envio:
                for byte in valor_para_bytes(valor):
                    ser.write(bytes([byte]))
            ser.flush()

        texto_principal.config(
            text=f"✅ Coeficientes enviados para {porta} com sucesso!",
            fg="#006600"
        )
        messagebox.showinfo("Sucesso", f"Filtro transmitido com sucesso para a FPGA via {porta}!")

    except ValueError as e:
        messagebox.showerror("Erro nos Parâmetros", f"Erro nos valores informados:\n{e}")
    except serial.SerialException as e:
        messagebox.showerror("Erro de Transmissão UART", f"Falha ao comunicar com a porta {porta}.\n\nDetalhes: {e}")
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")


# ============================== INTERFACE GRÁFICA ==============================

janela = tk.Tk()
janela.title("FIR_generator_GUI")
janela.config(padx=15, pady=10)

# 1. Imagem
try:
    PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
    imagem_original = Image.open(os.path.join(PASTA_ATUAL, "logo-linse.png"))
    imagem_redimensionada = imagem_original.resize((300, 135))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
    label_imagem = tk.Label(janela, image=imagem_tk)
    label_imagem.image = imagem_tk
    label_imagem.grid(row=0, column=0, columnspan=2, pady=5)
except Exception:
    label_imagem = tk.Label(janela, text="[ LINSE LOGO ]", font=("Arial", 16, "bold"))
    label_imagem.grid(row=0, column=0, columnspan=2, pady=10)

# 2. Texto de Status
texto_principal = tk.Label(janela, text="FIR filter generator GUI:", font=("Arial", 11, "bold"), width=55, anchor="w")
texto_principal.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 5))

# 3. Painel de Seleção do Filtro
frame_botoes = tk.Frame(janela)
frame_botoes.grid(row=2, column=0, sticky="nw", padx=(0, 10))

low_pass_button = tk.Button(
    frame_botoes, text="Passa Baixas", width=13,
    command=lambda: selecionar_filtro(low_pass_button, "00", "Low pass")
)
low_pass_button.pack(pady=4)

high_pass_button = tk.Button(
    frame_botoes, text="Passa Altas", width=13,
    command=lambda: selecionar_filtro(high_pass_button, "01", "High pass")
)
high_pass_button.pack(pady=4)

range_pass_button = tk.Button(
    frame_botoes, text="Passa Faixa", width=13,
    command=lambda: selecionar_filtro(range_pass_button, "10", "Range pass")
)
range_pass_button.pack(pady=4)

rejects_range_button = tk.Button(
    frame_botoes, text="Rejeita Faixa", width=13,
    command=lambda: selecionar_filtro(rejects_range_button, "11", "Rejects range")
)
rejects_range_button.pack(pady=4)

todos_botoes = [low_pass_button, high_pass_button, range_pass_button, rejects_range_button]

# 4. Painel de Parâmetros
frame_params = tk.LabelFrame(janela, text=" Parâmetros ", font=("Arial", 9, "bold"), padx=10, pady=5)
frame_params.grid(row=2, column=1, sticky="nsew")

# --- Coluna Interna 0 ---
MAX_COEFS = NUM_REGS-1
tk.Label(frame_params, text="NUM_TAPS:", font=("Arial", 8, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 10))
spin_taps = tk.Spinbox(frame_params, from_=1, to=MAX_COEFS, increment=2, width=13, font=("Arial", 9))
spin_taps.delete(0, "end")
spin_taps.insert(0, MAX_COEFS)
spin_taps.grid(row=1, column=0, sticky="w", pady=(0, 5), padx=(0, 10))

tk.Label(frame_params, text="FS (Hz):", font=("Arial", 8, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 10))
spin_fs = tk.Spinbox(frame_params, from_=1000, to=192000, increment=1000, width=13, font=("Arial", 9))
spin_fs.delete(0, "end")
spin_fs.insert(0, "48000.0")
spin_fs.grid(row=3, column=0, sticky="w", pady=(0, 5), padx=(0, 10))

tk.Label(frame_params, text="FC1 (Hz):", font=("Arial", 8, "bold")).grid(row=4, column=0, sticky="w", padx=(0, 10))
spin_fc1 = tk.Spinbox(frame_params, from_=100, to=96000, increment=500, width=13, font=("Arial", 9))
spin_fc1.delete(0, "end")
spin_fc1.insert(0, "6000.0")
spin_fc1.grid(row=5, column=0, sticky="w", pady=(0, 2), padx=(0, 10))

# --- Coluna Interna 1 ---
tk.Label(frame_params, text="PORTA:", font=("Arial", 8, "bold")).grid(row=0, column=1, sticky="w")
frame_porta = tk.Frame(frame_params)
frame_porta.grid(row=1, column=1, sticky="w", pady=(0, 5))

portas_encontradas = listar_portas_uart()
combo_porta = ttk.Combobox(frame_porta, values=portas_encontradas, width=13, font=("Arial", 9), state="readonly")
combo_porta.pack(side="left")

if "/dev/ttyUSB0" in portas_encontradas:
    combo_porta.set("/dev/ttyUSB0")
elif portas_encontradas:
    combo_porta.set(portas_encontradas[0])

btn_refresh_porta = tk.Button(frame_porta, text="🔄", command=atualizar_lista_portas, font=("Arial", 7), width=2)
btn_refresh_porta.pack(side="left", padx=(3, 0))

BAUD_RATES = (9600, 19200, 38400, 57600, 115200, 230400, 921600)
tk.Label(frame_params, text="BAUD Rate:", font=("Arial", 8, "bold")).grid(row=2, column=1, sticky="w")
spin_baud = tk.Spinbox(frame_params, values=BAUD_RATES, width=13, font=("Arial", 9), wrap=True)
spin_baud.delete(0, "end")
spin_baud.insert(0, "57600")
spin_baud.grid(row=3, column=1, sticky="w", pady=(0, 5))

tk.Label(frame_params, text="FC2 (Hz):", font=("Arial", 8, "bold")).grid(row=4, column=1, sticky="w")
spin_fc2 = tk.Spinbox(frame_params, from_=100, to=96000, increment=500, width=13, font=("Arial", 9))
spin_fc2.delete(0, "end")
spin_fc2.insert(0, "8000.0")
spin_fc2.grid(row=5, column=1, sticky="w", pady=(0, 2))

# 5. Botão "Apply Filter"
btn_apply = tk.Button(
    janela,
    text="Aplicar Filtro",#🚀
    font=("Arial", 10, "bold"),
    bg="#28a745",
    fg="white",
    activebackground="#218838",
    activeforeground="white",
    pady=6,
    command=aplicar_e_enviar_filtro
)
btn_apply.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(15, 5))

# Seleciona Rejeita-Faixa por padrão
selecionar_filtro(low_pass_button, "00", "Low pass")

janela.mainloop()