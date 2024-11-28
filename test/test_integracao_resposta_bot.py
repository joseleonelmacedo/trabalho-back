from unittest.mock import MagicMock
import telebot
import pandas as pd
import pytest
from io import StringIO

# Fixture para simular os dados CSV
@pytest.fixture
def mock_csv_data():
    # Exemplo de dados para PIB em formato CSV
    pib_data = """Ano;valor
    2020;"2.000.000.000"
    2021;"2.500.000.000"
    """
    return {
        "pib": StringIO(pib_data)
    }

# Testando a lógica de resposta do bot
@pytest.fixture
def mock_bot():
    bot = MagicMock(spec=telebot.TeleBot)
    return bot

def test_responder_ano_pib(mock_bot, mock_csv_data):
    # Simule o recebimento de uma mensagem com o ano do PIB
    texto = "2020"
    chat_id = 12345

    # Simula a leitura do CSV do PIB
    df_pib = pd.read_csv(mock_csv_data["pib"], delimiter=";", dtype={"Ano": int, "valor": str})
    
    # Corrigindo o formato da coluna "valor" para garantir que seja interpretado corretamente como número
    df_pib["valor"] = df_pib["valor"].str.replace('"', '').str.replace('.', '').str.replace(',', '.').astype(float)
    
    # Defina o estado da conversa para "aguardando_ano_pib"
    estado_conversa = {chat_id: "aguardando_ano_pib"}

    # Simule a execução da função "responder"
    if estado_conversa[chat_id] == "aguardando_ano_pib":
        try:
            ano = int(texto)
            resultado = df_pib[df_pib["Ano"] == ano]
            if not resultado.empty:
                pib = resultado["valor"].values[0]
                estado_conversa[chat_id] = {"ano1": ano, "pib1": pib, "proximo": "aguardando_comparacao_pib"}
                mock_bot.send_message(chat_id, f"The GDP of Brazil in {ano} was: R${pib:,.2f}. Do you want to compare with another year? (Type the year or 'no' to return to the menu)")
            else:
                mock_bot.send_message(chat_id, f"Sorry, I couldn't find data for the year {ano}.")
        except ValueError:
            mock_bot.send_message(chat_id, "Please enter a valid year.")

    # Verifique se a resposta correta foi enviada
    mock_bot.send_message.assert_called_with(chat_id, "The GDP of Brazil in 2020 was: R$2,000,000,000.00. Do you want to compare with another year? (Type the year or 'no' to return to the menu)")
