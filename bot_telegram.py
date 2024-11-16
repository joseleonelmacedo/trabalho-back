import telebot
from datetime import datetime

token = "7852388462:AAGjxA7nls0cqzxKW81KV-7pMQbB0Rk_ATg"

bot = telebot.TeleBot(token)

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = mensagem.text.lower()

    if texto == "ola":
        bot.reply_to(mensagem, "Opa, aqui é o ZenBot!")
    elif texto == "que horas são ?":
        hora_atual = datetime.now().strftime("%H:%M:%S")
        bot.reply_to(mensagem, f"A hora exata agora é: {hora_atual}")
    elif texto == "fale uma cor":
        bot.reply_to(mensagem, "Vermelho")

try:
    bot.polling()
except Exception as e:
    print(f"Ocorreu um erro: {e}")
