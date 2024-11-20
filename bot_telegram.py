import telebot
import pandas as pd
from datetime import datetime

# Carregar o arquivo CSV com os dados do PIB
arquivoPib = "pib.csv"
dadosPib = pd.read_csv(arquivoPib, delimiter=";", dtype={"Ano": int, "valor": str})
dadosPib["valor"] = dadosPib["valor"].str.replace('"', '').str.replace(',', '.').astype(float)

# Token do bot
token = "7852388462:AAGjxA7nls0cqzxKW81KV-7pMQbB0Rk_ATg"
bot = telebot.TeleBot(token)

# Dicionário para armazenar o estado de cada chat
estado_conversa = {}

# Função para verificar mensagens
def verificar(mensagem):
    return True

# Manipulador de mensagens
@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = mensagem.text.lower()
    chat_id = mensagem.chat.id

    # Verifica se o usuário está na etapa de fornecer o ano
    if chat_id in estado_conversa and estado_conversa[chat_id] == "aguardando_ano":
        try:
            ano = int(texto)
            # Filtra os dados do PIB para o ano informado
            resultado = dadosPib[dadosPib["Ano"] == ano]
            
            if not resultado.empty:
                pib = resultado["valor"].values[0]  # Obtém o PIB correspondente
                bot.send_message(chat_id, f"O PIB do Brasil em {ano} foi: R${pib:,.2f}")
            else:
                bot.send_message(chat_id, f"Desculpe, não encontrei dados para o ano {ano}.")
        except ValueError:
            bot.send_message(chat_id, "Por favor, digite um ano válido.")
        
        # Remove o estado de espera
        estado_conversa.pop(chat_id, None)
        return

    # Respostas padrões
    if texto == "ola":
        bot.send_message(chat_id, "Opa, aqui é o ZenBot!")
        bot.send_message(
            chat_id, 
            """
Escolha uma opção para começar (clique no ícone):
/opcao1 : Falar azul
/opcao2 : Falar o PIB do Brasil
/opcao3 : Falar uma cor
            """
        )

    elif texto == "/opcao1":
        bot.send_message(chat_id, "Azul")
    
    elif texto == "/opcao2":
        bot.send_message(chat_id, "Digite o ano que você quer consultar o PIB do Brasil:")
        estado_conversa[chat_id] = "aguardando_ano"  # Marca o estado como aguardando o ano

    elif texto == "/opcao3":
        bot.send_message(chat_id, "Vermelho!")

    else:
        bot.send_message(chat_id, "Desculpe, não entendi. Tente novamente.")

# Executando o bot
try:
    bot.polling()
except Exception as e:
    print(f"Ocorreu um erro: {e}")
