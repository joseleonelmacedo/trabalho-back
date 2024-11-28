import pytest
import pandas as pd

# Dados de exemplo para os testes
dadosInfla = pd.DataFrame({
    'Ano': [2020, 2021, 2022],
    'Brasil': [3.2, 5.4, 6.5]
})

# Função para realizar a comparação da inflação
def calcular_comparacao_inflacao(ano1, ano2):
    # Verificar se o ano1 existe
    if ano1 not in dadosInfla['Ano'].values:
        raise ValueError(f"O ano {ano1} nao foi encontrado nos dados. Por favor, insira um ano válido.")
    
    # Verificar se o ano2 existe
    if ano2 not in dadosInfla['Ano'].values:
        raise ValueError(f"O ano {ano2} nao foi encontrado nos dados. Por favor, insira um ano válido.")
    
    # Obtém os valores da inflação para os anos fornecidos
    inflacao1 = dadosInfla.loc[dadosInfla['Ano'] == ano1, 'Brasil'].values[0]
    inflacao2 = dadosInfla.loc[dadosInfla['Ano'] == ano2, 'Brasil'].values[0]
    
    # Calcula a variação percentual
    variacao = ((inflacao2 - inflacao1) / inflacao1) * 100
    status = "no change" if variacao == 0 else ("increased" if variacao > 0 else "decreased")
    
    return inflacao2, status, abs(variacao)

@pytest.mark.parametrize(
    "ano1, ano2, expected_message",
    [
        # Casos válidos
        (2020, 2021, "The inflation in Brazil in 2021 was: 5.40%. Compared to 2020, the inflation increased by 68.75%."),
        (2021, 2022, "The inflation in Brazil in 2022 was: 6.50%. Compared to 2021, the inflation increased by 20.37%."),
        
        # Casos inválidos
        (2020, 2023, "O ano 2023 nao foi encontrado nos dados. Por favor, insira um ano válido."),
        (2023, 2022, "O ano 2023 nao foi encontrado nos dados. Por favor, insira um ano válido."),
    ]
)
def test_comparacao_inflacao(ano1, ano2, expected_message):
    # Tenta chamar a função de comparação de inflação e verifica o retorno
    try:
        inflacao2, status, variacao = calcular_comparacao_inflacao(ano1, ano2)
        result_message = f"The inflation in Brazil in {ano2} was: {inflacao2:.2f}%. Compared to {ano1}, the inflation {status} by {variacao:.2f}%."
        assert result_message == expected_message
    except ValueError as e:
        # Verifica se a mensagem de erro corresponde ao esperado
        assert str(e) == expected_message