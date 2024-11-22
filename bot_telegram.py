import telebot
import pandas as pd
from datetime import datetime

# Carregar o arquivo CSV com os dados do PIB
arquivoPib = "pib.csv"
dadosPib = pd.read_csv(arquivoPib, delimiter=";", dtype={"Ano": int, "valor": str})
dadosPib["valor"] = dadosPib["valor"].str.replace('"', '').str.replace(',', '.').astype(float)

# Carregar o arquivo CSV com os dados de inflação
arquivoInfla = "inflacao.csv"
dadosInfla = pd.read_csv(arquivoInfla, delimiter=";", dtype={"Ano": int, "Brasil": str})

# Limpar os dados na coluna "Brasil"
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

# Dicionário para armazenar o estado de cada chat
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
                    estado_conversa[chat_id] = {"ano1": ano, "pib1": pib, "proximo": "aguardando_comparacao"}
                    bot.send_message(chat_id, f"O PIB do Brasil em {ano} foi: R${pib:,.2f}. Deseja comparar com outro ano? (Digite o ano ou 'não' para voltar ao menu)")
                else:
                    bot.send_message(chat_id, f"Desculpe, não encontrei dados para o ano {ano}.")
                    estado_conversa.pop(chat_id, None)  # Remove o estado
            except ValueError:
                bot.send_message(chat_id, "Por favor, digite um ano válido.")
            return
        
        elif "proximo" in estado_conversa[chat_id] and estado_conversa[chat_id]["proximo"] == "aguardando_comparacao":
            if texto == "não":
                bot.send_message(
                    chat_id,
                    """
Escolha uma opção para começar (clique no ícone):
/opcao1 : Falar azul
/opcao2 : Consultar o PIB do Brasil
/opcao3 : Consultar a inflação do Brasil
                    """
                )
                estado_conversa.pop(chat_id, None)  # Remove o estado
            else:
                try:
                    ano2 = int(texto)
                    resultado = dadosPib[dadosPib["Ano"] == ano2]
                    if not resultado.empty:
                        pib2 = resultado["valor"].values[0]
                        ano1 = estado_conversa[chat_id]["ano1"]
                        pib1 = estado_conversa[chat_id]["pib1"]

                        # Cálculo da variação percentual
                        variacao = ((pib2 - pib1) / pib1) * 100
                        status = "cresceu" if variacao > 0 else "diminuiu"
                        bot.send_message(
                            chat_id, 
                            f"O PIB do Brasil em {ano2} foi: R${pib2:,.2f}. Comparado a {ano1}, o PIB {status} em {abs(variacao):.2f}%."
                        )
                    else:
                        bot.send_message(chat_id, f"Desculpe, não encontrei dados para o ano {ano2}.")
                    
                    # Exibir o menu novamente
                    bot.send_message(
                        chat_id,
                        """
Escolha uma opção para começar (clique no ícone):
/opcao1 : Falar azul
/opcao2 : Consultar o PIB do Brasil
/opcao3 : Consultar a inflação do Brasil
                        """
                    )
                    estado_conversa.pop(chat_id, None)  # Remove o estado
                except ValueError:
                    bot.send_message(chat_id, "Por favor, digite um ano válido.")
            return

    # Respostas padrões
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

# Executando o bot
try:
    bot.polling()
except Exception as e:
    print(f"Ocorreu um erro: {e}")
