
![Captura de tela 2024-05-31 144839](https://github.com/JoaoMMoura/ELT_clima_transito/assets/113948697/fc5ac7f5-2159-49be-b17f-b761a612e038)

![Captura de tela 2024-05-31 143222](https://github.com/JoaoMMoura/escola_dnc/assets/113948697/2b350702-55dd-4a7e-b80e-290fb9806982)

# Projeto de Integração de Dados e Visualização

Este repositório contém a solução desenvolvida para uma empresa fícticia, que consiste em um sistema de integração de dados de Clima e Trânsito, seguido por uma visualização interativa dos mesmos.
Contexto da funcionalidade: Imagine que um cliente more em uma cidade vizinha e precise se deslocar para o seu trabalho. Ele irá enfrentar variações de clima e trânsito. O objetivo é entregar uma painel onde ele possa monitorar como está o trânsito por onde ele irá passar e como está o clima no seu destino.

# Funcionalidade

O objetivo principal é fornecer um painel interativo que permita ao cliente visualizar as condições de trânsito ao longo de sua rota e monitorar as condições climáticas em seu destino. Com isso, ele poderá tomar decisões informadas sobre o melhor momento e a melhor rota para se deslocar, levando em consideração as condições atuais.

## Arquitetura e Tecnologias Utilizadas

- **Extração de Dados:** 
    - Desenvolvimento de um processo de ELT que integra as informações das APIs de Clima e Trânsito.
    - Utilização do Amazon EC2 para hospedar o processo de ELT.
    - Integração com as seguintes APIs:
        - [API de Clima](https://openweathermap.org/api)
        - [API de Trânsito](https://developers.google.com/maps/documentation/directions/overview)

- **Armazenamento de Dados:**
    - Utilização do Snowflake como o banco de dados para armazenar os dados brutos e transformados em schema de staging.
    - Utilização do dbt para realizar as transformações e carregar os dados em um schema analítico separado no Snowflake.

- **Visualização de Dados:**
    - Utilização do Power BI para criar painéis interativos que permitem a exploração intuitiva dos dados de Clima e Trânsito.

- **Agendamento de Tarefas:**
    - Utilização do Apache Airflow para agendar e orquestrar o fluxo de dados, garantindo a execução pontual do ELT conforme as necessidades da API.

## Estrutura do Repositório

- `/dags`: Contém o código responsável pela extração e carregamento dos dados no airflow, que está orquestrado por uma dag.
- `/dbt`: Você pode acessar o repositório do dbt [dbt](https://github.com/JoaoMMoura/dbt_cloud)
- `/docs`: Contém a documentação do projeto.
- `/visualizacao`: Contém os arquivos relacionados à visualização no Power BI, mas você também acessar o [por aqui](https://app.powerbi.com/view?r=eyJrIjoiNTRlNTYyNmYtMWQxNC00NjU2LWJhZGMtZWFhYjYwYTRhZmUyIiwidCI6IjA2MjE5YTRhLWE4MzUtNDRkNS1hZmFmLTM5MjYzNDNiZmI4OSIsImMiOjh9).

Observação: o ELT não está ligado (custos), então os dados podem não estar atualizados quando acessar.

## Instruções para Execução Local

1. **Configuração do Ambiente:**
    - Instale o Apache Airflow.

2. **Configuração das Credenciais:**
    - Configure as credenciais necessárias para acessar as APIs de Clima e Trânsito, bem como as credenciais de acesso ao Snowflake e ao dbt.

3. **Execução do ELT:**
    - Execute o processo de ELT (faça o fork desse repositório), garantindo que as dependências estejam instaladas e as credenciais de acesso configuradas.

4. **Execução do dbt:**
    - Execute o dbt para aplicar as transformações e carregar os dados na camada analítica no Snowflake.

## Segurança da Solução

A solução foi desenvolvida com foco na segurança, garantindo o uso de credenciais de forma segura, além de seguir as melhores práticas de segurança para a integração e armazenamento de dados.
Também foi pensado em um desenvolvimento simples, onde, em caso de aumento do número de clientes para a funcionalidade não gere impacto em custos (por já ter uma EC2 instalada ela pode executar DIVERSOS processos além desse).
Uma boa opção também seria configurar no AWS Lambda, porém com maior complexidade.

## Documentação
