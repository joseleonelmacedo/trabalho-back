import pytest
from unittest.mock import Mock, patch
from bot_telegram import responder, exibir_menu, estado_conversa, dadosPib, dadosInfla, dadosDesem

@pytest.fixture
def mock_bot():
    """Mock do bot para interceptar mensagens enviadas."""
    mock = Mock()
    return mock

def test_menu_display(mock_bot):
    """Teste para garantir que o menu é exibido corretamente."""
    chat_id = 12345
    exibir_menu(mock_bot)
    menu = (
        "Choose an option to get started:"
        "/opcao1 : Check the GDP of Brazil"
        "/opcao2 : Check the inflation rate of Brazil"
        "/opcao3 : Check the unemployment rate of Brazil"
        "/opcao4 : exit"
    )
    mock_bot.send_message.assert_called_with(chat_id, menu)

def test_gdp_lookup_success(mock_bot):
    """Teste para verificar se o PIB de um ano específico é retornado corretamente."""
    mensagem = Mock()
    mensagem.chat.id = 12345
    mensagem.text = "2020"
    
    estado_conversa[mensagem.chat.id] = "aguardando_ano_pib"
    responder(mensagem)

    resultado = dadosPib[dadosPib["Ano"] == 2020]
    assert not resultado.empty, "Os dados do PIB para o ano de 2020 não estão disponíveis no CSV."

    pib = resultado["valor"].values[0]
    expected_message = f"The GDP of Brazil in 2020 was: R${pib:,.2f}. Do you want to compare with another year? (Type the year or 'no' to return to the menu)"
    mock_bot.send_message.assert_called_with(mensagem.chat.id, expected_message)

def test_inflation_lookup_no_data(mock_bot):
    """Teste para verificar a resposta do bot quando não há dados de inflação disponíveis."""
    mensagem = Mock()
    mensagem.chat.id = 12345
    mensagem.text = "1800"  # Ano fora do conjunto de dados
    
    estado_conversa[mensagem.chat.id] = "aguardando_ano_inflacao"
    responder(mensagem)

    expected_message = "Sorry, I couldn't find data for the year 1800."
    mock_bot.send_message.assert_called_with(mensagem.chat.id, expected_message)

def test_unemployment_comparison(mock_bot):
    """Teste para comparar taxas de desemprego entre dois anos."""
    mensagem = Mock()
    mensagem.chat.id = 12345

    # Simula o primeiro ano
    mensagem.text = "2020"
    estado_conversa[mensagem.chat.id] = "aguardando_ano_desemprego"
    responder(mensagem)

    desemprego_2020 = dadosDesem[dadosDesem["Ano"] == 2020]["Taxa"].values[0]
    estado_conversa[mensagem.chat.id] = {"ano1": 2020, "desemprego1": desemprego_2020, "proximo": "aguardando_comparacao_desemprego"}

    # Simula o segundo ano
    mensagem.text = "2019"
    responder(mensagem)

    desemprego_2019 = dadosDesem[dadosDesem["Ano"] == 2019]["Taxa"].values[0]
    variacao = ((desemprego_2020 - desemprego_2019) / desemprego_2019) * 100
    status = "increased" if variacao > 0 else "decreased"
    expected_message = (
        f"The unemployment rate in Brazil in 2019 was: {desemprego_2019:.2f}%. "
        f"Compared to 2020, the unemployment rate {status} by {abs(variacao):.2f}."
    )

    mock_bot.send_message.assert_called_with(mensagem.chat.id, expected_message)