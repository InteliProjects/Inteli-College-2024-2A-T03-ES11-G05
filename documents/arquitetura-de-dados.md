# Documentação da Arquitetura de 3 Camadas da API

### 1. Camada de Apresentação
A "Camada de Apresentação" é responsável por lidar com a interação do cliente da API. Essa camada expõe os endpoints que permitem ao cliente fazer solicitações HTTP (GET, POST, etc.) e acessar os recursos fornecidos pela API.

- **Função**: Utiliza o React como framework para a construção de uma aplicação mobile, que serve como a interface de comunicação entre o usuário e o backend da API, exibindo listas de produtos com maior margem de lucro para os vendedores, qual a meta a ser atingida pelos colaboradores, gráficos de metas para os gerentes, etc.
  
Além disso, a API também utiliza o FastAPI para fornecer uma interface REST para ingestão de dados. O FastAPI é utilizado para expor os endpoints da API.

- **Função**:
  - `POST /ingest/`: Este é o endpoint que recebe os arquivos via upload e os processa. Então, cada arquivo contendo informações sobre produtos, colaboradores e lucro é processado e salvo com uma tag gerada dinamicamente .
  - `GET /visualize/{tag}`: Este é o endpoint que permite visualizar os dados processados com base em uma tag específica. Nesse sentido, este endpoint será utilizado quando, por exemplo, um vendedor buscar um produto que esse quer vender.

#### Exemplo de Endpoints:
```python
@ingest_router.post("/")
async def postIngest(files: List[UploadFile] = File(...)):
    # Recebe múltiplos arquivos, processando-os e armazenando os dados fornecidos.
    ...

@ingest_router.get("/visualize/{tag}")
async def get_visualize(tag: str):
    # Recupera e visualiza dados de produtos, funcionários e estoque a partir de uma tag
    ...
```

### 2. Camada de Negócio
A "Camada de Negócio" é a responsável por toda a definição da lógica de negócio da API construída. É nela que ocorre a validação e aplicação das regras de negócio antes que os dados sejam salvos ou recuperados dos bancos de dados. Na camada de negócio, há o recebimento de todas as requisições da camada de apresentação e são realizadas as tarefas que foram definidas nas regras de negócio. Além disso, foi utilizado o "Flask" que é um framework que facilita a criação dos endpoints REST da API.

- **Função**: 
  - **Serviço de Ingestão**: Manipula o processamento de arquivos, faz o upload para o Supabase, baixa os arquivos, prepara os dados para inserção no banco de dados, e faz a persistência dos dados.
  - As funções de manipulação dos dados incluem operações como a preparação do DataFrame e a verificação de duplicidade antes da inserção no banco.

#### Funções Importantes:
- **`process_and_save_data(file, tag)`**: Recebe os arquivos enviados, converte eles para o formato Parquet, e faz o upload para o Supabase. Depois disso, baixa o arquivos, prepara os dados e insere-os no banco de dados. Tal método terá aplicações em funcionalidades como a persistência das metas dos vendedores e dos gerentes.
  
```python
def process_and_save_data(file, tag):
    # Processa o arquivo CSV, converte para Parquet, faz upload para Supabase
    # e insere os dados no banco de dados.
    ...
```

- **`get_data_by_tag(tag)`**: Busca os dados no banco de dados usando uma tag específica e retorna os resultados para a camada de apresentação. Tal método será muito utilizado para a requisição de certos produtos e de outros similares ao que o vendedor está visualizando

```python
def get_data_by_tag(tag: str) -> List[Dict]:
    # Recupera os dados no banco de dados baseados na tag fornecida.
    ...
```

### 3. Camada de Acesso a Dados
A "Camada de Acesso a Dados" atua na manipulação da conservação e da recuperação dos dados diretamente do banco de dados ClickHouse. Ela simplifica operações de banco de dados para que a camada de negócio não precise lidar com muitos detalhes da linguagem SQL ou com muitas interações diretas com a base de dados. Nessa camada, utilizamos o "Supabase" que armazena e gerencia os arquivos processados, permitindo assim, que a API baixe e trabalhe com os dados de forma eficiente.

- **Funções**:
  - **`insert_working_data`**: Insere os dados no banco de dados ClickHouse. Aqui podem ser salvos dados de novos produtos, metas de gerentes e vendedores, qual o estoque de determinado produto, etc.Tal método faz isso recebendo uma tabela e inserindo cada linha como um novo registro na tabela `WorkingData`. Essa inserção é realizada dentro de uma transação para garantir consistência.
  - **`search_duplicates`**: Verifica se existem dados duplicados no banco de dados antes de inserir novos dados. Essa operação é otimizada para lidar com grandes volumes de dados usando processamento em lotes.

#### Funções Importantes:
- **`insert_working_data(db, data_ingestao, df, tag, email)`**: Insere os dados de ingestão no banco, associando cada linha com uma tag e o email do usuário responsável pela criação.

```python
def insert_working_data(db, data_ingestao, df, tag, email):
    # Insere cada linha do DataFrame no banco de dados com a tag e o email do responsável.
    ...
```

- **`search_duplicates(db, df_tuples, tag, batch_size=1000)`**: Realiza a verificação de dados duplicados por meio de uma consulta dinâmica que compara as linhas do `DataFrame` com as já presentes no banco de dados.

```python
def search_duplicates(db, df_tuples, tag, batch_size=1000):
    # Busca por dados duplicados no banco de dados baseado na tag e nas linhas do DataFrame.
    ...
```
