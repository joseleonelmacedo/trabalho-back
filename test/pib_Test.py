import pytest
import pandas as pd

# Dados de exemplo para os testes
dadosPib = pd.DataFrame({
    'Ano': [2020, 2021, 2022],
    'valor': [2000.00, 2200.00, 2500.00]
})

# Função para realizar a comparação do PIB
def calcular_comparacao_pib(ano1, ano2):
    # Verificar se o ano1 existe
    if ano1 not in dadosPib['Ano'].values:
        raise ValueError(f"O ano {ano1} não foi encontrado nos dados. Por favor, insira um ano válido.")
    
    # Verificar se o ano2 existe
    if ano2 not in dadosPib['Ano'].values:
        raise ValueError(f"O ano {ano2} não foi encontrado nos dados. Por favor, insira um ano válido.")
    
    # Obtém os valores do PIB para os anos fornecidos
    pib1 = dadosPib.loc[dadosPib['Ano'] == ano1, 'valor'].values[0]
    pib2 = dadosPib.loc[dadosPib['Ano'] == ano2, 'valor'].values[0]

    # Calcula a variação percentual
    variacao = ((pib2 - pib1) / pib1) * 100
    status = "no change" if variacao == 0 else ("increased" if variacao > 0 else "decreased")
    
    return pib2, status, abs(variacao)

@pytest.mark.parametrize(
    "ano1, ano2, expected_message",
    [
        # Casos válidos
        (2020, 2021, "The GDP of Brazil in 2021 was: R$2,200.00. Compared to 2020, the GDP increased by 10.00%."),
        (2021, 2022, "The GDP of Brazil in 2022 was: R$2,500.00. Compared to 2021, the GDP increased by 13.64%."),
        
        # Casos inválidos
        (2020, 2023, "O ano 2023 não foi encontrado nos dados. Por favor, insira um ano válido."),
        (2023, 2022, "O ano 2023 não foi encontrado nos dados. Por favor, insira um ano válido."),
    ]
)
def test_comparacao_pib(ano1, ano2, expected_message):
    # Tenta chamar a função de comparação de PIB e verifica o retorno
    try:
        pib2, status, variacao = calcular_comparacao_pib(ano1, ano2)
        result_message = f"The GDP of Brazil in {ano2} was: R${pib2:,.2f}. Compared to {ano1}, the GDP {status} by {variacao:.2f}%."
        assert result_message == expected_message
    except ValueError as e:
        # Verifica se a mensagem de erro corresponde ao esperado
        assert str(e) == expected_message