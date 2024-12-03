import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- Configuração do Arquivo ---
ARQUIVO_CLIENTES = "clientes.json"

# --- Funções de Manipulação de Dados ---
def carregar_clientes():
    """Carrega a lista de clientes do arquivo JSON."""
    if os.path.exists(ARQUIVO_CLIENTES):
        with open(ARQUIVO_CLIENTES, "r") as arquivo:
            return json.load(arquivo)
    return []

def salvar_clientes():
    """Salva a lista de clientes no arquivo JSON."""
    with open(ARQUIVO_CLIENTES, "w") as arquivo:
        json.dump(clientes, arquivo, indent=4)

# --- Funções Auxiliares ---
def limpar_campos():
    """Limpa os campos de entrada de texto."""
    entrada_nome.delete(0, tk.END)
    entrada_cpf.delete(0, tk.END)
    entrada_senha.delete(0, tk.END)
    btn_adicionar.config(state=tk.NORMAL)
    btn_salvar.config(state=tk.DISABLED)

def atualizar_tabela(filtro=None, tipo_pesquisa="nome"):
    """Atualiza a tabela com os dados dos clientes."""
    tabela.delete(*tabela.get_children())  # Limpa a tabela
    for cliente in clientes:
        if filtro:
            if tipo_pesquisa == "nome" and filtro in cliente["nome"].lower():
                tabela.insert("", "end", values=(cliente["nome"], cliente["cpf"], cliente["senha_gov"]))
            elif tipo_pesquisa == "cpf" and filtro in cliente["cpf"]:
                tabela.insert("", "end", values=(cliente["nome"], cliente["cpf"], cliente["senha_gov"]))
        else:
            tabela.insert("", "end", values=(cliente["nome"], cliente["cpf"], cliente["senha_gov"]))

def alternar_visibilidade():
    """Alterna a visibilidade do campo de senha."""
    entrada_senha.config(show="" if mostrar_senha.get() else "*")

# --- Funções Principais ---
def pesquisar_cliente():
    """Realiza a pesquisa de clientes pelo filtro informado."""
    termo = entrada_pesquisa.get().lower()
    tipo_pesquisa = tipo_busca.get()
    atualizar_tabela(filtro=termo, tipo_pesquisa=tipo_pesquisa)

def adicionar_cliente():
    """Adiciona um novo cliente à lista."""
    nome = entrada_nome.get()
    cpf = entrada_cpf.get()
    senha_gov = entrada_senha.get()

    if not nome or not cpf or not senha_gov:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return

    if any(cliente["cpf"] == cpf for cliente in clientes):
        messagebox.showerror("Erro", "CPF já cadastrado!")
        return

    clientes.append({"nome": nome, "cpf": cpf, "senha_gov": senha_gov})
    salvar_clientes()
    atualizar_tabela()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")

def excluir_cliente():
    """Exclui o cliente selecionado da tabela e da lista."""
    try:
        item_selecionado = tabela.selection()[0]
        valores = tabela.item(item_selecionado, "values")
        tabela.delete(item_selecionado)

        clientes[:] = [c for c in clientes if c["cpf"] != valores[1]]
        salvar_clientes()
        messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
    except IndexError:
        messagebox.showerror("Erro", "Selecione um cliente para excluir.")

def selecionar_cliente():
    """Preenche os campos com os dados do cliente selecionado para edição."""
    try:
        item_selecionado = tabela.selection()[0]
        valores = tabela.item(item_selecionado, "values")

        entrada_nome.delete(0, tk.END)
        entrada_nome.insert(0, valores[0])

        entrada_cpf.delete(0, tk.END)
        entrada_cpf.insert(0, valores[1])

        entrada_senha.delete(0, tk.END)
        entrada_senha.insert(0, valores[2])

        # Desativa o botão de adicionar e ativa o de salvar
        btn_adicionar.config(state=tk.DISABLED)
        btn_salvar.config(state=tk.NORMAL)
    except IndexError:
        messagebox.showerror("Erro", "Selecione um cliente para editar.")

def salvar_alteracoes():
    """Salva as alterações feitas no cliente selecionado."""
    nome = entrada_nome.get()
    cpf = entrada_cpf.get()
    senha_gov = entrada_senha.get()

    if not nome or not cpf or not senha_gov:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return

    item_selecionado = tabela.selection()[0]
    valores = tabela.item(item_selecionado, "values")

    for cliente in clientes:
        if cliente["cpf"] == valores[1]:  # CPF é usado como identificador único
            cliente["nome"] = nome
            cliente["cpf"] = cpf
            cliente["senha_gov"] = senha_gov
            break

    salvar_clientes()
    atualizar_tabela()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")

# --- Inicialização de Dados ---
clientes = carregar_clientes()

# --- Interface Gráfica ---
janela = tk.Tk()
janela.title("Consulta e Cadastro de Clientes")
janela.geometry("800x600")

# --- Seção de Pesquisa ---
frame_pesquisa = tk.Frame(janela, padx=10, pady=10)
frame_pesquisa.pack(fill="x")

tipo_busca = tk.StringVar(value="nome")
tk.Radiobutton(frame_pesquisa, text="Nome", variable=tipo_busca, value="nome").pack(side=tk.LEFT, padx=5)
tk.Radiobutton(frame_pesquisa, text="CPF", variable=tipo_busca, value="cpf").pack(side=tk.LEFT, padx=5)

entrada_pesquisa = tk.Entry(frame_pesquisa, width=30)
entrada_pesquisa.pack(side=tk.LEFT, padx=5)

tk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar_cliente).pack(side=tk.LEFT, padx=5)

# --- Tabela de Clientes ---
frame_tabela = tk.Frame(janela)
frame_tabela.pack(fill="both", expand=True, pady=10)

tabela = ttk.Treeview(frame_tabela, columns=("nome", "cpf", "senha_gov"), show="headings")
tabela.pack(side=tk.LEFT, fill="both", expand=True)

tabela.heading("nome", text="Nome")
tabela.heading("cpf", text="CPF")
tabela.heading("senha_gov", text="Senha GOV")

tabela.column("nome", width=200)
tabela.column("cpf", width=150)
tabela.column("senha_gov", width=200)

scroll_tabela = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
scroll_tabela.pack(side=tk.RIGHT, fill="y")
tabela.configure(yscroll=scroll_tabela.set)

atualizar_tabela()

# --- Seção de Adicionar/Editar Cliente ---
frame_adicionar = tk.LabelFrame(janela, text="Adicionar/Editar Cliente", padx=10, pady=10)
frame_adicionar.pack(fill="x", padx=10, pady=10)

tk.Label(frame_adicionar, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entrada_nome = tk.Entry(frame_adicionar, width=30)
entrada_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_adicionar, text="CPF:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entrada_cpf = tk.Entry(frame_adicionar, width=30)
entrada_cpf.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_adicionar, text="Senha GOV:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entrada_senha = tk.Entry(frame_adicionar, width=30, show="*")
entrada_senha.grid(row=2, column=1, padx=5, pady=5)

mostrar_senha = tk.BooleanVar()
tk.Checkbutton(frame_adicionar, text="Mostrar senha", variable=mostrar_senha, command=alternar_visibilidade).grid(row=2, column=2, padx=5, pady=5)

btn_adicionar = tk.Button(frame_adicionar, text="Adicionar Cliente", command=adicionar_cliente)
btn_adicionar.grid(row=3, column=0, pady=10)

btn_excluir = tk.Button(frame_adicionar, text="Excluir Cliente", command=excluir_cliente)
btn_excluir.grid(row=3, column=1, pady=10)

btn_salvar = tk.Button(frame_adicionar, text="Salvar Alterações", command=salvar_alteracoes, state=tk.DISABLED)
btn_salvar.grid(row=3, column=2, pady=10)

btn_editar = tk.Button(frame_adicionar, text="Editar Cliente", command=selecionar_cliente)
btn_editar.grid(row=3, column=3, pady=10)

# --- Inicializa o Loop ---
janela.mainloop()
