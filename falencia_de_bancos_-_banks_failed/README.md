# Resumo do projeto | Project's summary

[PT] 

## Objetivo do projeto
A ideia deste projeto é monitorarmos o número de falências bancárias de bancos segurados pelo FIDC nos Estados Unidos. Este dado é alimentado pelo Federal Deposit Insurance Corporation (FIDC) e é atualizado sempre que um novo evento do tipo acontece. 

## O que a FIDC considera falência? 
* Uma falência bancária é o fechamento de um banco por uma agência reguladora bancária federal ou estadual. Geralmente, um banco é fechado quando não consegue cumprir suas obrigações com os depositantes e outros. Este trabalho trata da falência de "bancos segurados". O termo "banco segurado" significa um banco segurado pelo FDIC, incluindo bancos credenciados pelo governo federal, bem como a maioria dos bancos credenciados pelos governos estaduais. Um banco segurado deve exibir um sinal oficial do FDIC em cada caixa.

## Qual stack de dados foi utilizada?
* Através deste projeto tentamos explorar 3 ferramentas muito utilizadas no dia a dia de dados: python, google big query e Power BI. 

1. *Python*: foi utilizado para o processo ETL desse projeto (que de um modo geral seria simples). Com ele, conectamos na fonte de dados, tratamos a informação para o formato mais adequado ao Power BI e subimos a informação tratada para a núvem. 
2. *Google Big Query*: foi utilizado para armazenar as tabelas que foram tratadas no Python. Assim, temos o dado disponível em um ambiente cloud. 
3. *Power BI*: foi utilizado como "deploy" do projeto. Com ele, conectamos no Google Big Query, extraímos as informações e geramos as visualizações mais adequadas. 

*OBS: sabemos que o Power BI possui um recurso nativo para leitura de conteúdos WEB. Porém, o objetivo desse trabalho era testarmos uma estrutura mais robusta e com maiores possibilidades, o que, por nossa decisão, justificou a inclusão do Python e do Google Big Query neste escopo. Com estas outras duas ferramentas, nosso leque de possibilidades aumenta de forma exponencial, e ter essa stack testada será muito relevante para os projetos futuros.*


