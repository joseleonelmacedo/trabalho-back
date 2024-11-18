import telebot
from datetime import datetime

# Token do bot
token = "7852388462:AAGjxA7nls0cqzxKW81KV-7pMQbB0Rk_ATg"

# Inicializando o bot
bot = telebot.TeleBot(token)

# Função para verificar mensagens
def verificar(mensagem):
    return True

# Manipulador de mensagens
@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = mensagem.text.lower()

    if texto == "ola":
        bot.send_message(mensagem.chat.id, "Opa, aqui é o ZenBot!")
        bot.send_message(
            mensagem.chat.id, 
            """
Escolha uma opção para começar (clique no ícone):
/opcao1 : dar bom dia
/opcao2 : falar a hora
/opcao3 : falar uma cor
            """
        )

    if texto =="/opcao1":
        bot.send_message(mensagem.chat.id, "Bom dia!")
    
    elif texto =="/opcao2":
        hora_atual = datetime.now().strftime("%H:%M:%S")
        bot.send_message(mensagem.chat.id,f"A hora exata agora é: {hora_atual}")

    elif texto == "/opcao3":
        bot.send_message(mensagem.chat.id, "vermelho!")




try:
    bot.polling()
except Exception as e:
    print(f"Ocorreu um erro: {e}")
