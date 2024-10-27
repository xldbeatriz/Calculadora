#calculadora

import tkinter as tk
from tkinter import messagebox

#função para processar o calculo
def calcular():
   try:
       expressao=entrada.get()
       resultado=eval(expressao)
       entrada.delete(0,tk.END)
       entrada.insert(tk.END,str(resultado))
   except Exception as e:
        messagebox.showerror('Erro',f'Erro na expressão: {e}')

def apagar():
    entrada.delete(0,tk.END)

#Função para inserir números e operadores
def clique_botao(valor):
   if valor == '=':
       calcular()
   else:
    entrada.insert(tk.END, valor)


#criar a janela
janela = tk.Tk()
janela.title("CALCULADORA")

#Entrada de texto para a expressão
entrada = tk.Entry(janela,width=16, font=('Arial',24))
entrada.grid(row=0, column=0, columnspan=4)

#botões da calculadora
botoes = [
    'C','7','8','9','/',
    '4','5','6','*',
    '1','2','3','-',
    '0','.','=','+',
    ]


#Criar e posicionar os botões
for i,botao in enumerate(botoes):
    if botao == 'C':
        tk.Button(janela, text=botao, width=5, height=2, font=('Arial',18),
              command=apagar).grid(row=(i//4)+1, column=i%4)
    else:
         tk.Button(janela, text=botao, width=5, height=2,font=('Arial',18),
            command=lambda valor=botao: clique_botao(valor)).grid(row=(i//4)+1,column=i % 4)

#loop da interface
janela.mainloop()