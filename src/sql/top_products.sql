CREATE VIEW IF NOT EXISTS top_products AS
WITH
    ranked_sales AS (
        SELECT
            JSONExtractString (
                transactions.dado_linha,
                'cod_loja'
            ) AS store_id,
            JSONExtractString (
                sku.dado_linha,
                'nome_completo'
            ) AS product_name,
            toYear (
                toDate (
                    JSONExtractString (
                        transactions.dado_linha,
                        'data'
                    )
                )
            ) AS year,
            toMonth (
                toDate (
                    JSONExtractString (
                        transactions.dado_linha,
                        'data'
                    )
                )
            ) AS month,
            SUM(
                JSONExtractFloat (
                    transactions.dado_linha,
                    'preco'
                ) * JSONExtractInt (
                    transactions.dado_linha,
                    'quantidade'
                )
            ) AS total_sales,
            ROW_NUMBER() OVER (
                PARTITION BY
                    JSONExtractString (
                        transactions.dado_linha,
                        'cod_loja'
                    ),
                    toYear (
                        toDate (
                            JSONExtractString (
                                transactions.dado_linha,
                                'data'
                            )
                        )
                    ),
                    toMonth (
                        toDate (
                            JSONExtractString (
                                transactions.dado_linha,
                                'data'
                            )
                        )
                    )
                ORDER BY SUM(
                        JSONExtractFloat (
                            transactions.dado_linha, 'preco'
                        ) * JSONExtractInt (
                            transactions.dado_linha, 'quantidade'
                        )
                    ) DESC
            ) AS rank
        FROM
            working_data transactions
            JOIN working_data sku ON JSONExtractInt (
                transactions.dado_linha,
                'cod_prod'
            ) = JSONExtractInt (sku.dado_linha, 'cod_prod')
        WHERE
            transactions.tag = 'transaction_fact'
            AND sku.tag = 'sku_dataset'
            AND toMonth (
                toDate (
                    JSONExtractString (
                        transactions.dado_linha,
                        'data'
                    )
                )
            ) IN (
                toMonth (now()),
                toMonth (now()) - 1
            )
            AND toYear (
                toDate (
                    JSONExtractString (
                        transactions.dado_linha,
                        'data'
                    )
                )
            ) = toYear (now())
        GROUP BY
            store_id,
            product_name,
            year,
            month
    )
SELECT
    store_id,
    product_name,
    year,
    month,
    total_sales
FROM ranked_sales
WHERE
    rank <= 5
ORDER BY store_id, year DESC, month DESC, total_sales DESC
LIMIT 5000000;