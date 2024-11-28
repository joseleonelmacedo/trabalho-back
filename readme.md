ZENBOT - Projeto Integrador de Testes de Software, Back-End, Ciência de Dados e IA

O ZENBOT é uma API integrada ao Telegram que permite consultar dados de inflação no Brasil ao longo dos anos. Este projeto combina práticas de desenvolvimento de back-end com análise de dados econômicos e testes de software, garantindo a confiabilidade e funcionalidade do sistema. O objetivo principal é oferecer acesso rápido e fácil às informações, ajudando a acompanhar e entender melhor a economia brasileira. Além disso, o ZENBOT também permite consultar dados sobre desemprego e PIB, e realizar comparações entre diferentes períodos.

### 1. Funcionalidades
- Consulta de dados de inflação para diferentes anos no Brasil.
- Interação por meio de um bot no Telegram.
- Integração com conjuntos de dados econômicos (CSV) para processamento e análise.
- Sistema modular, facilitando futuras expansões, como a inclusão de outros indicadores econômicos.

### 2. Estrutura do Projeto
- Back-End: Desenvolvido em Python, com foco em manipulação de dados e respostas rápidas.
- Bot no Telegram: Responsável pela interação com os usuários e exibição das informações solicitadas.
- Testes Automatizados: Garantem a precisão e a estabilidade do sistema.
- Ciência de Dados: Utilização de bibliotecas como pandas para leitura e análise de dados econômicos.

### 3. Cobertura de Testes

Ferramentas Utilizadas:
- pytest e pytest-cov: Aplicados para executar os testes e gerar relatórios de cobertura.

Cobertura Atual:
- 85%, abrangendo principalmente funções essenciais, como cálculos e consultas aos dados.

Resultados dos Testes:
- Funções testadas:
  - Cálculo e exibição de inflação.
  - Validação de entradas dos usuários (anos inválidos, valores nulos, etc.).

### 4. Análise dos Resultados

- Alta precisão nos cálculos de inflação.
- Funções de manipulação de dados robustas.
- Estrutura bem organizada, facilitando a manutenção e os testes.

- Dependência de dados bem formatados nos arquivos CSV.

### 5. Conclusão e Aprendizados

O desenvolvimento do ZENBOT foi uma experiência enriquecedora, tanto em termos de colaboração quanto de aprendizado técnico. Alguns destaques incluem:

- Importância dos Testes: A inclusão de testes automatizados reforçou a confiabilidade do sistema, ajudando a identificar e corrigir problemas antes da entrega final.

Principais Aprendizados:
- Ferramentas como pytest são essenciais para construir APIs estáveis.
- Uma análise detalhada dos dados garante resultados mais precisos e úteis para os usuários.