# Objetivo do projeto / Project's goal
'''
[PT-BR]

Neste projeto, o objetivo é criar um pipeline de dados completo. Embora estejamos usando um conjunto de dados pequeno, o "processo" é semelhante para grandes conjuntos de dados.

O que pode mudar, naturalmente, são os métodos de leitura (mais adequados para volumes grandes de dados) e a transformação (que poderia ser feita em SQL ou pyspark, por exemplo).

Sendo assim, o último passo é enviar os dados transformados para um datalake. Neste caso, teríamos um "job" que coleta os dados e os transforma, e depois envia para um local centralizado onde outras análises poderiam ser realizadas.

[EN]

In this project, the goal is to create a complete data pipeline. Although we are using a small data set, the “process” is similar for large data sets.

What can change, of course, are the reading methods (more suitable for large volumes of data) and the transformation (which could be done in SQL or pyspark, for example).

Therefore, the last step is to send the transformed data to a datalake. In this case, we would have a “job” that collects the data and transforms it, and then sends it to a centralized location where other analyzes could be carried out.
'''

import requests
import pandas as pd
import pandas_gbq
import io
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

"""# Passo 01: Coleta de dados na fonte / Step 01: Data collection at the source"""

import requests
import pandas as pd

# URL da fonte de dados / Data source URL
url = "https://www.cepea.esalq.usp.br/br/indicador/frango.aspx"

# Informações para simular um navegador / Information to simulate a browser
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

try:
    # Fazendo a requisição / Making the request
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Verifica se houve algum erro na requisição / Checks for request errors

    # Lendo as tabelas da página / Reading tables from the page
    tables = pd.read_html(io.StringIO(response.text), thousands='.', decimal=',')

    # Verificando se alguma tabela foi encontrada / Checking if any table was found
    if tables:
        df = tables[0]  # Assume-se que a tabela de interesse é a primeira / Assuming the first table is of interest
        print(df.head())  # Exibe as primeiras linhas da tabela / Displays the first rows of the table
    else:
        print("Nenhuma tabela encontrada na página.")  # No table found on the page

except requests.exceptions.RequestException as e:
    print(f"Erro ao acessar a página: {e}")  # Error accessing the page
except ValueError as e:
    print(f"Erro ao processar os dados da tabela: {e}")  # Error processing table data

# Verificando o tamanho do dataset e o tipo de dado / Checking dataset size and data types
df.info()

"""# Passo 02: transformação e padronização do dataset / Step 02: transformation and standardization of the dataset

[PT-BR] Iremos realizar 3 tranfromações na base de dados

1. Mudaremos o nome da tabela de data de "Unnamed:0" para "Data"
2. Renomearemos as colunas para um padrão mais adequado para leituras em banco de dados
3. Ajustaremos os tipos de dados para os adequados.

[EN] We will perform 4 transformations in the database

1. We will rename the date table from "Unnamed:0" to "Date"
2. We will rename the columns to a pattern more suitable for database readings
3. We will adjust the data types to the appropriate ones.
"""

def transformation(df):

    # 1. Renomear a coluna "Unnamed: 0" para "Data" / Rename column "Unnamed: 0" to "data"
    df = df.rename(columns={'Unnamed: 0': 'data'})

    # 2. Renomear as colunas para um padrão mais adequado / Rename columns for a more suitable pattern
    df = df.rename(columns={
        'Valor R$': 'valor',
        'Var./Dia': 'variacao_dia',
        'Var./Mês': 'variacao_mes'
    })

    # 3. Ajustar os tipos de dados / Adjust data types
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['valor'] = df['valor'].astype(float)
    df['variacao_dia'] = df['variacao_dia'].str.replace(',', '.').str.rstrip('%').astype(float) / 100
    df['variacao_mes'] = df['variacao_mes'].str.replace(',', '.').str.rstrip('%').astype(float) / 100

    return df

# Aplicando as transformações / Applying the transformations
df_transformed = transformation(df)

df_transformed.head()

df_transformed.info()

"""# Passo 03: enviar os dados para um banco de dados / Step 03: send the data to a database

[PT-BR] Neste caso, iremos enviar para um datalake no Google Big Query

[EN] In this case, we will send it to a datalake in Google Big Query
"""

def upload_to_bigquery(df, table_id, project_id, credentials_info):

    # Escopos necessários para acessar o BigQuery / Required scopes for accessing BigQuery
    SCOPES = [
        'https://www.googleapis.com/auth/cloud-platform'
    ]

    # Credenciais da conta de serviço / Service account credentials
    credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)

    # Definindo o contexto de credenciais e projeto do pandas-gbq / Setting the credentials and project context for pandas-gbq
    pandas_gbq.context.credentials = credentials
    pandas_gbq.context.project = project_id

    # Enviando o DataFrame para o BigQuery / Sending the DataFrame to BigQuery
    pandas_gbq.to_gbq(df, table_id, project_id=project_id, if_exists='replace')

credentials_info = {
    "type": os.getenv('TYPE'),
    "project_id": os.getenv('PROJECT_ID'),
    "private_key_id": os.getenv('PRIVATE_KEY_ID'),
    "private_key": os.getenv('PRIVATE_KEY').replace('\\n', '\n'),  # Substituir '\n' por quebras de linha reais
    "client_email": os.getenv('CLIENT_EMAIL'),
    "client_id": os.getenv('CLIENT_ID'),
    "auth_uri": os.getenv('AUTH_URI'),
    "token_uri": os.getenv('TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL'),
    "universe_domain": os.getenv('UNIVERSE_DOMAIN'),
}

table_id = '02_cotacao_frango.Cotacoes'
project_id = os.getenv('PROJECT_ID')

# Chamada da função para realizar o upload / Function call to perform the upload
upload_to_bigquery(df_transformed, table_id, project_id, credentials_info)

"""# Próximos passos / Next Steps

[PT-BR] O próximo passo deste projeto é construir a visualização dos dados. Iremos realizar este processo no Power BI. Lá, conectaremos no Google Big Query, acessaremos a tabela e criaremos um dashboard com as análises.

[EN] The next step of this project is to build the data visualization. We will carry out this process in Power BI. There, we will connect to Google Big Query, access the table and create a dashboard with the analyses.
"""