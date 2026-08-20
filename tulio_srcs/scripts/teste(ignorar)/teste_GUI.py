import os
import tkinter as tk
from PIL import Image, ImageTk

# Funções
def low_pass():
    texto_principal.config(text="Select the filter:🌍")

def high_pass():
    texto_principal.config(text="Select the filter:🌍")

def range_pass():
    texto_principal.config(text="Select the filter:🌍")

def rejects_range():
    texto_principal.config(text="Select the filter:🌍")

# 1. Janela Principal
janela = tk.Tk()
janela.title("FIR_generator_GUI")
#janela.geometry("400x300")

# 2. Imagem (Linha 0, ocupa as colunas 0 e 1)
# Pega o caminho exato da pasta onde o GUI_fir.py está salvo
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
caminho_imagem = os.path.join(PASTA_ATUAL, "logo-linse.png")

# Abre a imagem usando o caminho completo
imagem_original = Image.open(caminho_imagem)

imagem_redimensionada = imagem_original.resize((300, 135))
imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
label_imagem = tk.Label(janela, image=imagem_tk)
label_imagem.image = imagem_tk
label_imagem.grid(row=0, column=0, columnspan=2, pady=5)

# 3. Texto (Linha 1, ocupa as colunas 0 e 1)
texto_principal = tk.Label(janela, text="Select the filter:", font=("Arial", 14), width=20)
texto_principal.grid(row=1, column=0, columnspan=2, sticky="w", pady=10)

# 4. Botões (Linha 2, lado a lado nas colunas 0 e 1)
low_pass_button = tk.Button(janela, text="Low pass", relief="raised", command=low_pass)
low_pass_button.grid(row=2, column=0, padx=1, pady=1)

high_pass_button = tk.Button(janela, text="High pass", relief="raised", command=high_pass)
high_pass_button.grid(row=3, column=0, padx=1, pady=10)

range_pass_button = tk.Button(janela, text="Range pass", relief="raised", command=range_pass)
range_pass_button.grid(row=4, column=0, padx=1, pady=10)

rejects_range_button = tk.Button(janela, text="Rejects range", command=rejects_range)
rejects_range_button.grid(row=5, column=0, padx=1, pady=10)

# 5. Spinbox na Direita (Coluna 2, centralizado entre as linhas 2 e 3)
frame_spinbox = tk.Frame(janela)
frame_spinbox.grid(row=2, column=2, rowspan=2, padx=15, pady=5, sticky="n")

label_spinbox = tk.Label(frame_spinbox, text="Ntaps:", font=("Arial", 10, "bold"))
label_spinbox.pack(anchor="w", pady=(0, 2))

seletor_ordem = tk.Spinbox(frame_spinbox, from_=1, to=201, width=8, font=("Arial", 11))
seletor_ordem.pack(anchor="w")


# 6. Loop Principal
janela.mainloop()