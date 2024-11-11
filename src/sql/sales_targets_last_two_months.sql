CREATE VIEW IF NOT EXISTS sales_targets_last_two_months AS
SELECT
    JSONExtractString (
        target_store.dado_linha,
        'store_id'
    ) AS store_id,
    JSONExtractString (
        store_final.dado_linha,
        'nome_loja'
    ) AS nome_loja,
    JSONExtractString (
        store_final.dado_linha,
        'regiao'
    ) AS regiao,
    JSONExtractString (
        store_final.dado_linha,
        'diretoria'
    ) AS diretoria,
    JSONExtractString (
        target_store.dado_linha,
        'month'
    ) AS month,
    JSONExtractFloat (
        target_store.dado_linha,
        'sales_target'
    ) AS sales_target,
    IF(
        length(
            JSONExtractString (
                target_store.dado_linha,
                'month'
            )
        ) >= 7
        AND toInt32 (
            substr(
                JSONExtractString (
                    target_store.dado_linha,
                    'month'
                ),
                1,
                2
            )
        ) = toMonth (now())
        AND toInt32 (
            substr(
                JSONExtractString (
                    target_store.dado_linha,
                    'month'
                ),
                4,
                4
            )
        ) = toYear (now()),
        'current_month',
        'previous_month'
    ) AS period
FROM
    working_data target_store
    JOIN working_data store_final ON JSONExtractString (
        target_store.dado_linha,
        'store_id'
    ) = JSONExtractString (
        store_final.dado_linha,
        'nome_loja'
    )
WHERE
    target_store.tag = 'target_store'
    AND store_final.tag = 'store_final'
    AND length(
        JSONExtractString (
            target_store.dado_linha,
            'month'
        )
    ) >= 7
    AND (
        (
            toInt32 (
                substr(
                    JSONExtractString (
                        target_store.dado_linha,
                        'month'
                    ),
                    1,
                    2
                )
            ) = toMonth (now())
            AND toInt32 (
                substr(
                    JSONExtractString (
                        target_store.dado_linha,
                        'month'
                    ),
                    4,
                    4
                )
            ) = toYear (now())
        )
        OR (
            toInt32 (
                substr(
                    JSONExtractString (
                        target_store.dado_linha,
                        'month'
                    ),
                    1,
                    2
                )
            ) = toMonth (now()) - 1
            AND toInt32 (
                substr(
                    JSONExtractString (
                        target_store.dado_linha,
                        'month'
                    ),
                    4,
                    4
                )
            ) = toYear (now())
        )
    )
ORDER BY nome_loja, month LIMIT 5000000;