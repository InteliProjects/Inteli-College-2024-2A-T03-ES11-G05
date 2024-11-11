CREATE VIEW IF NOT EXISTS sales_by_category_last_two_months AS
SELECT
    JSONExtractString (
        transactions.dado_linha,
        'cod_loja'
    ) AS store_id,
    JSONExtractString (sku.dado_linha, 'categoria') AS product_category,
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
    ) AS total_sales
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
    product_category,
    year,
    month
ORDER BY
    store_id,
    product_category,
    year DESC,
    month DESC
LIMIT 5000000;