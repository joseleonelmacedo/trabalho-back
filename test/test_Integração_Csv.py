import pytest
import pandas as pd
from io import StringIO

# Função que imita a leitura dos arquivos CSV, fornecendo dados fictícios para os testes
@pytest.fixture
def mock_csv_data():
    pib_data = """Ano;valor
    2020;"2,000,000,000"
    2021;"2,500,000,000"
    """
    inflacao_data = """Ano;Brasil
    2020;3,5%
    2021;4,0%
    """
    desemprego_data = """Ano;Taxa
    2020;14,5%
    2021;12,3%
    """
    return {
        "pib": StringIO(pib_data),
        "inflacao": StringIO(inflacao_data),
        "desemprego": StringIO(desemprego_data),
    }

def test_process_pib(mock_csv_data):
    # Lê os dados de PIB do CSV
    df_pib = pd.read_csv(mock_csv_data["pib"], delimiter=";", dtype={"Ano": int, "valor": str})
    
    # Primeiro, substitui a vírgula por ponto decimal
    df_pib["valor"] = df_pib["valor"].str.replace(',', '.')
    
    # Remove os pontos usados como separadores de milhar
    df_pib["valor"] = df_pib["valor"].str.replace('.', '', regex=False)
    
    # Converte a coluna para tipo float
    df_pib["valor"] = df_pib["valor"].astype(float)
    
    # Verifique se os dados foram processados corretamente
    assert df_pib["valor"].iloc[0] == 2000000000.0
    assert df_pib["valor"].iloc[1] == 2500000000.0



def test_process_inflacao(mock_csv_data):
    # Lê os dados de Inflação do CSV
    df_inflacao = pd.read_csv(mock_csv_data["inflacao"], delimiter=";", dtype={"Ano": int, "Brasil": str})
    
    # Remove os pontos, vírgulas e o símbolo de porcentagem antes de converter para float
    df_inflacao["Brasil"] = df_inflacao["Brasil"].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.replace('%', '', regex=False).str.strip().astype(float)
    
    # Verifique se os dados foram processados corretamente
    assert df_inflacao["Brasil"].iloc[0] == 3.5
    assert df_inflacao["Brasil"].iloc[1] == 4.0

def test_process_desemprego(mock_csv_data):
    # Lê os dados de Desemprego do CSV
    df_desemprego = pd.read_csv(mock_csv_data["desemprego"], delimiter=";", dtype={"Ano": int, "Taxa": str})
    
    # Remove os pontos, vírgulas e o símbolo de porcentagem antes de converter para float
    df_desemprego["Taxa"] = df_desemprego["Taxa"].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.replace('%', '', regex=False).str.strip().astype(float)
    
    # Verifique se os dados foram processados corretamente
    assert df_desemprego["Taxa"].iloc[0] == 14.5
    assert df_desemprego["Taxa"].iloc[1] == 12.3