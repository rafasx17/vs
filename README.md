API de Gerenciamento de Investimentos
Esta API foi desenvolvida em Python para facilitar o controle de ativos financeiros, focando em praticidade e organização de dados para investidores.

Principais Funcionalidades:

- Registro de compras e vendas de ações e FIIs

- Cálculo automático de preço médio dos ativos

- Histórico de dividendos e proventos recebidos

- Relatório consolidado com valor total investido

- Documentação interativa via Swagger para testes rápidos

Tecnologias Utilizadas:

- Linguagem: Python

- Framework: FastAPI

- Banco de Dados: SQLite

Processamento de dados: Pandas


Como executar o projeto: 

Instale as dependências: pip install fastapi uvicorn pandas yfinance

Inicie o servidor: uvicorn api:app --reload

Acesse a documentação: http://127.0.0.1:8000/docs

Desenvolvido por Rafael Seco Pieniz - Estudante de Ciência da Computação.
