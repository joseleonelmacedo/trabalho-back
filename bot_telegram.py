import telebot
import pandas as pd
from datetime import datetime

# Arquivos CSV
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

arquivoDesem = "desemprego.csv"
dadosDesem = pd.read_csv(arquivoDesem, delimiter=";", dtype={"Ano": int, "Taxa": str})
dadosDesem["Taxa"] = (
    dadosDesem["Taxa"]
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
    texto = mensagem.text.lower()  # Converte o texto para minúsculas para aceitar qualquer caso
    chat_id = mensagem.chat.id

    if chat_id in estado_conversa:
        if estado_conversa[chat_id] == "aguardando_ano_pib":
            try:
                ano = int(texto)
                resultado = dadosPib[dadosPib["Ano"] == ano]
                if not resultado.empty:
                    pib = resultado["valor"].values[0]
                    estado_conversa[chat_id] = {"ano1": ano, "pib1": pib, "proximo": "aguardando_comparacao_pib"}
                    bot.send_message(chat_id, f"The GDP of Brazil in {ano} was: R${pib:,.2f}. Do you want to compare with another year? (Type the year or 'no' to return to the menu)")
                else:
                    bot.send_message(chat_id, f"Sorry, I couldn't find data for the year {ano}.")
                    estado_conversa.pop(chat_id, None)
            except ValueError:
                bot.send_message(chat_id, "Please enter a valid year.")
            return

        elif estado_conversa[chat_id] == "aguardando_ano_inflacao":
            try:
                ano = int(texto)
                resultado = dadosInfla[dadosInfla["Ano"] == ano]
                if not resultado.empty:
                    inflacao = resultado["Brasil"].values[0]
                    estado_conversa[chat_id] = {"ano1": ano, "inflacao1": inflacao, "proximo": "aguardando_comparacao_inflacao"}
                    bot.send_message(chat_id, f"The inflation in Brazil in {ano} was: {inflacao:.2f}%. Do you want to compare with another year? (Type the year or 'no' to return to the menu)")
                else:
                    bot.send_message(chat_id, f"Sorry, I couldn't find data for the year {ano}.")
                    estado_conversa.pop(chat_id, None)
            except ValueError:
                bot.send_message(chat_id, "Please enter a valid year.")
            return

        elif estado_conversa[chat_id] == "aguardando_ano_desemprego":
            try:
                ano = int(texto)
                resultado = dadosDesem[dadosDesem["Ano"] == ano]
                if not resultado.empty:
                    taxa_desemprego = resultado["Taxa"].values[0]
                    estado_conversa[chat_id] = {"ano1": ano, "desemprego1": taxa_desemprego, "proximo": "aguardando_comparacao_desemprego"}
                    bot.send_message(chat_id, f"The unemployment rate in Brazil in {ano} was: {taxa_desemprego:.2f}%. Do you want to compare with another year? (Type the year or 'no' to return to the menu)")
                else:
                    bot.send_message(chat_id, f"Sorry, I couldn't find data for the year {ano}.")
                    estado_conversa.pop(chat_id, None)
            except ValueError:
                bot.send_message(chat_id, "Please enter a valid year.")
            return

        # Comparação para PIB
        elif "proximo" in estado_conversa[chat_id] and estado_conversa[chat_id]["proximo"] == "aguardando_comparacao_pib":
            if texto == "não" or texto == "no":
                exibir_menu(chat_id)
                estado_conversa.pop(chat_id, None)  # Limpa o estado
            else:
                try:
                    ano2 = int(texto)
                    resultado = dadosPib[dadosPib["Ano"] == ano2]
                    if not resultado.empty:
                        pib2 = resultado["valor"].values[0]
                        ano1 = estado_conversa[chat_id]["ano1"]
                        pib1 = estado_conversa[chat_id]["pib1"]

                        variacao = ((pib2 - pib1) / pib1) * 100
                        status = "increased" if variacao > 0 else "decreased"
                        bot.send_message(
                            chat_id,
                            f"The GDP of Brazil in {ano2} was: R${pib2:,.2f}. Compared to {ano1}, the GDP {status} by {abs(variacao):.2f}%."
                        )
                    else:
                        bot.send_message(chat_id, f"Sorry, I couldn't find data for the year {ano2}.")

                    exibir_menu(chat_id)
                    estado_conversa.pop(chat_id, None)  # Limpa o estado
                except ValueError:
                    bot.send_message(chat_id, "Please enter a valid year.")
            return

        # Comparação para Inflação
        elif "proximo" in estado_conversa[chat_id] and estado_conversa[chat_id]["proximo"] == "aguardando_comparacao_inflacao":
            if texto == "não" or texto == "no":
                exibir_menu(chat_id)
                estado_conversa.pop(chat_id, None)
            else:
                try:
                    ano2 = int(texto)
                    resultado = dadosInfla[dadosInfla["Ano"] == ano2]
                    if not resultado.empty:
                        inflacao2 = resultado["Brasil"].values[0]
                        ano1 = estado_conversa[chat_id]["ano1"]
                        inflacao1 = estado_conversa[chat_id]["inflacao1"]

                        variacao = ((inflacao2 - inflacao1) / inflacao1) * 100
                        status = "increased" if variacao > 0 else "decreased"
                        bot.send_message(
                            chat_id,
                            f"The inflation in Brazil in {ano2} was: {inflacao2:.2f}%. Compared to {ano1}, the inflation {status} by {abs(variacao):.2f}%."
                        )
                    else:
                        bot.send_message(chat_id, f"Sorry, I couldn't find data for the year {ano2}.")

                    exibir_menu(chat_id)
                    estado_conversa.pop(chat_id, None)
                except ValueError:
                    bot.send_message(chat_id, "Please enter a valid year.")
            return

        # Comparação para Desemprego
        elif "proximo" in estado_conversa[chat_id] and estado_conversa[chat_id]["proximo"] == "aguardando_comparacao_desemprego":
            if texto == "não" or texto == "no":
                exibir_menu(chat_id)
                estado_conversa.pop(chat_id, None)  # Limpa o estado
            else:
                try:
                    ano2 = int(texto)
                    resultado = dadosDesem[dadosDesem["Ano"] == ano2]
                    if not resultado.empty:
                        desemprego2 = resultado["Taxa"].values[0]
                        ano1 = estado_conversa[chat_id]["ano1"]
                        desemprego1 = estado_conversa[chat_id]["desemprego1"]

                        variacao = ((desemprego2 - desemprego1) / desemprego1) * 100
                        status = "increased" if variacao > 0 else "decreased"
                        bot.send_message(
                            chat_id,
                            f"The unemployment rate in Brazil in {ano2} was: {desemprego2:.2f}%. Compared to {ano1}, the unemployment rate {status} by {abs(variacao):.2f}%."
                        )
                    else:
                        bot.send_message(chat_id, f"Sorry, I couldn't find data for the year {ano2}.")

                    exibir_menu(chat_id)
                    estado_conversa.pop(chat_id, None)
                except ValueError:
                    bot.send_message(chat_id, "Please enter a valid year.")
            return

    if texto == "hi" or texto == "hello":
        bot.send_message(chat_id, "Hello, I am ZenBot! How can I assist you?")
        exibir_menu(chat_id)
    elif texto == "/opcao1":
        estado_conversa[chat_id] = "aguardando_ano_pib"
        bot.send_message(chat_id, "Enter the year you want to check the GDP of Brazil:")
    elif texto == "/opcao2":
        estado_conversa[chat_id] = "aguardando_ano_inflacao"
        bot.send_message(chat_id, "Enter the year you want to check the inflation rate of Brazil:")
    elif texto == "/opcao3":
        estado_conversa[chat_id] = "aguardando_ano_desemprego"
        bot.send_message(chat_id, "Enter the year you want to check the unemployment rate of Brazil:")
    elif texto == "/opcao4":
        bot.send_message(chat_id, "see you in one day supertropical")
    else:
        bot.send_message(chat_id, "Sorry, I didn't understand. Please choose a valid option.")

def exibir_menu(chat_id):
    menu = "Choose an option to get started:\n"
    menu += "/opcao1 : Check the GDP of Brazil\n"
    menu += "/opcao2 : Check the inflation rate of Brazil\n"
    menu += "/opcao3 : Check the unemployment rate of Brazil\n"
    menu += "/opcao4 : Say blue"
    bot.send_message(chat_id, menu)

bot.polling(none_stop=True)