from models.working_data import WorkingData
from sqlalchemy.sql import text
import pandas as pd


def insert_working_data(db, data_ingestao, df, tag, email):
    # Recebe um df com mais de um dado_linha, abre uma transação e insere cada dado_linha no banco
    for index, row in df.iterrows():
        new_data = WorkingData(
            data_ingestao=data_ingestao,
            dado_linha=row['dado_linha'],
            tag=tag,
            createdBy=email
        )
        db.add(new_data)

    db.commit()
    return new_data

# def search_duplicates(db, df_tuple, tag):
#     # Verificar se a lista de tuplas está vazia
#     if not df_tuple:
#         return []

#     # Criar uma lista de condições para cada tupla
#     conditions = " OR ".join(
#         ["(dado_linha = :dado_linha_{})".format(i) for i in range(len(df_tuple))]
#     )

#     # Montar a query dinamicamente
#     query = f"""
#     SELECT *
#     FROM working_data
#     WHERE tag = :tag
#     AND ({conditions})
#     """

#     # Criar dicionário de parâmetros para todas as tuplas e a tag
#     params = {'tag': tag}
#     for i, row in enumerate(df_tuple):
#         dado_linha = row[1]  # Pegando o primeiro elemento da tupla que representa 'dado_linha'
#         print(dado_linha)
#         params[f'dado_linha_{i}'] = dado_linha

#     # Executar a consulta
#     result = db.execute(text(query), params)

#     return result.fetchall()


def search_duplicates(db, df_tuples, tag, batch_size=1000):
    # Verificar se a lista de tuplas está vazia
    if not df_tuples:
        return []

    duplicates = []

    # Processa em lotes
    for i in range(0, len(df_tuples), batch_size):
        batch = df_tuples[i:i + batch_size]

        # Criar uma lista de condições para cada dado_linha no lote
        conditions = " OR ".join(
            ["(dado_linha = :dado_linha_{})".format(j)
             for j in range(len(batch))]
        )

        # Montar a query dinamicamente para o lote atual
        query = f"""
        SELECT *
        FROM working_data
        WHERE tag = :tag
        AND ({conditions})
        """

        # Criar dicionário de parâmetros para cada 'dado_linha' no lote e a 'tag'
        params = {'tag': tag}
        for j, row in enumerate(batch):
            # Pegando o segundo elemento da tupla que representa 'dado_linha'
            dado_linha = row[1]
            params[f'dado_linha_{j}'] = dado_linha

        # Executar a consulta para o lote atual
        result = db.execute(text(query), params)

        fetch = result.fetchall()

        duplicates.extend(fetch)

    return duplicates
