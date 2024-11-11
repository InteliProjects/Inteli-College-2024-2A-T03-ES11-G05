CREATE VIEW IF NOT EXISTS store_sales_last_six_months AS
SELECT
    JSONExtractString (
        transactions.dado_linha,
        'cod_loja'
    ) AS store_id,
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
FROM working_data transactions
WHERE
    transactions.tag = 'transaction_fact'
    AND toDate (
        JSONExtractString (
            transactions.dado_linha,
            'data'
        )
    ) >= addMonths (today (), -6)
GROUP BY
    store_id,
    year,
    month
ORDER BY year DESC, month DESC, store_id
LIMIT 5000000;