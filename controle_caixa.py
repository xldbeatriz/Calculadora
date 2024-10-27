import tkinter as tk
from tkinter import messagebox
import sqlite3

# Função para salvar os dados no banco de dados
def salvar_dados():
    try:
        cartao = sum([float(x.replace(',', '.')) for x in cartao_entry.get().split('+')]) if cartao_entry.get() else 0
        pix = float(pix_entry.get().replace(',', '.')) if pix_entry.get() else 0
        dinheiro = float(dinheiro_entry.get().replace(',', '.')) if dinheiro_entry.get() else 0
        sangria = float(sangria_entry.get().replace(',', '.')) if sangria_entry.get() else 0
        data = data_entry.get()

        conn = sqlite3.connect('controle_caixa.db')
        c = conn.cursor()
        c.execute('INSERT INTO caixa (data, cartao, pix, dinheiro, sangria) VALUES (?, ?, ?, ?, ?)', 
                  (data, cartao, pix, dinheiro, sangria))
        conn.commit()
        conn.close()

        # Limpar os campos após salvar
        cartao_entry.delete(0, tk.END)
        pix_entry.delete(0, tk.END)
        dinheiro_entry.delete(0, tk.END)
        sangria_entry.delete(0, tk.END)
        data_entry.delete(0, tk.END)

        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

# Função para gerar o relatório do dia
def gerar_relatorio_dia():
    relatorio_dia_window = tk.Toplevel()
    relatorio_dia_window.title("Relatório do Dia")

    tk.Label(relatorio_dia_window, text="Data (dd/mm/yyyy):").grid(row=0, column=0)
    data_relatorio_entry = tk.Entry(relatorio_dia_window)
    data_relatorio_entry.grid(row=0, column=1)

    def mostrar_relatorio():
        data = data_relatorio_entry.get()
        conn = sqlite3.connect('controle_caixa.db')
        c = conn.cursor()
        c.execute('SELECT SUM(cartao), SUM(pix), SUM(dinheiro), SUM(sangria) FROM caixa WHERE data = ?', (data,))
        resultado = c.fetchone()
        conn.close()

        total_cartao = resultado[0] if resultado[0] is not None else 0
        total_pix = resultado[1] if resultado[1] is not None else 0
        total_dinheiro = resultado[2] if resultado[2] is not None else 0
        total_sangria = resultado[3] if resultado[3] is not None else 0

        total_entradas = total_cartao + total_pix + total_dinheiro
        total_saidas = total_sangria
        saldo = total_entradas - total_saidas

        relatorio_texto = (
            f"Relatório do dia {data}:\n"
            f"Total Cartão: R${total_cartao:.2f}\n"
            f"Total Pix: R${total_pix:.2f}\n"
            f"Total Dinheiro: R${total_dinheiro:.2f}\n"
            f"Total Sangria: R${total_sangria:.2f}\n"
            f"Saldo: R${saldo:.2f}\n"
        )

        messagebox.showinfo("Relatório do Dia", relatorio_texto)

    gerar_button = tk.Button(relatorio_dia_window, text="Gerar Relatório", command=mostrar_relatorio)
    gerar_button.grid(row=1, column=0, columnspan=2)

# Função para gerar o relatório do mês
def gerar_relatorio_mes():
    relatorio_mes_window = tk.Toplevel()
    relatorio_mes_window.title("Relatório do Mês")

    tk.Label(relatorio_mes_window, text="Mês (mm/yyyy):").grid(row=0, column=0)
    mes_relatorio_entry = tk.Entry(relatorio_mes_window)
    mes_relatorio_entry.grid(row=0, column=1)

    def mostrar_relatorio():
        mes = mes_relatorio_entry.get()
        conn = sqlite3.connect('controle_caixa.db')
        c = conn.cursor()
        # Ajustando a consulta para pegar o mês e o ano corretamente
        c.execute('SELECT SUM(cartao), SUM(pix), SUM(dinheiro), SUM(sangria) FROM caixa WHERE data LIKE ?', (f'%/{mes}',))
        resultado = c.fetchone()
        conn.close()

        total_cartao = resultado[0] if resultado[0] is not None else 0
        total_pix = resultado[1] if resultado[1] is not None else 0
        total_dinheiro = resultado[2] if resultado[2] is not None else 0
        total_sangria = resultado[3] if resultado[3] is not None else 0

        total_entradas = total_cartao + total_pix + total_dinheiro
        total_saidas = total_sangria
        saldo = total_entradas - total_saidas

        relatorio_texto = (
            f"Relatório do mês {mes}:\n"
            f"Total Cartão: R${total_cartao:.2f}\n"
            f"Total Pix: R${total_pix:.2f}\n"
            f"Total Dinheiro: R${total_dinheiro:.2f}\n"
            f"Total Sangria: R${total_sangria:.2f}\n"
            f"Saldo: R${saldo:.2f}\n"
        )

        messagebox.showinfo("Relatório do Mês", relatorio_texto)

    gerar_button = tk.Button(relatorio_mes_window, text="Gerar Relatório", command=mostrar_relatorio)
    gerar_button.grid(row=1, column=0, columnspan=2)

# Função para criar a interface gráfica
def criar_interface():
    global cartao_entry, pix_entry, dinheiro_entry, sangria_entry, data_entry

    # Janela principal
    root = tk.Tk()
    root.title("TORRE FORTE - Controle de Caixa")

    # Título
    titulo_label = tk.Label(root, text="TORRE FORTE", font=("Helvetica", 16, "bold"))
    titulo_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Campos de entrada
    tk.Label(root, text="Data (dd/mm/yyyy):").grid(row=1, column=0)
    data_entry = tk.Entry(root)
    data_entry.grid(row=1, column=1)

    tk.Label(root, text="Valor dos Cartões:").grid(row=2, column=0)
    cartao_entry = tk.Entry(root)
    cartao_entry.grid(row=2, column=1)

    tk.Label(root, text="Valor do Pix:").grid(row=3, column=0)
    pix_entry = tk.Entry(root)
    pix_entry.grid(row=3, column=1)

    tk.Label(root, text="Valor em Dinheiro:").grid(row=4, column=0)
    dinheiro_entry = tk.Entry(root)
    dinheiro_entry.grid(row=4, column=1)

    tk.Label(root, text="Valor da Sangria:").grid(row=5, column=0)
    sangria_entry = tk.Entry(root)
    sangria_entry.grid(row=5, column=1)

    # Botões
    salvar_button = tk.Button(root, text="Salvar Dados", command=salvar_dados)
    salvar_button.grid(row=6, column=0, columnspan=2, pady=10)

    relatorio_dia_button = tk.Button(root, text="Relatório do Dia", command=gerar_relatorio_dia)
    relatorio_dia_button.grid(row=7, column=0, columnspan=2)

    relatorio_mes_button = tk.Button(root, text="Relatório do Mês", command=gerar_relatorio_mes)
    relatorio_mes_button.grid(row=8, column=0, columnspan=2)

    root.mainloop()

# Criar a tabela no banco de dados, se não existir
def criar_tabela():
    conn = sqlite3.connect('controle_caixa.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS caixa (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 data TEXT,
                 cartao REAL,
                 pix REAL,
                 dinheiro REAL,
                 sangria REAL)''')
    conn.commit()
    conn.close()

# Executar as funções principais
criar_tabela()
criar_interface()
