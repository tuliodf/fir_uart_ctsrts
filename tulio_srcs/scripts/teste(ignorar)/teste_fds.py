import os
import tkinter as tk
from tkinter import ttk, messagebox
import serial.tools.list_ports  # Para detectar as portas seriais do sistema
from PIL import Image, ImageTk

# --- VARIÁVEIS DE CONFIGURAÇÃO ---
FILTER_SEL = "11"  # "00"=passa-baixas, "01"=passa-altas, "10"=passa-faixa, "11"=rejeita-faixa

# --- FUNÇÃO PARA DETECTAR PORTAS UART ---
def listar_portas_uart():
    portas_brutas = serial.tools.list_ports.comports()
    
    # Filtra apenas portas USB reais (ttyUSB/ttyACM no Linux, COM no Windows)
    portas_filtradas = [
        port.device for port in portas_brutas
        if any(term in port.device for term in ["ttyUSB", "ttyACM", "COM"])
    ]
    # Retorna as portas USB encontradas ou um aviso caso nenhuma esteja plugada
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

    # 1. Reseta todos os botões para o visual padrão (elevado)
    for btn in todos_botoes:
        btn.config(relief="raised", bd=2, bg="#f0f0f0", fg="black")

    # 2. Destaca o botão selecionado (afundado e colorido em azul)
    botao_clicado.config(relief="sunken", bd=3, bg="#007ACC", fg="white")

    # 3. Atualiza o texto de status
    texto_principal.config(text=f"Filter selected: {nome_filtro} ({codigo_filtro})")

    # 4. Habilita/Desabilita FC2 de acordo com o tipo de filtro
    if codigo_filtro in ["10", "11"]:
        spin_fc2.config(state="normal")
    else:
        spin_fc2.config(state="disabled")

# --- FUNÇÃO PARA APLICAR O FILTRO (BOTÃO APPLY FILTER) ---
def aplicar_filtro():
    try:
        taps = int(spin_taps.get())
        fs = float(spin_fs.get())
        fc1 = float(spin_fc1.get())
        fc2 = float(spin_fc2.get()) if FILTER_SEL in ["10", "11"] else None
        porta = combo_porta.get()
        baud = spin_baud.get()

        # Exibe os parâmetros lidos no terminal
        print("\n=== APLICANDO CONFIGURAÇÃO DO FILTRO ===")
        print(f"Tipo (FILTER_SEL) : {FILTER_SEL}")
        print(f"NUM_TAPS          : {taps}")
        print(f"FS (Hz)           : {fs}")
        print(f"FC1 (Hz)          : {fc1}")
        print(f"FC2 (Hz)          : {fc2 if fc2 is not None else 'N/A'}")
        print(f"Porta UART        : {porta}")
        print(f"Baud Rate         : {baud}")
        print("=========================================\n")

        # Atualiza a interface
        texto_principal.config(
            text=f"Filter applied! ({FILTER_SEL}) | Taps: {taps} | Fs: {int(fs)}Hz",
            fg="#006600"
        )

    except ValueError:
        messagebox.showerror("Erro de Entrada", "Verifique se os valores numéricos dos Spinboxes são válidos!")


# 1. Janela Principal
janela = tk.Tk()
janela.title("FIR_generator_GUI")
janela.config(padx=15, pady=10)

# 2. Imagem (Linha 0)
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

# 3. Texto de Status (Linha 1)
texto_principal = tk.Label(janela, text="Select the filter:", font=("Arial", 11, "bold"), width=40, anchor="w")
texto_principal.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 5))

# 4. Painel de Botões (Coluna 0)
frame_botoes = tk.Frame(janela)
frame_botoes.grid(row=2, column=0, sticky="nw", padx=(0, 10))

low_pass_button = tk.Button(
    frame_botoes, text="Low pass", width=13,
    command=lambda: selecionar_filtro(low_pass_button, "00", "Low pass")
)
low_pass_button.pack(pady=4)

high_pass_button = tk.Button(
    frame_botoes, text="High pass", width=13,
    command=lambda: selecionar_filtro(high_pass_button, "01", "High pass")
)
high_pass_button.pack(pady=4)

range_pass_button = tk.Button(
    frame_botoes, text="Range pass", width=13,
    command=lambda: selecionar_filtro(range_pass_button, "10", "Range pass")
)
range_pass_button.pack(pady=4)

rejects_range_button = tk.Button(
    frame_botoes, text="Rejects range", width=13,
    command=lambda: selecionar_filtro(rejects_range_button, "11", "Rejects range")
)
rejects_range_button.pack(pady=4)

todos_botoes = [low_pass_button, high_pass_button, range_pass_button, rejects_range_button]

# 5. Painel de Parâmetros e UART (Coluna 1)
frame_params = tk.LabelFrame(janela, text=" Parameters ", font=("Arial", 9, "bold"), padx=10, pady=5)
frame_params.grid(row=2, column=1, sticky="nsew")

# --- COLUNA INTERNA 0 ---
# Spinbox: NUM_TAPS
tk.Label(frame_params, text="NUM_TAPS:", font=("Arial", 8, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 10))
spin_taps = tk.Spinbox(frame_params, from_=1, to=501, increment=2, width=13, font=("Arial", 9))
spin_taps.delete(0, "end")
spin_taps.insert(0, "199")
spin_taps.grid(row=1, column=0, sticky="w", pady=(0, 5), padx=(0, 10))

# Spinbox: FS (Frequência de Amostragem)
tk.Label(frame_params, text="FS (Hz):", font=("Arial", 8, "bold")).grid(row=2, column=0, sticky="w", padx=(0, 10))
spin_fs = tk.Spinbox(frame_params, from_=1000, to=192000, increment=1000, width=13, font=("Arial", 9))
spin_fs.delete(0, "end")
spin_fs.insert(0, "48000.0")
spin_fs.grid(row=3, column=0, sticky="w", pady=(0, 5), padx=(0, 10))

# Spinbox: FC1 (Frequência de Corte 1)
tk.Label(frame_params, text="FC1 (Hz):", font=("Arial", 8, "bold")).grid(row=4, column=0, sticky="w", padx=(0, 10))
spin_fc1 = tk.Spinbox(frame_params, from_=100, to=96000, increment=500, width=13, font=("Arial", 9))
spin_fc1.delete(0, "end")
spin_fc1.insert(0, "6000.0")
spin_fc1.grid(row=5, column=0, sticky="w", pady=(0, 2), padx=(0, 10))


# --- COLUNA INTERNA 1 ---
# Seleção de PORTA UART
tk.Label(frame_params, text="PORTA:", font=("Arial", 8, "bold")).grid(row=0, column=1, sticky="w")
frame_porta = tk.Frame(frame_params)
frame_porta.grid(row=1, column=1, sticky="w", pady=(0, 5))

portas_encontradas = listar_portas_uart()
combo_porta = ttk.Combobox(frame_porta, values=portas_encontradas, width=13, font=("Arial", 9), state="readonly")
combo_porta.pack(side="left")

# Define /dev/ttyUSB0 se existir na lista, senão escolhe a primeira disponível
if "/dev/ttyUSB0" in portas_encontradas:
    combo_porta.set("/dev/ttyUSB0")
elif portas_encontradas:
    combo_porta.set(portas_encontradas[0])

btn_refresh_porta = tk.Button(frame_porta, text="🔄", command=atualizar_lista_portas, font=("Arial", 7), width=2)
btn_refresh_porta.pack(side="left", padx=(3, 0))

# Spinbox: BAUD Rate
BAUD_RATES = (9600, 19200, 38400, 57600, 115200, 230400, 921600)
tk.Label(frame_params, text="BAUD Rate:", font=("Arial", 8, "bold")).grid(row=2, column=1, sticky="w")
spin_baud = tk.Spinbox(frame_params, values=BAUD_RATES, width=13, font=("Arial", 9), wrap=True)
spin_baud.delete(0, "end")
spin_baud.insert(0, "57600")
spin_baud.grid(row=3, column=1, sticky="w", pady=(0, 5))

# Spinbox: FC2 (Frequência de Corte 2)
tk.Label(frame_params, text="FC2 (Hz):", font=("Arial", 8, "bold")).grid(row=4, column=1, sticky="w")
spin_fc2 = tk.Spinbox(frame_params, from_=100, to=96000, increment=500, width=13, font=("Arial", 9))
spin_fc2.delete(0, "end")
spin_fc2.insert(0, "8000.0")
spin_fc2.grid(row=5, column=1, sticky="w", pady=(0, 2))

# 6. Botão "Apply Filter" (Linha 3 - Ocupa toda a largura)
btn_apply = tk.Button(
    janela,
    text="🚀 Apply Filter",
    font=("Arial", 10, "bold"),
    bg="#28a745",
    fg="white",
    activebackground="#218838",
    activeforeground="white",
    pady=6,
    command=aplicar_filtro
)
btn_apply.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(15, 5))

# 🚀 Ativa por padrão o Rejeita-Faixa ("11")
selecionar_filtro(rejects_range_button, "11", "Rejects range")

# 7. Loop Principal
janela.mainloop()