import pytest
import pandas as pd

# Dados de exemplo para os testes
dadosDesem = pd.DataFrame({
    'Ano': [2020, 2021, 2022],
    'Taxa': [13.5, 14.7, 9.3]
})

# Função para realizar a comparação do desemprego
def calcular_comparacao_desemprego(ano1, ano2):
    # Verificar se o ano1 existe
    if ano1 not in dadosDesem['Ano'].values:
        raise ValueError(f"O ano {ano1} não foi encontrado nos dados. Por favor, insira um ano válido.")
    
    # Verificar se o ano2 existe
    if ano2 not in dadosDesem['Ano'].values:
        raise ValueError(f"O ano {ano2} não foi encontrado nos dados. Por favor, insira um ano válido.")
    
    # Obtém os valores da taxa de desemprego para os anos fornecidos
    desemprego1 = dadosDesem.loc[dadosDesem['Ano'] == ano1, 'Taxa'].values[0]
    desemprego2 = dadosDesem.loc[dadosDesem['Ano'] == ano2, 'Taxa'].values[0]
    
    # Calcula a variação percentual
    variacao = ((desemprego2 - desemprego1) / desemprego1) * 100
    status = "no change" if variacao == 0 else ("increased" if variacao > 0 else "decreased")
    
    return desemprego2, status, abs(variacao)

@pytest.mark.parametrize(
    "ano1, ano2, expected_message",
    [
        # Casos válidos
        (2020, 2021, "The unemployment rate in Brazil in 2021 was: 14.70%. Compared to 2020, the unemployment rate increased by 8.89%."),
        (2021, 2022, "The unemployment rate in Brazil in 2022 was: 9.30%. Compared to 2021, the unemployment rate decreased by 36.73%."),
        
        # Casos inválidos
        (2020, 2023, "O ano 2023 não foi encontrado nos dados. Por favor, insira um ano válido."),
        (2023, 2022, "O ano 2023 não foi encontrado nos dados. Por favor, insira um ano válido."),
    ]
)
def test_comparacao_desemprego(ano1, ano2, expected_message):
    # Tenta chamar a função de comparação de desemprego e verifica o retorno
    try:
        desemprego2, status, variacao = calcular_comparacao_desemprego(ano1, ano2)
        result_message = f"The unemployment rate in Brazil in {ano2} was: {desemprego2:.2f}%. Compared to {ano1}, the unemployment rate {status} by {variacao:.2f}%."
        assert result_message == expected_message
    except ValueError as e:
        # Verifica se a mensagem de erro corresponde ao esperado
        assert str(e) == expected_message