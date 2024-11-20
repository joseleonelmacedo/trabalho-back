import telebot
import pandas as pd
from datetime import datetime

arquivoPib = "pib.csv"
dadosPib = pd.read_csv(arquivoPib, delimiter=";", dtype={"Ano": int, "valor": str})
dadosPib["valor"] = dadosPib["valor"].str.replace('"', '').str.replace(',', '.').astype(float)

arquivoInfla = "inflacao.csv"
dadosInfla = pd.read_csv(arquivoInfla, delimiter=";", dtype={"Ano": int, "Brasil": str})
dadosInfla["Brasil"] = (
    dadosInfla["Brasil"]
    .str.replace('.', '', regex=False) 
    .str.replace(',', '.', regex=False) 
    .str.replace('%', '', regex=False) 
    .str.strip()
    .astype(float)
)

token = "7852388462:AAGjxA7nls0cqzxKW81KV-7pMQbB0Rk_ATg"
bot = telebot.TeleBot(token)

estado_conversa = {}

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = mensagem.text.lower()
    chat_id = mensagem.chat.id

    if chat_id in estado_conversa:
        if estado_conversa[chat_id] == "aguardando_ano_pib":
            try:
                ano = int(texto)
                resultado = dadosPib[dadosPib["Ano"] == ano]
                if not resultado.empty:
                    pib = resultado["valor"].values[0]
                    bot.send_message(chat_id, f"O PIB do Brasil em {ano} foi: R${pib:,.2f}")
                else:
                    bot.send_message(chat_id, f"Desculpe, não encontrei dados para o ano {ano}.")
            except ValueError:
                bot.send_message(chat_id, "Por favor, digite um ano válido.")
            estado_conversa.pop(chat_id, None) 
            return

        elif estado_conversa[chat_id] == "aguardando_ano_inflacao":
            try:
                ano = int(texto)
                resultado = dadosInfla[dadosInfla["Ano"] == ano]
                if not resultado.empty:
                    inflacao = resultado["Brasil"].values[0]
                    bot.send_message(chat_id, f"A inflação no Brasil em {ano} foi: {inflacao:.2f}%")
                else:
                    bot.send_message(chat_id, f"Desculpe, não encontrei dados para o ano {ano}.")
            except ValueError:
                bot.send_message(chat_id, "Por favor, digite um ano válido.")
            estado_conversa.pop(chat_id, None)  
            return

    if texto == "ola":
        bot.send_message(chat_id, "Opa, aqui é o ZenBot!")
        bot.send_message(
            chat_id, 
            """
Escolha uma opção para começar (clique no ícone):
/opcao1 : Falar azul
/opcao2 : Consultar o PIB do Brasil
/opcao3 : Consultar a inflação do Brasil
            """
        )

    elif texto == "/opcao1":
        bot.send_message(chat_id, "Azul")
    
    elif texto == "/opcao2":
        bot.send_message(chat_id, "Digite o ano que você quer consultar o PIB do Brasil:")
        estado_conversa[chat_id] = "aguardando_ano_pib"

    elif texto == "/opcao3":
        bot.send_message(chat_id, "Digite o ano que você quer consultar a inflação do Brasil:")
        estado_conversa[chat_id] = "aguardando_ano_inflacao"

    else:
        bot.send_message(chat_id, "Desculpe, não entendi. Tente novamente.")

try:
    bot.polling()
except Exception as e:
    print(f"Ocorreu um erro: {e}")
