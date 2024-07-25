import tkinter as tk
from tkinter import messagebox
import sqlite3

def conectar_banco():
    return sqlite3.connect('contas.db')

# Dicionário para armazenar as contas mensais
contas_mensais = {}

# Função para adicionar uma nova conta
def adicionar_conta():
    mes = entry_mes.get()
    try:
        valor = float(entry_valor.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor válido.")
        return
    
    contas_mensais[mes] = valor
    atualizar_lista()
    messagebox.showinfo("Sucesso", f"Conta adicionada para {mes}: R${valor:.2f}")

# Função para editar uma conta existente
def editar_conta():
    mes = entry_mes.get()
    try:
        novo_valor = float(entry_valor.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor válido.")
        return
    
    if mes in contas_mensais:
        contas_mensais[mes] = novo_valor
        atualizar_lista()
        messagebox.showinfo("Sucesso", f"Conta para {mes} atualizada para: R${novo_valor:.2f}")
    else:
        messagebox.showerror("Erro", f"Conta para {mes} não encontrada.")

# Função para excluir uma conta
def excluir_conta():
    mes = entry_mes.get()
    if mes in contas_mensais:
        del contas_mensais[mes]
        atualizar_lista()
        messagebox.showinfo("Sucesso", f"Conta para {mes} excluída.")
    else:
        messagebox.showerror("Erro", f"Conta para {mes} não encontrada.")

# Função para atualizar a lista de contas exibida
def atualizar_lista():
    listbox_contas.delete(0, tk.END)
    for mes, valor in contas_mensais.items():
        listbox_contas.insert(tk.END, f"{mes}: R${valor:.2f}")

# Criação da janela principal
root = tk.Tk()
root.title("Armazenamento de Contas Mensais")

# Criação dos widgets
label_mes = tk.Label(root, text="Mês:")
label_mes.grid(row=0, column=0, padx=10, pady=10)
entry_mes = tk.Entry(root)
entry_mes.grid(row=0, column=1, padx=10, pady=10)

label_valor = tk.Label(root, text="Valor:")
label_valor.grid(row=1, column=0, padx=10, pady=10)
entry_valor = tk.Entry(root)
entry_valor.grid(row=1, column=1, padx=10, pady=10)

button_adicionar = tk.Button(root, text="Adicionar", command=adicionar_conta)
button_adicionar.grid(row=2, column=0, padx=10, pady=10)

button_editar = tk.Button(root, text="Editar", command=editar_conta)
button_editar.grid(row=2, column=1, padx=10, pady=10)

button_excluir = tk.Button(root, text="Excluir", command=excluir_conta)
button_excluir.grid(row=2, column=2, padx=10, pady=10)

listbox_contas = tk.Listbox(root, width=50)
listbox_contas.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Inicializar a lista de contas
atualizar_lista()

# Iniciar o loop principal
root.mainloop()
