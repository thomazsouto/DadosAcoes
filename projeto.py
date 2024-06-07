import yfinance as yf
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox

def enviar_email(para, ticker, cotacao_maxima, cotacao_minima, valor_medio, data_brasil_inicio, data_brasil_fim):
    # Configurações do servidor de e-mail do Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'testethomaz53@gmail.com'
    smtp_password = 'csxf gbcn fvhk rous'  

    # Detalhes do e-mail
    de = 'testethomaz53@gmail.com'
    assunto = 'Relatório da Ação Financeira'
    corpo = f"""
    Olá,

    Segue os dados solicitados sobre a ação: {ticker} 

    Cotação máxima: R$ {cotacao_maxima}
    Cotação mínima: R$ {cotacao_minima}
    Valor médio: R$ {valor_medio}

    Esses dados são referentes ao período {data_brasil_inicio:%d/%m/%Y} até {data_brasil_fim:%d/%m/%Y}

    Atenciosamente
    """

    # Criar a mensagem
    mensagem = MIMEMultipart()
    mensagem['From'] = de
    mensagem['To'] = para
    mensagem['Subject'] = assunto
    mensagem.attach(MIMEText(corpo, 'plain'))

    # Conectar ao servidor de e-mail e enviar o e-mail
    try:
        servidor = smtplib.SMTP(smtp_server, smtp_port)
        servidor.starttls()  # Iniciar TLS para segurança
        servidor.login(smtp_user, smtp_password)  # Logar no servidor de e-mail
        texto = mensagem.as_string()  # Converter a mensagem para string
        servidor.sendmail(de, para, texto)  # Enviar o e-mail
        messagebox.showinfo("Sucesso", "E-mail enviado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        servidor.quit()  # Sair do servidor de e-mail

def buscar_e_enviar():
    ticker = entry_ticker.get()
    data_input_inicio = entry_data_inicio.get()
    data_input_fim = entry_data_fim.get()
    email = entry_email.get()
    
    try:
        data_brasil_inicio = datetime.strptime(data_input_inicio, "%d/%m/%Y")
        data_brasil_fim = datetime.strptime(data_input_fim, "%d/%m/%Y")
        
        data_america_inicio = data_brasil_inicio.strftime("%Y-%m-%d")
        data_america_fim = data_brasil_fim.strftime("%Y-%m-%d")
        
        dados = yf.Ticker(ticker).history(start=data_america_inicio, end=data_america_fim)

        fechamento = dados['Close']
        cotacao_maxima = round(fechamento.max(), 2)
        cotacao_minima = round(fechamento.min(), 2)
        valor_medio = round(fechamento.mean(), 2)
        
        enviar_email(email, ticker, cotacao_maxima, cotacao_minima, valor_medio, data_brasil_inicio, data_brasil_fim)
        
    except ValueError:
        messagebox.showerror("Erro", "Formato de data inválido. Por favor, insira a data no formato DD/MM/AAAA.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao buscar as informações: {e}")

# Criação da interface gráfica
root = tk.Tk()
root.title("Relatório de Ação Financeira")

tk.Label(root, text="Código da Ação:").grid(row=0, column=0)
entry_ticker = tk.Entry(root)
entry_ticker.grid(row=0, column=1)

tk.Label(root, text="Data de Início (DD/MM/AAAA):").grid(row=1, column=0)
entry_data_inicio = tk.Entry(root)
entry_data_inicio.grid(row=1, column=1)

tk.Label(root, text="Data de Fim (DD/MM/AAAA):").grid(row=2, column=0)
entry_data_fim = tk.Entry(root)
entry_data_fim.grid(row=2, column=1)

tk.Label(root, text="E-mail:").grid(row=3, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=3, column=1)

tk.Button(root, text="Enviar Relatório", command=buscar_e_enviar).grid(row=4, columnspan=2)

root.mainloop()